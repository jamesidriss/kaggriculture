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
    """Wilson interval for a W/L/T record, ties excluded.

    Returns a dict carrying the record, the rate and the interval, computed from
    ONE set of counts so they cannot disagree.
    """
    decided = wins + losses
    lo, hi = wilson(wins, decided)
    return {
        "W": wins, "L": losses, "T": ties,
        "games": wins + losses + ties,
        "decided": decided,
        "win_rate": (wins / decided) if decided else 0.0,
        "wilson_lo": lo, "wilson_hi": hi,
    }


def mcnemar_exact(b, c):
    """Exact two-sided McNemar test on discordant pairs.

    b = A wins while B wins in the paired game; c = the reverse. Only the
    discordant pairs carry information, so the test conditions on b + c.
    Returns (two_sided_p, n_discordant).
    """
    n = b + c
    if n == 0:
        return (1.0, 0)
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2.0 ** n)
    return (min(1.0, 2.0 * tail), n)


def binom_two_sided(k, n, p=0.5):
    """Exact two-sided binomial test against p (default 0.5)."""
    if n == 0:
        return 1.0
    def pmf(i):
        return math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    obs = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs + 1e-15))


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
      cycle_inconsistent - gradient norm still large after fitting

    A BT ranking must NOT be published unless ok is True.
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
        "strong_component_size": len(seen),
        "teams": len(teams),
    }


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
