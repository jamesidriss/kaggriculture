"""simcomp — a reusable harness for Kaggle environment agent competitions.

Extracted from the Kaggriculture audit. Everything environment-specific lives in
`simcomp/config/*.json`; everything else is generic.

    from simcomp import Registry, SeedSplits, League

    reg = Registry("simcomp/config/kaggriculture.json")
    reg.verify()                                  # digests, licences, provenance
    res = League(reg).play(a_path, b_path, seed, cand_seat=0)
    res.assert_clean()                            # both played, no tie
    res.assert_discriminating()                   # a sweep is an error, not a win

The rules this encodes, each of which cost a wrong conclusion to learn:

  1. Identity is the content digest, never a filename or a label. The same agent
     is `v51` as a candidate and `ahmedberatozer-v51-lean-flock` as an opponent;
     keying on labels splits one agent in two.
  2. Drive agents through the environment's own `run()`. Feeding an agent from
     `env.steps[i][seat].observation` drops shared fields for seat 1 and
     manufactures a KeyError that cannot occur on the real server.
  3. Never invoke an agent directly. The framework truncates the argument list
     to `co_argcount`, so both `agent(obs)` and `agent(obs, configuration)` are
     legal; calling `fn(obs, configuration)` yourself is not.
  4. A sweep is a measurement failure, not a result.
  5. Assert on the side effects an agent produces — invocations, exceptions,
     status, action trace — not on the absence of an error code. An agent that
     raises inside `env.run()` yields a perfectly green result.
  6. Never report a proportion without an interval, and never report an
     undefeated record as 100%.
  7. Do not fit a model that will not converge. If Bradley-Terry is unbounded,
     say so; a truncated iteration is not a ranking.
  8. Content-addressed files must not be rewritten by the VCS. A CRLF checkout
     changes the digest of every artifact in the project.

Component map
-------------
registry.py  digest-addressed identity, licence + provenance gating
seeds.py     sealed dev/holdout/final splits, disjointness assertions
league.py    paired both-seat runner, validity gates, self-play refusal
stats.py     Wilson (cross-validated), exact binomial, McNemar, bootstrap,
             Bradley-Terry with an identifiability gate and a labelled
             regularized variant
parity.py    shared-field delivery proof, snapshot-divergence demonstration
selftest.py  self-test; exercises every guard including the two that caught
             real bugs during development
"""
from . import stats as _stats
from .registry import Registry, Agent
from .seeds import SeedSplits
from .stats import (wilson, bradley_tery, bradley_tery_regularized,  # noqa: F401
                    bt_identifiability, binom_two_sided, mcnemar_exact,
                    paired_bootstrap_ci, win_interval)
from .league import League, Result
from .parity import (assert_shared_delivery, assert_both_seats,  # noqa: F401
                     snapshot_divergence, runtime_info)

__all__ = [
    "Registry", "Agent", "SeedSplits", "League", "Result",
    "wilson", "bradley_tery", "bradley_tery_regularized", "bt_identifiability",
    "binom_two_sided", "mcnemar_exact", "paired_bootstrap_ci", "win_interval",
    "assert_shared_delivery", "assert_both_seats", "snapshot_divergence",
    "runtime_info",
]

__version__ = "1.1.0"
