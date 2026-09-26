---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Gives the exact ancestry command to test "not built" definitively: get the commit SHA (for example `git log --grep='SHOP-163' -1 --format=%H` on `main`), list or check tags with `git tag --contains <sha>`, and states that an empty result means no existing tag, and therefore no built version, contains the commit yet.
2. Does not treat comparing deployed version numbers or timestamps against an expected baseline as sufficient by itself: it names ancestry (`git tag --contains` or `git merge-base --is-ancestor <sha> <tag>`) as the actual test, not "the version looks old" or "the version looks new enough".
3. To check whether a build ran for that commit, gives a pipeline run listing scoped to the project and build type (for example `krci pipelinerun list --project billing-api --type build -o json`), and explicitly does not rely on filtering that listing by `--branch main` (or the default/target branch) as the way to find it: `--branch` filters by the pipeline run's source branch, the branch the merge request came from, not the branch the merge lands on, so a build triggered by the merge itself would not reliably be labeled `main` and can be missed by that filter.
4. Instead of `--branch`, matches the right run some other reliable way: by the merge commit SHA (`commitSha` on the pipeline run) or the merge request number (`prNumber`), or by not restricting to a branch at all and checking timestamps/status of recent build runs.
5. Distinguishes a build that never ran from one that ran and failed (which would explain the missing tag), and says a failed build is worth escalating, while an unstarted build points at the webhook or trigger instead.

Fail if the response's only way to confirm "not built" is comparing version numbers or timestamps without naming an ancestry command, or if its only or first proposed way to find the build run is `krci pipelinerun list --project billing-api --branch main --type build` without flagging that this can miss a build started by the merge.
