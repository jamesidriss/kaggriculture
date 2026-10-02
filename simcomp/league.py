"""Paired, both-seat, official-path evaluation.

Every number this module produces goes through `Environment.run`. That is not a
style preference: the alternative — driving `env.step()` by hand and feeding the
agent `env.steps[i][seat].observation` — silently drops shared observation
fields for seat 1 and produces crashes that cannot occur on the real server.
That bug cost the previous audit its headline finding.
"""
import importlib.util
import math
import os

from .stats import wilson


def load_agent(path, name=None):
    """Import an agent module from an exact file path.

    Returns a callable with a uniform `(obs, configuration)` signature.
    Necessary because Kaggle invokes agents as `agent(obs, configuration)` while
    a large share of the public agents define `def agent(obs)`. Calling the
    one-argument form with two positional arguments raises TypeError on every
    turn, and the agent then plays passively and still "wins" 170k to 3k --
    a spectacular false positive. The signature is therefore introspected.
    """
    import inspect
    name = name or ("agent_" + hashlib12(path))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "agent"):
        raise AttributeError(f"{path} defines no agent(obs) function")
    fn = mod.agent
    try:
        sig = inspect.signature(fn)
        npos = sum(1 for p in sig.parameters.values()
                   if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
        has_var = any(p.kind == p.VAR_POSITIONAL for p in sig.parameters.values())
    except (TypeError, ValueError):
        npos, has_var = 2, True
    if has_var or npos >= 2:
        def _call(obs, configuration=None):
            return fn(obs, configuration)
    else:
        def _call(obs, configuration=None):
            return fn(obs)
    _call.__wrapped__ = fn
    return _call


def hashlib12(path):
    import hashlib
    return hashlib.sha256(path.encode()).hexdigest()[:12]


class Match:
    __slots__ = ("seed", "seat", "cand_cash", "opp_cash", "cand_status",
                 "opp_status", "cand_ms", "opp_ms", "error")

    def __init__(self, seed, seat, cand_cash, opp_cash, cand_status, opp_status,
                 cand_ms, opp_ms, error=None):
        self.seed, self.seat = seed, seat
        self.cand_cash, self.opp_cash = cand_cash, opp_cash
        self.cand_status, self.opp_status = cand_status, opp_status
        self.cand_ms, self.opp_ms = cand_ms, opp_ms
        self.error = error

    def outcome(self):
        """W/L/T from the CANDIDATE's perspective. Ties are exact equality."""
        if self.error:
            return None
        if self.cand_cash > self.opp_cash:
            return "W"
        if self.cand_cash < self.opp_cash:
            return "L"
        return "T"


class Result:
    def __init__(self, candidate, opponent, pool, matches, meta=None):
        self.candidate = candidate
        self.opponent = opponent
        self.pool = pool
        self.matches = matches
        self.meta = meta or {}

    @property
    def games(self):
        return len(self.matches)

    def counts(self):
        w = l = t = e = 0
        for m in self.matches:
            o = m.outcome()
            if o == "W":
                w += 1
            elif o == "L":
                l += 1
            elif o == "T":
                t += 1
            else:
                e += 1
        return w, l, t, e

    def win_rate(self):
        w, l, t, e = self.counts()
        n = w + l + t
        return w / n if n else 0.0

    def wilson95(self):
        w, l, t, e = self.counts()
        n = w + l + t
        return wilson(w, n) if n else (0.0, 1.0)

    def summary(self):
        w, l, t, e = self.counts()
        lo, hi = self.wilson95()
        return {
            "candidate": self.candidate, "opponent": self.opponent,
            "pool": self.pool, "games": self.games, "W": w, "L": l, "T": t,
            "errors": e, "win_rate": round(self.win_rate(), 4),
            "wilson95": [round(lo, 4), round(hi, 4)],
            "seat0_W": sum(1 for m in self.matches if m.seat == 0 and m.outcome() == "W"),
            "seat1_W": sum(1 for m in self.matches if m.seat == 1 and m.outcome() == "W"),
            "median_cash": self._median("cand_cash"),
            "mean_cash": self._mean("cand_cash"),
            "mean_opp_cash": self._mean("opp_cash"),
            "max_runtime_ms": self._max_runtime(),
            **self.meta,
        }

    def _vals(self, attr):
        return [getattr(m, attr) for m in self.matches
                if getattr(m, attr) is not None and m.error is None]

    def _median(self, attr):
        v = sorted(self._vals(attr))
        if not v:
            return None
        n = len(v)
        return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) // 2

    def _mean(self, attr):
        v = self._vals(attr)
        return int(sum(v) / len(v)) if v else None

    def _max_runtime(self):
        v = [x for m in self.matches for x in (m.cand_ms, m.opp_ms)
             if x is not None]
        return max(v) if v else None

    # ---- assertions ------------------------------------------------------
    def assert_clean(self, both_seats=True):
        w, l, t, e = self.counts()
        if e:
            raise AssertionError(f"{self.candidate} vs {self.opponent} "
                                 f"({self.pool}): {e} errored game(s)")
        if t:
            raise AssertionError(
                f"{self.candidate} vs {self.opponent} ({self.pool}): {t} exact "
                f"tie(s). Two distinct agents producing identical cash is a "
                f"self-play / duplicate-content signal, not a result.")
        if both_seats:
            seats = {m.seat for m in self.matches}
            if seats != {0, 1}:
                raise AssertionError(f"seats covered: {sorted(seats)}, need 0 and 1")
            seeds0 = {m.seed for m in self.matches if m.seat == 0}
            seeds1 = {m.seed for m in self.matches if m.seat == 1}
            if seeds0 != seeds1:
                raise AssertionError("seat sets are not paired: "
                                     f"{sorted(seeds0 ^ seeds1)[:5]}")
        for m in self.matches:
            if m.cand_status != "DONE" or m.opp_status != "DONE":
                raise AssertionError(f"non-DONE status at seed {m.seed} seat {m.seat}: "
                                     f"{m.cand_status}/{m.opp_status}")
        return self

    def assert_discriminating(self, threshold=0.90):
        """A sweep means the league cannot discriminate. That is a failure.

        Refusing to celebrate an undefeated record is the single most useful
        behaviour in this harness. It is what would have caught the 360-0
        result that was really 216-48.
        """
        if self.win_rate() >= threshold and self.games >= 8:
            lo, hi = self.wilson95()
            raise AssertionError(
                f"{self.candidate} beat {self.opponent} {self.win_rate():.0%} "
                f"of {self.games} games (Wilson [{lo:.3f},{hi:.3f}]). The league "
                f"is not discriminating: find a stronger opponent before "
                f"reading anything into this number.")
        return self


class League:
    """Runs a candidate against a league through the official environment."""

    def __init__(self, registry, env_name="kaggriculture", episode_steps=720,
                 config=None):
        self.reg = registry
        self.env_name = env_name
        self.episode_steps = episode_steps
        self.extra_config = config or {}

    def _env(self, seed):
        from kaggle_environments import make
        cfg = {"seed": seed, "episodeSteps": self.episode_steps}
        cfg.update(self.extra_config)
        env = make(self.env_name, configuration=cfg)
        env.reset()
        return env

    def play(self, cand_path, opp_path, seed, cand_seat):
        """One game, both agents driven by Environment.run."""
        import time
        cand = load_agent(cand_path)
        opp = load_agent(opp_path)
        times = {}
        errors = {}

        def wrap(fn, tag):
            def _a(obs, configuration=None):
                t0 = time.perf_counter()
                try:
                    r = fn(obs, configuration)
                except Exception as exc:  # noqa: BLE001
                    errors[tag] = f"{type(exc).__name__}: {exc}"
                    r = {"farmer": ["PASS"], "hands": [], "market": []}
                times[tag] = (time.perf_counter() - t0) * 1000
                return r
            return _a

        env = self._env(seed)
        seats = [wrap(cand, "cand"), wrap(opp, "opp")] if cand_seat == 0 \
            else [wrap(opp, "opp"), wrap(cand, "cand")]
        env.run(seats)
        f = env.steps[-1]
        cs = int(f[cand_seat].observation.farms[cand_seat]["money"])
        os_ = 1 - cand_seat
        oc = int(f[os_].observation.farms[os_]["money"])
        return Match(seed=seed, seat=cand_seat, cand_cash=cs, opp_cash=oc,
                     cand_status=f[cand_seat].status, opp_status=f[os_].status,
                     cand_ms=times.get("cand"), opp_ms=times.get("opp"),
                     error="; ".join(f"{k}: {v}" for k, v in errors.items()) or None)

    def head_to_head(self, cand, opp, seeds, meta=None):
        """Every seed from BOTH seats. The candidate plays `opp` twice per seed."""
        a = self.reg.get(cand) if isinstance(cand, str) else cand
        b = self.reg.get(opp) if isinstance(opp, str) else opp
        if a.sha256 == b.sha256:
            raise ValueError(f"self-play refused: {a.name} and {b.name} are the "
                             f"same content ({a.short})")
        matches = []
        for s in seeds:
            for seat in (0, 1):
                matches.append(self.play(a.path, b.path, s, seat))
        return Result(a.name, b.name, meta.get("pool", "?") if meta else "?",
                      matches, meta)

    def run(self, cand, pool="dev", seeds=None, both_seats=True, meta=None):
        """Candidate against every eligible league member."""
        from .seeds import SeedSplits  # local import to avoid a cycle
        if seeds is None:
            seeds = SeedSplits(self.reg.config["seed_dir"]).load(pool)
        a = self.reg.get(cand) if isinstance(cand, str) else cand
        results = []
        for b in self.reg.eligible():
            if b.sha256 == a.sha256:
                continue
            m = dict(meta or {})
            m["pool"] = pool
            m["candidate_sha256"] = a.sha256
            m["opponent_sha256"] = b.sha256
            m["delivery_path"] = f"kaggle_environments...Environment.run[{self.env_name}]"
            results.append(self.head_to_head(a, b, seeds, m))
        return results

    @staticmethod
    def summarise(results):
        return [r.summary() for r in results]

    @staticmethod
    def totals(results):
        w = l = t = e = n = 0
        for r in results:
            a, b, c, d = r.counts()
            w += a; l += b; t += c; e += d; n += r.games
        lo, hi = wilson(w, n) if n else (0.0, 1.0)
        return {"games": n, "W": w, "L": l, "T": t, "errors": e,
                "win_rate": round(w / n, 4) if n else 0.0,
                "wilson95": [round(lo, 4), round(hi, 4)]}
