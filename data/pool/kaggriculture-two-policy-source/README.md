# Kaggriculture: Observed Production and Last Dance

Two independent Python policies for Kaggriculture's 720-step farming economy. They share a licensed production and market lineage, but address different decisions: **Observed Production** selects between isolated production experts; **Last Dance** adjusts wheat trading and defensive responses to observed market flow. They are not an ensemble, and the package does not combine them into a new policy.

## Implementations

| Policy | Source entry | Reference artifact | Additional assets |
|---|---|---|---|
| Observed Production | `policies/observed_56713902.py` | 56713902 | Shared upstream output; authorized 24-episode task library |
| Last Dance | `policies/last_dance_56720309.py` | 56720309 | Shared upstream output |

The IDs identify the implementations, not their rank. No final competition score is claimed.

### Observed Production

Both experts receive the actual opening observations in separate namespaces. A common two-step purchase sequence preserves the ability to choose either expert. At step 2, the policy selects its learned production branch when the rival has at least five hands and its farmer remains at its initial position; otherwise it uses the mature expert. This is a compact public-state rule, not opponent identification or a learned classifier.

The first day's actor roles are translated to the actual deployment. Two workers exchange construction and placement duties only when their positions and carried inventories agree. This respects the engine's unit execution order without adding an early hire. The translation ends at the daily reset.

The production branch uses reference task intents with live-state preconditions and movement repair. Its project selector combines an empirical return table with a neural fallback. The exported model includes 98-dimensional normalization, three network members and a four-option prior. Supported table entries use count-shrunk return estimates; sparsely supported contexts defer to the neural selector. This is policy improvement over executable options, not end-to-end control of every action.

### Last Dance

The production controller is retained while the market layer tracks realized transactions. Public inventory changes, known town demand and the policy's own orders provide information about rival wheat flow. The policy sizes simultaneous carry positions with a per-unit clearing model, recognizes adverse timing patterns, and settles outstanding positions before standing down.

The final implementation adds execution-cost lower bounds, separate accounting for counter-inventory, phase-aware responses, realized-loss detection and a bounded probation period. Estimated current-quote risk and realized losses remain distinct. Repeated adverse evidence can disable new carry orders for the episode. These mechanisms are heuristic control and bounded enumeration; no RL training claim is made for this branch.

## Inputs and outputs

Each entry accepts `observation` and optional `configuration`. Observations contain the current step, player index, public farms and town/market state, plus the player's private inventory. The result is a dictionary containing `farmer`, `hands` and `market`. The original insertion-order entry point is preserved by `publication_assets.load_policy`; an intermediate function named `agent` is not necessarily the outermost policy.

Policy execution uses Python's standard library. Run each game with fresh policy namespaces. Do not reuse stateful policy objects across simultaneous games or swap an expert into an episode without its initialization history.

## Run

Python 3.11 or 3.12 is recommended. For official-engine evaluation, use `kaggle-environments==1.32.7`. The companion Kaggle notebook attaches this code dataset and the upstream notebook output; it reads no competition dataset files. No GPU is needed.

Locally, first obtain the upstream output through its original Kaggle page or CLI:

```sh
kaggle kernels output degnonguidi/best-agent-ranking -p upstream
export KAGGRICULTURE_UPSTREAM_MAIN="$PWD/upstream/main.py"
```

From the extracted code directory:

```python
from publication_assets import load_policy
policy = load_policy('last_dance_56720309')
action = policy(observation, configuration)
```

For Observed Production, follow `DATA_ACCESS.md` before loading `observed_56713902`. Its task library is a required dependency, not an optional accuracy improvement. Missing assets produce an explicit error; there is no silent fallback to another agent.

```sh
python extract_task_library.py /authorized/observed/main.py /private/task_library.json
export KAGGRICULTURE_PRIVATE_ASSETS=/private/task_library.json
```

The `/authorized` and `/private` paths above are placeholders to replace locally, not directories created by the notebook.

## Training and evaluation scope

The released neural weights and empirical statistics support inference without retraining. Their development used simulated counterfactual continuations and world-separated evaluation. The full historical training corpus and training pipeline are not included; this is an inference/source release, not a from-scratch training reproduction.

An archived local comparison covered 16 worlds, two seats and 16 executable-program or reconstructed-plan opponents: Observed Production won 475/512 versus 451/512 for its mature reference, with 30 recovered losses and six newly lost games. The 512 contexts contain only 16 independent worlds; reconstructed plans do not reproduce private opponents' reactions. Those results neither measure Last Dance nor establish current leaderboard strength.

Publication checks compared each reorganized implementation with its original payload throughout complete games at seed 20261002 in both seats. Across six distinct policy/opponent/seat paths, including an Observed self-play path that selects the learned branch, all 4,314 corresponding decisions matched. This verifies the source/asset separation on those paths, not every branch or environment. The companion notebook separately runs an official-engine Last Dance smoke game and records its installed engine version. An engine smoke game is not a competitive benchmark.

## Limits

Reference task libraries constrain the production branch's option space. Public opening features are imperfect predictors of later opponent behavior. Market-flow estimates can be confounded by simultaneous orders and changing production. More elaborate selection does not remove those limitations. Reusing a strong schedule is useful, but does not recover its author's full adaptive policy.

## License and credit

Code and original model parameters are provided under Apache-2.0. See `LICENSE.txt`, `NOTICE_56713902.txt`, `NOTICE_56720309.txt` and the attribution comments within the readable sources. The release retains contributions credited to thomastschinkel, Yusuke Hayashi/yhay81, destbreso, aurax7, tetsutani, prvsiyan, Dmitrii Gluzdov, Ahmed Berat Ozer, Steven Lee Hans, Seyit Kaan Gunes, flexonafft, renji_starfall/shiiin9 and Kaggle/kaggle-environments contributors. Attribution does not imply endorsement.

Public dependencies: [upstream market/production notebook](https://www.kaggle.com/code/degnonguidi/best-agent-ranking), [Frontier lineage](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-soil-remembers-rain), [multi-route execution lineage](https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent), and [official engine](https://github.com/Kaggle/kaggle-environments).

The code license does not grant rights to redistribute competition replay data. Access dependencies through their original sources and applicable terms.
