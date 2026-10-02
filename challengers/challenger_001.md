# challenger_001 — `sell_lead` True → False

H1 sale timing, primary lever. sell_lead is the only market layer the agent actually runs. If switching it OFF helps, the agent is leading its own sales into its own competition and the missing piece is a proper market-order model rather than a one-turn lead.

- parent: `ahmedberatozer-v51-lean-flock` `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
- change: **one** value in the live `_SETTINGS` dict, verified to occur exactly once
- challenger sha256: `2d5d98c93b6fbe93469047c3fe848576488eacbabfd4c30fdfabbf5525df51bb`
- screening: `experiments/challenger_screen.csv`
- promotion: requires improvement against BOTH v51 and the 2945 Farm on a large paired sample. A screening sample cannot resolve a 2-point effect, so no promotion is granted on screening alone.
