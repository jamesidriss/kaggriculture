"""Statistics for the Kaggriculture benchmark scripts.

Thin re-export of `simcomp.stats` so that there is exactly ONE implementation of
`wilson` and `bradley_tery` in the repository. Two copies of a statistical
primitive is how two reports end up quoting different intervals for the same
record; an earlier version of this file also returned a nonsensical (0.0, 0.0)
for n == 0, i.e. a zero-width interval claiming certainty about nothing.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simcomp.stats import wilson, bradley_tery, p_win  # noqa: F401,E402

__all__ = ["wilson", "bradley_tery", "p_win"]
