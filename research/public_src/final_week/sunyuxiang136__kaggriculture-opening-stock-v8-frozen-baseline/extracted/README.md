# Kaggriculture Opening Stock V8 — Frozen Baseline

I am sharing an older frozen version of my Kaggriculture agent as a reproducible baseline for studying inventory management, execution, and market timing. This is a historical release, not my latest competitive version.

The agent builds on the attributed public Tetsutani and community route-policy lineage. My V8 additions focus on keeping useful wheat as feed, reconciling planned sales with executable actions, preserving payroll, and repairing execution at the end of the game. It also contains the frozen local supervised/fitted-Q market model used in that version.

## What is included

- `main.py`: the original self-contained V8 agent, byte for byte.
- `submission.tar.gz`: `main.py`, `LICENSE.txt`, and `NOTICE.txt`, ready to upload to Kaggriculture.
- `opening_stock_v8_source.zip`: the source, documentation, exporter, and readable embedded modules.
- `readable/base_policy.py`, `readable/guard_policy.py`, and `readable/embedded_*.py`: exact decoded source strings for inspection. These are reference copies; `main.py` is the executable entrypoint.
- `SOURCE_MANIFEST.json`: SHA256 hashes for the distributed files.

The agent itself uses only the Python standard library. The notebook uses IPython to write the files and display download links. Running the notebook creates the source bundle and submission archive without network access or model training.

Kaggle limits uploaded notebook source to 1 MB. The 1.4 MB agent is therefore transported as a zlib/Base85 payload with a mandatory SHA256 check. The resulting `main.py` and readable sources are complete, inspectable text files; the encoding does not alter the strategy.

## Main ideas

1. **Keep useful opening stock.** At the temporary wheat delivery, omit an optional extra sale when the visible wheat quote is below 31. The retained wheat remains available for feed or later decisions.
2. **Reconcile sale feedback.** Update the inherited sale bookkeeping when the outer controller changes the executable action, avoiding mismatches between intended and actual inventory movements.
3. **Protect execution.** Preserve payroll where the guard applies, repair feasible production and delivery actions, and use the bounded terminal planner. Repeated calls for the same step return independent action copies.
4. **Use bounded market decisions.** A frozen offline model evaluates small observed-state sale adjustments with deadlines for deferred sales. It is not trained during a match.

## Run and submit

Run the Kaggle notebook from top to bottom, then download `submission.tar.gz` from Output. You can also download and inspect the source ZIP. The release identity is:

```text
main.py SHA256
d760ace37153218546ef8219db4de5ea93f69e70c48b573cc37ee000f3e0228d
```

The archive is repackaged with explicit license and attribution files; the strategy source is unchanged. In a local checkout containing the release files, `python export_v8.py` regenerates the archives. Verify the printed source hash before comparing variants.

## Limits and an experiment to try

This is an older baseline, with no claim of a current leaderboard rating or guaranteed wins. Inventory forecasts and the short-horizon market model can be wrong, and passing a loading check does not establish competitive strength.

A useful experiment is to compare the visible-price wheat-retention rule with an ablation on identical scenarios, both player seats, and several live responsive opponents. Record wins, losses, ties, final cash margin, and previously winning games that become losses. Keep new confirmation scenarios separate from development scenarios.

## Attribution and license

Apache License 2.0. This is a derivative of public community work, not a from-scratch policy. All inherited notices remain in `main.py` and its readable extracted sources. See `NOTICE.txt` for the exact parent source and local modifications, and `LICENSE.txt` for the license.

Primary upstream notebook: https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing

Thanks to the upstream authors for sharing their work. Reuse and improvements are welcome with the required attribution and license notices preserved.
