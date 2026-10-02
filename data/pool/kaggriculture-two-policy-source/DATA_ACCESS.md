# Data access and reproducibility

## Included

Readable policy code for both implementations; exported neural parameters and aggregated simulated-return statistics; original optimized closing schedules; dependency lookup code; license and attribution notices. The public package contains no raw competition replay files, private credentials, or archived user conversations.

`policy_parameters.json` is a runtime parameter container. Numeric tables retain their original Python literal types through `ast.literal_eval`; no text from it is executed as Python code. The separately stored Python source modules retain the policy's original `exec`-based isolation, so source dependencies must be trusted code.

## Upstream dependency

Attach `degnonguidi/best-agent-ranking` as a Kaggle Notebook input. Its output `main.py` supplies the inherited route and forecast constants. They are resolved without executing the upstream file. The required constant lengths and prefixes are listed in `dependency_spec.json`; missing or ambiguous values are rejected. A later incompatible upstream revision may require obtaining a compatible historical version. The publication notebook's attached source version is recorded by Kaggle.

For local execution, set `KAGGRICULTURE_UPSTREAM_MAIN` to that downloaded `main.py`. The public code package references these arrays rather than duplicating them as a new Dataset.

## Observed Production task library

The production expert's `_DATA` field contains 24 reference episodes: each has 719 action dictionaries, daily field/shop snapshots, and derived worker-task lists. These were extracted from public episodes of submission 56689315. Unlike learned parameters or newly optimized schedules, this object directly retains recorded competition actions and observations. It is excluded from the public Dataset under the competition's Data Security restrictions.

An authorized holder of the original Observed Production source can use `extract_task_library.py` to create the required local sidecar. Set `KAGGRICULTURE_PRIVATE_ASSETS` to its path. The tool does not provide access to the original artifact, accept rules, or grant redistribution rights. Keep the sidecar out of public notebook outputs.

Consequently, Last Dance can run with the documented public upstream dependency; exact Observed Production inference additionally requires an authorized task library. Its algorithm and learned parameters are public, but its full inference inputs are not contained in this release. The public notebook does not pretend to run the missing branch.

Rules: https://www.kaggle.com/competitions/kaggriculture/rules
