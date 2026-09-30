# Third-Party Code and Licences

## Environment

- **Name:** `kaggle-environments`
- **Source:** https://github.com/Kaggle/kaggle-environments
- **Licence:** Apache-2.0
- **Version used:** 1.32.7
- **Use:** the official `kaggriculture` environment, used unmodified for all
  local simulation, evaluation and metrics.
- **Derivation:** none. No environment source was copied or modified.

## Constants mirrored into `main.py`

`main.py` re-declares a small number of numeric constants from
`kaggle_environments/envs/kaggriculture/kaggriculture.py` (CROPS, MARKET_PARAMS,
LAND_PRICES, the `_shape` price functions, `SHED_CAPACITY`, `MAX_MARKET_ORDERS`).
This is re-declaration of game data so the agent can compute sale prices locally
without importing the environment inside the submission sandbox. The logic is
Apache-2.0 licensed upstream; the values below are game parameters, not
copyrightable expression, and they are reproduced verbatim so the agent's price
predictions match the environment exactly.

Licensed under Apache-2.0. No environment source file was vendored into this
repository.

## Built-in agents

`pass`, `random` and `starter` ship with the official environment and are used
only as smoke-test opponents. No environment file was copied.

## Opponent league (`opponents/league.py`)

Original work for this project. Written from the published rules in
`research/README.md` to provide strategy diversity during local evaluation.
Not derived from any third-party agent.

## Rejected third-party agents

No public Kaggriculture agent source was copied into this repository. The
baseline was chosen as the official `starter` carrot loop described in the
competition's own `AGENTS.md`, implemented locally in the evaluation harness.
An early goose/livestock pipeline was drafted from the official rules and then
reverted on measured evidence (see `experiments/EXPERIMENTS.csv`, E007);
no third-party code was involved.

## Verbatim competition documentation

`research/README.md` and `research/AGENTS.md` are the official competition
documentation files as distributed by Kaggle. They are byte-identical to the
copies shipped inside `kaggle-environments` 1.32.7 and are retained here as the
auditable rules reference for the run.