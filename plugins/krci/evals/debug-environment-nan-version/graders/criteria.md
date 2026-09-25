---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Says that nothing has been deployed to `qa` yet: `NaN` is the placeholder version that the platform sets when an environment is created, and Argo CD cannot resolve it until the first deploy. It is not a missing Git tag, a failed build, or a defect.
2. Gives an ownership verdict that nobody owns a fix (for example `Owner: none` or `nobody`), because nothing is broken. It does not assign a defect to the application team or the platform team.
3. Gives as the next step deploying the wanted version to `qa`, which is needed because the trigger type is `Manual`, as an action the user or whoever runs deploys starts from the portal, not something the agent runs unconfirmed.
4. Tells the user not to open a bug for the application team about tags or builds for this state.

Fail if the response agrees that the build or tagging failed, assigns the fix to the application team or the platform team, or proposes a rebuild, a manual Sync, or chart changes as the fix.
