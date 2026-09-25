---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Does not rely on filtering deploy runs by project: deploy pipeline runs do not carry the project label, so `krci pipelinerun list --project shop-api --type deploy` returns nothing. The response either says so or avoids that command.
2. Lists deploy runs of the environment in a way that works: `krci pipelinerun list --type deploy -o json` and a filter on run names that belong to `shop` and `qa`, or kubectl on PipelineRuns with the label `app.edp.epam.com/cdstage=shop-qa`, or both.
3. Accounts for the run name not always starting with `deploy-shop-qa-`: with a manual approval gate, runs started by auto-deploy are named after the trigger template, for example `deploy-with-approve-shop-qa-`. Alternatively, it filters by the `cdstage` label, which does not depend on the name.
4. Reads the current version and the time of the last sync from `krci env get shop qa -o json` (`projects[].version`, `deployedAt`, `operation`), or from `krci project deployments shop-api`.

Fail if the response's only way to find deploy runs is `--project shop-api` combined with `--type deploy`, or if it treats an empty result as "no deploy happened".
