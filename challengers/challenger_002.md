# challenger_002 — `terminal_liquidation` False → True

H1 sale timing, endgame lever. Off in the live config. If switching it ON helps, unsold shed stock is worth more converted at step >= 718, which is precisely where 59% of top-two games are decided.

- parent: `ahmedberatozer-v51-lean-flock` `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
- change: **one** value in the live `_SETTINGS` dict, verified to occur exactly once
- challenger sha256: `f5c254f9598af0a6bb358f7bf41936ef96d12c0b4090a936e600aa7ee20970d0`
- screening: `experiments/challenger_screen.csv`
- promotion: requires improvement against BOTH v51 and the 2945 Farm on a large paired sample. A screening sample cannot resolve a 2-point effect, so no promotion is granted on screening alone.
