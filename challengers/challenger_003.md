# challenger_003 — `clamp_sells` False → True

H1 sale sizing. Off in the live config. If clamping helps, the agent is overselling into a thin market and losing price on volume.

- parent: `ahmedberatozer-v51-lean-flock` `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
- change: **one** value in the live `_SETTINGS` dict, verified to occur exactly once
- challenger sha256: `259fb772ee0547ed1f2a29b2752b9d1064aed9ff885b028341414e5d8945fcba`
- screening: `experiments/challenger_screen.csv`
- promotion: requires improvement against BOTH v51 and the 2945 Farm on a large paired sample. A screening sample cannot resolve a 2-point effect, so no promotion is granted on screening alone.
