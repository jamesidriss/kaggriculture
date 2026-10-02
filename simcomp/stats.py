"""Statistics: Wilson intervals and a Bradley-Terry fitter.

Kept dependency-free so the harness can be lifted into another repo without
dragging in a numeric stack.
"""
import math


def wilson(w, n, z=1.96):
    """Wilson score interval for a binomial proportion.

    The only interval to use at the extremes. At 24/24 the Wald interval has
    zero width, which reports an undefeated record as a *proven* 100%. This
    returns a lower bound of 0.862 for 24/24, which is the honest statement.
    """
    if n == 0:
        return (0.0, 1.0)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def _bt_loglik(pairs, beta, teams):
    L = 0.0
    for (a, b), (wa, wb) in pairs.items():
        for t, o, w in ((a, b, wa), (b, a, wb)):
            d = beta[t] - beta[o]
            # log sigmoid(d), computed stably
            L += w * (-math.log1p(math.exp(-d)) if d >= 0
                      else d - math.log1p(math.exp(d)))
    return L


def _bt_grad(pairs, beta, teams):
    g = {t: 0.0 for t in teams}
    for (a, b), (wa, wb) in pairs.items():
        n = wa + wb
        for t, o, w in ((a, b, wa), (b, a, wb)):
            g[t] += w - n / (1.0 + math.exp(-(beta[t] - beta[o])))
    return g


def bradley_tery(pairs, iters=2000, tol=1e-8, require_convergence=True):
    """Fit BT strengths by maximum likelihood.

    pairs: {(a, b): (wins_a, wins_b)}. Ties should already be split 0.5/0.5.
    Returns {team: beta}, mean-centred so betas are comparable.

    Implemented as damped gradient ascent with a backtracking line search on the
    BT log-likelihood, which is log-concave, so this is a well-behaved convex
    problem. The textbook MM update is shorter but its denominator
    `sum_j (n_tj - w_tj/p_tj)` goes NEGATIVE for any lopsided record (e.g. 71%
    and 85% win rates at equal strengths), which silently freezes the iterate
    and returns a meaningless ranking. That failure is invisible unless you
    test the fitter against data generated from known strengths, which is why
    `selftest.py` does exactly that.

    A tournament that no set of strengths can reproduce (rock-paper-scissors, or
    any over-determined record) has no maximum here. That is a fact about the
    data, not a bug, so it is raised rather than papered over with whatever the
    last iterate happened to be.
    """
    teams = sorted({t for p in pairs for t in p})
    if not teams:
        return {}
    beta = {t: 0.0 for t in teams}
    L = _bt_loglik(pairs, beta, teams)
    converged = False
    for _ in range(iters):
        g = _bt_grad(pairs, beta, teams)
        gn = math.sqrt(sum(v * v for v in g.values()))
        if gn < tol:
            converged = True
            break
        step = 1.0
        improved = False
        for _ls in range(40):
            cand = {t: beta[t] + step * g[t] for t in teams}
            shift = sum(cand.values()) / len(teams)
            cand = {k: v - shift for k, v in cand.items()}   # re-centre
            Lc = _bt_loglik(pairs, cand, teams)
            if Lc > L:
                beta, L = cand, Lc
                improved = True
                break
            step /= 2.0
        if not improved:
            break                       # at a numerical optimum
    # Final re-centre so betas are comparable across fits.
    shift = sum(beta.values()) / len(beta)
    beta = {k: v - shift for k, v in beta.items()}
    if require_convergence and not converged:
        g = _bt_grad(pairs, beta, teams)
        gn = math.sqrt(sum(v * v for v in g.values()))
        if gn >= tol * 1e3:
            raise ValueError(
                f"Bradley-Terry did not reach a maximum likelihood (gradient "
                f"norm {gn:.2e}). The pairwise results are not reproducible by "
                f"any set of strengths -- typically a non-transitive or "
                f"over-determined record. Report the observed head-to-heads and "
                f"their intervals instead of a fitted ranking.")
    return beta


def fit_bt(pairs, **kw):
    """Non-raising variant. Returns (betas, converged: bool)."""
    try:
        return bradley_tery(pairs, **kw), True
    except ValueError:
        return bradley_tery(pairs, require_convergence=False, **kw), False


def p_win(beta, a, b):
    """Implied P(a beats b) from fitted betas."""
    return 1.0 / (1.0 + math.exp(-(beta[a] - beta[b])))
