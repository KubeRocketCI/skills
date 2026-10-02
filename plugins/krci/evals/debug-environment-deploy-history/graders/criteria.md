---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Selects the deploy runs of the environment by deployment and environment, `krci pipelinerun list --deployment shop --env qa` with `--type deploy` to leave out clean runs, not by matching run names. `krci pipelinerun list --type deploy` alone holds the deploy runs still in the cluster plus only the 10 most recent finished ones of the whole platform, and an automatic deploy is named after the trigger template, for example `deploy-with-approve-shop-qa-`. A name filter, or kubectl with the label `app.edp.epam.com/cdstage=shop-qa`, may appear next to it as a fallback.
2. Does not rely on filtering deploy runs by project: deploy pipeline runs carry no project, so `krci pipelinerun list --project shop-api --type deploy` returns nothing. The response either says so or avoids that command.
3. Names a field that holds the time of the last deploy and one that holds its version. Any of these counts: `startTime` of the run with its `results.APPLICATIONS_PAYLOAD` or its log, `projects[].version` and `deployedAt` of `krci env get shop qa -o json`, the same fields of `krci project deployments shop-api`, or the history of the Argo CD Application.

Fail if the response's only way to find deploy runs is `--project shop-api` combined with `--type deploy`, or a filter on run names without `--deployment` and `--env`, or if it treats an empty result as "no deploy happened".
