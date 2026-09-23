---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Queries the `krci` CLI first, with a pipeline run listing filtered to the project, and uses its failure diagnosis (`--reason`, optionally `--logs`) to get the failed task and step.
2. Uses only verbs and flags that exist in the krci CLI: `krci pipelinerun list` (alias `krci run list`) with filters from `--project`, `--pr`, `--branch`, `--author`, `--type` (for example `review`), and `--status failed`, plus `--reason` or `--logs`, optionally `-o json`. `krci pipelinerun get <run>` with the same `--reason` or `--logs` flags and `krci auth status` as a session check are also valid. Fail if the response invents syntax such as `krci get pipelineruns`, `krci pipeline list`, or `--codebase`, or admits that it has not verified the command names.
3. Gives the specific reason for querying the CLI first: the run history is kept in Tekton Results, which the portal and the CLI read, and a finished PipelineRun may no longer exist in the cluster, so `kubectl get pipelineruns` can miss a run from yesterday. Accept "pruned", "cleaned up", "retention", or "garbage-collected" as the wording for the second part. A reason that only says the CLI is more convenient, higher-level, or purpose-built is not enough.

Fail if the primary path is `kubectl get pipelineruns`, `tkn`, or pod logs, or if `kubectl logs` or `kubectl get pipelinerun` is presented as the way to obtain the failure reason. Naming kubectl as a fallback after krci, for a run that is still in the cluster, is fine.
