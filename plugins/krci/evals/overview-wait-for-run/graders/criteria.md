---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Blocks with `krci pipelinerun get build-orders-main-x7k2p --wait` (alias `krci run get`), optionally with `--timeout`, and not with a loop that polls `krci pipelinerun get` or `krci pipelinerun list` and sleeps.
2. Stops the script through the exit code of that command, which is 0 only when the run succeeded. A pipe into `jq` counts only with `set -o pipefail`, or when the exit code is checked before the output is read: a failed build is still printed and can carry a `VCS_TAG`.
3. Takes the version from the run itself: the pipeline result `VCS_TAG` in the JSON output (`.pipelineRuns[0].results.VCS_TAG`). For a semver project that value is the Git tag `build/<version>`, so the version is the part after `build/`.
4. If it mentions `krci project versions orders`, it is a fallback for a run that is no longer in the cluster, not the primary source: the newest version of the branch can belong to another build.

Fail if the snippet waits in a polling loop, or prints the newest entry of `krci project versions` as the version of this build without reading the run's result.
