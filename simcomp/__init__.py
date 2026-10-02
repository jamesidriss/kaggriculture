"""simcomp — a reusable harness for Kaggle environment agent competitions.

Extracted from the Kaggriculture audit because the things that made that audit
trustworthy are not Kaggriculture-specific: content-digest identity, licence
gating, sealed seed splits, paired both-seat evaluation through the framework's
own delivery path, Wilson intervals, and a test suite that fails when any of
those are bypassed.

Environment-specific policy (seed sources, what counts as a legal artifact)
lives in a JSON config next to this file. Everything else is generic.

    from simcomp import Registry, SeedSplits, League

    reg = Registry("simcomp/config/kaggriculture.json")
    reg.verify()                                  # digests, licences, provenance
    splits = SeedSplits("seeds")                 # sealed dev/holdout/final
    res = League(reg).run("v51", pool="dev")     # official env.run, both seats
    res.assert_clean()                            # no errors, no self-play ties
    res.assert_discriminating()                   # a sweep is an error, not a win

Design rules learned the hard way, encoded here so they are not re-learned:

  1. Identity is the content digest, never a filename or a label. The same
     agent is called `v51` as a candidate and `ahmedberatozer-v51-lean-flock`
     as an opponent; keying on labels splits one agent in two.
  2. Agents are driven by the environment's own `run()`. Feeding an agent from
     `env.steps[i][seat].observation` drops shared fields for seat 1 and
     manufactures crashes that cannot happen on the real server.
  3. A sweep is a measurement failure, not a result. `assert_discriminating`
     exists to make that an error.
  4. Never report a proportion without an interval, and never report an
     undefeated record as 100%.
"""
# Import order matters. `league` and `parity` both depend on `stats`; pulling a
# submodule in while this package __init__ is still executing leaves it
# half-initialised, and a later `from .stats import ...` then fails with a
# misleading "cannot import name" for a name that plainly exists in the file.
from . import stats as _stats  # noqa: F401
from .registry import Registry, Agent
from .seeds import SeedSplits
from .stats import wilson, bradley_tery, p_win
from .league import League, Result
from .parity import assert_shared_delivery, assert_both_seats

__all__ = [
    "Registry", "Agent", "SeedSplits", "League", "Result",
    "wilson", "bradley_tery", "p_win",
    "assert_shared_delivery", "assert_both_seats",
]

__version__ = "1.0.0"
