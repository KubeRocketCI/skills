---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Says that `operation.phase` `Succeeded` is the result of the Argo CD sync, that is, the manifests were applied, and does not show that the deploy went through.
2. Names the deploy pipeline run of the environment as what settles the question: `krci pipelinerun list` for the deploy runs of `shop` and `dev`, read by its status or by the `deploy-app` task that `--reason` lists (on `list` or on `krci pipelinerun get <run>`).
3. Does not look for that run with `--project shop-api`: deploy runs carry no project.
4. Does not recommend promoting the version to `qa` now.

Fail if the response agrees that the deploy went through because the operation phase is `Succeeded`, or if it says that krci cannot show how the deploy run ended.
