---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Reads the field `tasksUnavailable` of the same JSON output, which is present when `tasks` is missing, and branches on its value.
2. `no_tasks`: the run finished and never scheduled a task, for example because it was cancelled before its first task. The script stops asking and reports the run's `status`.
3. `not_indexed`: the run finished and its task data is not in the history yet. Asking again a moment later makes sense.
4. `run_not_finished`: the run is pending or still running. The script waits for it with `krci pipelinerun get <run> --wait` (alias `krci run get`), with or without `--reason`, instead of sleeping and listing again.

Advice on top of these branches does not fail the answer: `--status failed` to skip runs that did not fail, the run's `status` as supporting context, or a time limit as a safety net.

Fail if the script still cannot tell a finished run whose tasks arrive a moment later from one that never gets any, for example because it decides from `status` alone or only limits the number of retries.
