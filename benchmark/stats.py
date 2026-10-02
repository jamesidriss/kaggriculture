"""Canonical statistics for the Kaggriculture audit. ONE implementation.

Corrected after discovering that the interval previously published for 76/144
as [0.3925, 0.5534] was computed on 68/144, not 76/144. The formula itself was
close to correct, but nothing in the repository validated it, and a
label/interval mismatch shipped in a report. Both problems are fixed here:

  1. `wilson()` is validated against an independent implementation and against
     closed-form expected values in the test suite.
  2. `win_interval(wins, losses, ties)` makes the win COUNT the single source
     of truth, so a reported rate and its interval cannot disagree.

Conventions used throughout this project, stated once:

  * An interval always describes a BINOMIAL proportion over DECIDED games:
    decided = wins + losses. Ties are excluded, never folded into wins,
    because a tie in this environment means identical final cash, which is a
    self-play/duplicate-content signal rather than a competitive outcome.
  * Offline win rate is NEVER a Kaggle rating and never a validation score.
    Those are different quantities and are labelled as such in every report.
"""
import math
import random

# Exact two-sided normal quantile for 95%, not the rounded 1.96.
Z95 = 1.959963984540054


# ---------------------------------------------------------------------------
# Wilson score interval
# ---------------------------------------------------------------------------
def wilson(wins, n, z=Z95):
    """Wilson score interval for a binomial proportion.

        p_hat = wins / n
        centre = (p_hat + z^2/(2n)) / (1 + z^2/n)
        half   = z/(1 + z^2/n) * sqrt(p_hat(1-p_hat)/n + z^2/(4n^2))
        CI     = centre +/- half

    Correct at the extremes, where the Wald interval collapses to zero width.
    For 0/n the upper bound is 1 - alpha^(2/n)-ish, never 1.0 by fiat, and for
    n/n the lower bound is never 1.0.

    Returns (lo, hi). n == 0 returns (0.0, 1.0): the interval for "no
    evidence" is the whole unit interval, not a zero-width point.
    """
    if n <= 0:
        return (0.0, 1.0)
    p = wins / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = (p + z2 / (2.0 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def win_interval(wins, losses, ties=0):
    """Canonical match metrics for a W/L/T record.

    THREE DISTINCT NUMBERS, never conflated. Confusing them is how a 18%-tie
    matchup came to be reported as an 80.9% "win rate":

      bt_score_rate  = (W + 0.5*T) / N      PRIMARY
          This is the competitive metric. Kaggle's final evaluation is a
          Bradley-Terry fit over episodes in which a draw scores 0.5 for each
          side, so the per-game score IS (1, 0.5, 0) and its sample mean is the
          number that belongs in a BT model. It is reported everywhere from now
          on and it is the promotion metric.

      decided_win_rate = W / (W+L)          SECONDARY DIAGNOSTIC
          Conditional on the game producing a winner. Useful for reading
          "when this matchup is decided, how often do I win", and it is the
          right denominator for McNemar and for a decided-only Wilson interval.
          It is NOT the match score and must never be labelled as one.

      tie_rate = T / N                      DIAGNOSTIC
          How often the matchup produced no winner at all. A high tie rate is
          itself a finding: it says the two policies behave identically on those
          worlds, which is information about mechanism rather than noise.

    The Wilson interval returned here is on the DECIDED-only rate, because a
    binomial interval is not the right uncertainty statement for a mean of
    per-game scores that can take the value 0.5. Use
    `bootstrap_score_interval` for the primary metric's uncertainty.
    """
    n = wins + losses + ties
    decided = wins + losses
    lo, hi = wilson(wins, decided)
    return {
        "W": wins, "L": losses, "T": ties,
        "games": n,
        "decided": decided,
        "bt_score_rate": ((wins + 0.5 * ties) / n) if n else 0.0,
        "win_rate": (wins / decided) if decided else 0.0,
        "decided_win_rate": (wins / decided) if decided else 0.0,
        "tie_rate": (ties / n) if n else 0.0,
        # Named explicitly so no caller can mistake which one it is quoting.
        "wilson_decided_lo": lo, "wilson_decided_hi": hi,
        "wilson_lo": lo, "wilson_hi": hi,
    }


def bt_score_rate(wins, losses, ties=0):
    """(W + 0.5*T) / (W + L + T). The primary competitive metric.

    Kaggle's final Bradley-Terry evaluation scores a draw as half a win for
    each side, so a per-game score of (1, 0.5, 0) is the correct observation
    and its mean is the BT score rate.
    """
    n = wins + losses + ties
    return ((wins + 0.5 * ties) / n) if n else 0.0


def wilson_decided(wins, losses):
    """Wilson interval on the decided-only rate. Secondary diagnostic only."""
    return wilson(wins, wins + losses)


def bootstrap_score_interval(game_scores, iters=20000, seed=20261002,
                             alpha=0.05):
    """Percentile bootstrap CI for the mean of per-game scores.

    `game_scores` is a sequence of per-game values in [0, 1] -- 1 win,
    0.5 tie, 0 loss. The mean is the BT score rate, and the bootstrap is the
    right uncertainty statement for it: the observations are bounded, discrete
    and the distribution is not binomial, so a normal-approximation interval on
    the mean would be wrong.

    Uses the BCa-free percentile method, which is adequate at these sample
    sizes and has no tuning constant to overfit.
    """
    import random
    xs = list(game_scores)
    n = len(xs)
    if n == 0:
        return (0.0, 0.0, 0.0, 0)
    rng = random.Random(seed)
    mean = sum(xs) / n
    if n == 1:
        return (mean, mean, mean, 1)
    means = []
    for _ in range(iters):
        s = 0.0
        for _ in range(n):
            s += xs[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo_i = int((alpha / 2) * iters)
    hi_i = min(iters - 1, int((1 - alpha / 2) * iters))
    return (mean, means[lo_i], means[hi_i], n)


def paired_seed_bootstrap(per_seed_scores, iters=20000, seed=20261002,
                          alpha=0.05):
    """Bootstrap the BT score rate resampling SEEDS, not individual games.

    In a paired both-seat experiment the two games from one world share the
    world and therefore share the opponent's behaviour and the market state.
    They are correlated observations, and resampling them independently
    understates the interval. The correct resampling unit is the seed.

    `per_seed_scores` maps seed -> list of per-game scores for that seed
    (normally two: one per seat). Returns (mean, lo, hi, n_seeds).
    """
    keys = list(per_seed_scores)
    if not keys:
        return (0.0, 0.0, 0.0, 0)
    rng = random.Random(seed)
    k = len(keys)
    flat_mean = (sum(sum(v) for v in per_seed_scores.values())
                 / max(1, sum(len(v) for v in per_seed_scores.values())))
    if k == 1:
        return (flat_mean, flat_mean, flat_mean, 1)
    means = []
    for _ in range(iters):
        s = 0.0
        c = 0
        for _ in range(k):
            v = per_seed_scores[keys[rng.randrange(k)]]
            s += sum(v)
            c += len(v)
        means.append(s / c)
    means.sort()
    lo_i = int((alpha / 2) * iters)
    hi_i = min(iters - 1, int((1 - alpha / 2) * iters))
    return (flat_mean, means[lo_i], means[hi_i], k)


def lineage_balanced_score(matchups):
    """Aggregate a candidate's score with each LINEAGE weighted equally.

    `matchups` is a list of dicts with keys: `lineage_id`, `W`, `L`, `T`.

    Why this exists: the league is lineage-concentrated. Nine of the twelve
    known artifacts are variants from one author, so an unweighted mean over
    matchups lets a single lineage decide the fitness function, and a
    candidate can look strong by being good against its own relatives. Equal
    weight per lineage removes that: variants are averaged WITHIN a lineage
    first, then the lineages are averaged, so adding a seventh variant of an
    already-represented strategy changes nothing.

    Also returns the worst lineage, because a mean hides a collapse.
    """
    per = {}
    for m in matchups:
        li = m["lineage_id"]
        n = m["W"] + m["L"] + m["T"]
        if n == 0:
            continue
        per.setdefault(li, []).append(
            (m["W"] + 0.5 * m["T"]) / n)
    if not per:
        return {"score": 0.0, "worst_lineage": None, "worst_score": 0.0,
                "n_lineages": 0, "per_lineage": {}}
    lin = {k: sum(v) / len(v) for k, v in per.items()}
    worst = min(lin, key=lambda k: lin[k])
    return {"score": sum(lin.values()) / len(lin),
            "worst_lineage": worst, "worst_score": lin[worst],
            "n_lineages": len(lin), "per_lineage": lin}


def mcnemar_exact(b, c):
    """Exact two-sided McNemar test on discordant pairs.

    b = A wins while B wins in the paired game; c = the reverse. Only the
    discordant pairs carry information, so the test conditions on b + c.
    Returns (two_sided_p, n_discordant).

    Computed in log space: `2.0 ** n` overflows a float for n > 1023, and
    `math.comb` then cannot be converted, so both are done with lgamma.
    """
    n = b + c
    if n == 0:
        return (1.0, 0)
    k = min(b, c)
    lgn = math.lgamma(n + 1)
    # Divide by 2^n inside the exponent: `2.0 ** n` overflows for n > 1023.
    tail = sum(math.exp(lgn - math.lgamma(i + 1) - math.lgamma(n - i + 1)
                        - n * math.log(2.0)) for i in range(0, k + 1))
    return (min(1.0, 2.0 * tail), n)


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial test against p (default 0.5).

    Computed in log space via lgamma: `math.comb(1984, 992)` is a 600-digit
    integer and converting it to float overflows. Summing the log-pmbs keeps
    the result exact to float precision.
    """
    if n <= 0:
        return 1.0

    def logpmf(i):
        if p == 0.0:
            return 0.0 if i == 0 else -math.inf
        if p == 1.0:
            return 0.0 if i == n else -math.inf
        if (p == 0.5 and (i == 0 or i == n)) or (0 < i < n):
            return (math.lgamma(n + 1) - math.lgamma(i + 1)
                    - math.lgamma(n - i + 1)
                    + i * math.log(p) + (n - i) * math.log1p(-p))
        return -math.inf

    obs = logpmf(k)
    total = 0.0
    for i in range(n + 1):
        li = logpmf(i)
        if li == -math.inf:
            continue
        if li <= obs + 1e-9:
            total += math.exp(li)
    return min(1.0, total)


def paired_bootstrap_ci(pairs, iters=20000, seed=20261002, alpha=0.05):
    """Bootstrap CI for the mean paired margin (A cash - B cash).

    `pairs` is a list of per-seed margins. Resampling SEEDS (not games)
    respects the paired design, because both seats of a world share one seed.
    """
    if not pairs:
        return (0.0, 0.0, 0.0)
    rng = random.Random(seed)
    m = len(pairs)
    means = []
    for _ in range(iters):
        s = 0.0
        for _ in range(m):
            s += pairs[rng.randrange(m)]
        means.append(s / m)
    means.sort()
    lo = means[int(alpha / 2 * iters)]
    hi = means[min(iters - 1, int((1 - alpha / 2) * iters))]
    return (sum(pairs) / m, lo, hi)


# ---------------------------------------------------------------------------
# Paired seat design
# ---------------------------------------------------------------------------
def paired_design(seeds):
    """The canonical schedule: every world played from BOTH seats.

    Yields (seed, candidate_seat) for each seed, in a stable order. Using this
    instead of ad-hoc loops is what guarantees a paired, both-seat comparison.
    """
    for s in seeds:
        for seat in (0, 1):
            yield s, seat


# ---------------------------------------------------------------------------
# Bradley-Terry
# ---------------------------------------------------------------------------
def bt_identifiability(pairs, teams=None):
    """Decide whether a BT maximum likelihood exists and is finite.

    Returns a dict with:
      ok            - a finite MLE exists
      zero_win      - teams with 0 wins against every opponent (MLE = -inf)
      zero_loss     - teams with 0 losses (MLE = +inf)
      disconnected  - True if the comparison graph is not strongly connected
      isolated      - teams absent from `pairs`
      complete_separation - pairs that are 100-0, which are themselves
                    sufficient to make the extreme betas diverge

    A BT ranking must NOT be published unless ok is True. Use
    `bradley_tery_regularized` and label the result REGULARIZED BT.
    """
    if teams is None:
        teams = sorted({t for p in pairs for t in p})
    w = {t: 0 for t in teams}
    l = {t: 0 for t in teams}
    adj = {t: set() for t in teams}
    for (a, b), (wa, wb) in pairs.items():
        w[a] += wa; l[a] += wb
        w[b] += wb; l[b] += wa
        adj[a].add(b); adj[b].add(a)
    zero_win = [t for t in teams if w[t] == 0 and (w[t] + l[t]) > 0]
    zero_loss = [t for t in teams if l[t] == 0 and (w[t] + l[t]) > 0]
    isolated = [t for t in teams if not adj[t]]
    sep = [f"{a} vs {b} {wa}-{wb}" for (a, b), (wa, wb) in pairs.items()
           if wa + wb > 0 and (wa == 0 or wb == 0)]
    # strong connectivity via BFS from an arbitrary node
    seen, stack = set(), [teams[0]] if teams else []
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj[n] - seen)
    disconnected = len(seen) != len(teams)
    return {
        "ok": not (zero_win or zero_loss or isolated or disconnected),
        "zero_win": zero_win, "zero_loss": zero_loss,
        "isolated": isolated, "disconnected": disconnected,
        "complete_separation": sep,
        "strong_component_size": len(seen),
        "teams": len(teams),
    }


def bradley_tery_regularized(pairs, prior_sd=1.0, iters=20000, tol=1e-10):
    """MAP Bradley-Terry with a Normal(0, prior_sd) prior on the betas.

    REQUIRED whenever the plain MLE is unbounded, and any result from this
    function must be published as **REGULARIZED BT**, never as plain MLE. The
    prior is what makes a finite optimum exist when an agent wins or loses
    every game: the log-posterior has a unique finite maximum because the
    Gaussian prior penalises large |beta|.

    The penalty shrinks all betas toward 0 by a data-dependent amount, so
    absolute values are NOT comparable with an MLE fit and the spread is
    compressed. Only the ordering, and the pairwise implied probabilities, are
    meaningful. This is why the observed head-to-heads remain the primary
    evidence.
    """
    teams = sorted({t for p in pairs for t in p})
    if not teams:
        return {}
    beta = {t: 0.0 for t in teams}
    lam = 1.0 / (prior_sd * prior_sd)
    for _ in range(iters):
        g = {t: -lam * beta[t] for t in teams}
        for (a, b), (wa, wb) in pairs.items():
            n = wa + wb
            if n == 0:
                continue
            for t, o, win in ((a, b, wa), (b, a, wb)):
                g[t] += win - n / (1.0 + math.exp(-(beta[t] - beta[o])))
        step = 1.0
        moved = False
        cur = _bt_loglik(pairs, beta) - 0.5 * lam * sum(v * v for v in beta.values())
        for _ls in range(50):
            cand = {t: beta[t] + step * g[t] for t in teams}
            sh = sum(cand.values()) / len(cand)
            cand = {k: v - sh for k, v in cand.items()}
            newL = (_bt_loglik(pairs, cand)
                    - 0.5 * lam * sum(v * v for v in cand.values()))
            if newL > cur + 1e-15:
                delta = max(abs(cand[t] - beta[t]) for t in teams)
                beta = cand
                moved = True
                if delta < tol:
                    break
                break
            step /= 2.0
        if not moved or delta < tol:
            break
    sh = sum(beta.values()) / len(beta)
    return {k: v - sh for k, v in beta.items()}


def bradley_tery(pairs, iters=20000, tol=1e-10, require_finite=True):
    """Maximum-likelihood BT strengths by damped gradient ascent.

    Ties must already be split 0.5/0.5 by the caller, and ties are excluded
    from competitive metrics entirely, so this sees only decisive pairs.

    Convergence is declared on the CHANGE IN BETAS, not on the gradient norm.
    Real head-to-head data are integers, so a synthetic-but-realistic record
    is very slightly inconsistent with any exact set of strengths and the
    gradient then asymptotes to a small non-zero value; demanding a gradient
    below 1e-9 would report "no MLE" for perfectly ordinary data.

    Raises ValueError when the MLE is unbounded or unattainable, so an
    unconverged or infinite solution can never be printed as a ranking.
    """
    ident = bt_identifiability(pairs)
    if require_finite and not ident["ok"]:
        raise ValueError(
            "Bradley-Terry is not identifiable for this result set. "
            f"zero-win (MLE = -inf): {ident['zero_win']}; "
            f"zero-loss (MLE = +inf): {ident['zero_loss']}; "
            f"isolated: {ident['isolated']}; disconnected: {ident['disconnected']}. "
            "Collect cross-tier matches before fitting, or publish a clearly "
            "labelled REGULARIZED BT model instead. Do not print betas here.")
    teams = sorted({t for p in pairs for t in p})
    if not teams:
        return {}
    beta = {t: 0.0 for t in teams}
    converged = False
    for _ in range(iters):
        g = {t: 0.0 for t in teams}
        for (a, b), (wa, wb) in pairs.items():
            n = wa + wb
            if n == 0:
                continue
            for t, o, win in ((a, b, wa), (b, a, wb)):
                g[t] += win - n / (1.0 + math.exp(-(beta[t] - beta[o])))
        step = 1.0
        moved = False
        for _ls in range(50):
            cand = {t: beta[t] + step * g[t] for t in teams}
            sh = sum(cand.values()) / len(cand)
            cand = {k: v - sh for k, v in cand.items()}
            if _bt_loglik(pairs, cand) > _bt_loglik(pairs, beta) + 1e-15:
                delta = max(abs(cand[t] - beta[t]) for t in teams)
                beta = cand
                moved = True
                if delta < tol:
                    converged = True
                break
            step /= 2.0
        if converged or not moved:
            converged = converged or not moved
            break
    sh = sum(beta.values()) / len(beta)
    beta = {k: v - sh for k, v in beta.items()}
    if require_finite and not converged:
        raise ValueError(
            "Bradley-Terry did not reach a finite maximum. The pairwise results "
            "contain a cycle that no set of strengths reproduces. Report the "
            "observed head-to-heads and their intervals instead.")
    return beta


def _bt_loglik(pairs, beta):
    L = 0.0
    for (a, b), (wa, wb) in pairs.items():
        for t, o, w in ((a, b, wa), (b, a, wb)):
            d = beta[t] - beta[o]
            L += w * (-math.log1p(math.exp(-d)) if d >= 0
                      else d - math.log1p(math.exp(d)))
    return L


def bt_implied_p(beta, a, b):
    return 1.0 / (1.0 + math.exp(-(beta[a] - beta[b])))


# ---------------------------------------------------------------------------
# Independent cross-check
# ---------------------------------------------------------------------------
def wilson_reference(wins, n):
    """Deliberately independent formulation, used only to cross-check `wilson`.

    Written from the definition (invert the score test) with a different code
    path, so an algebra slip in `wilson` cannot hide.
    """
    if n <= 0:
        return (0.0, 1.0)
    p = wins / n
    z2 = Z95 * Z95
    # Solve (p - p0)^2 <= z2 p0 (1-p0)/n for p0 by the quadratic formula.
    # (1 + z2/n) p0^2 - (2p + z2/n) p0 + p^2 <= 0
    A = 1.0 + z2 / n
    B = -(2.0 * p + z2 / n)
    C = p * p
    disc = B * B - 4.0 * A * C
    if disc < 0:
        return (0.0, 1.0)
    sq = math.sqrt(disc)
    return (max(0.0, (-B - sq) / (2.0 * A)), min(1.0, (-B + sq) / (2.0 * A)))
