"""Shared statistics for the Kaggriculture evaluation harness.

`wilson` previously had two independent copies (benchmark/meta.py and
benchmark/real_strength.py). Two copies of a statistical primitive is how two
reports end up quoting slightly different intervals for the same record. One
definition, imported everywhere.
"""
import math


def wilson(w, n, z=1.96):
    """Wilson score interval for a binomial proportion.

    Correct where the normal approximation is not: at 0/24 or 24/24 the
    Wald interval collapses to zero width, which would let an undefeated record
    be reported as a proven 100%. Returns (lo, hi).
    """
    if n == 0:
        return (0.0, 1.0)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))
