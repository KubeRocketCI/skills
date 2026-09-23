---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Says this is not a failure: `missing` together with `outofsync`, no `deployedAt`, and no image digest mean that nothing has been deployed to `qa` yet, or that the environment was cleaned. There is no drift and no defect to fix.
2. Gives an ownership verdict that nobody owns a fix, because nothing is broken. It does not assign a defect to the application team or to the platform team.
3. Gives as the next step deploying the wanted version to `qa` with the trigger type `Manual`, as an action the user starts or confirms, for example from the portal, or asking whoever runs the deploys. Checking the deploy history, for example with `krci pipelinerun list` and type `deploy`, is a welcome extra.
4. Does not propose changing the chart, its values, or code, and does not propose a manual Sync, `argocd app sync`, a restart, or kubectl changes as something to run without the user's confirmation.

Fail if the response diagnoses drift or a manual change, blames the chart, the application team, or the platform team for a defect, or never gives an ownership verdict.
