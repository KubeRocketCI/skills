# Skill map

Where each skill sits in the delivery lifecycle and whom it serves. Before proposing a skill, find its row here. If no row fits, say which stage and roles it serves in the issue.

Planned names are proposals and change with the eval cases. A planned skill becomes available when it is merged, and the README table lists it from then on.

| Stage | Roles | Skill | Status | Settles |
|---|---|---|---|---|
| all | all | `krci-overview` | available | Lifecycle, roles, vocabulary, tool tiers, preflight, safety contract, ownership verdict. |
| plan | ba, po, pm, dev, qa | `krci-trace-story` | available | The implementation status of a story by its tracker key, per project — whether it merged, its first version, and which environments run it. |
| code | dev | `krci-debug-review` | planned | Why the review run of a pull request failed, including code quality findings. |
| build | dev | `krci-debug-build` | planned | Why a build run failed, and who owns the fix. |
| build | devops | `krci-add-pipeline` | planned | How a custom pipeline is written and registered for a project. |
| test | qa | `krci-check-gates` | planned | Which quality gates an environment has, their state, and which approval waits for whom. |
| test | qa, devops | `krci-add-autotest` | planned | How an autotest project becomes a quality gate or a standalone tests run. |
| deploy | all | `krci-map-environments` | planned | Which version of each project runs in which environment. |
| deploy | dev, devops | `krci-write-chart` | planned | What the chart in `deploy-templates/` and the GitOps values file must provide. |
| operate | dev, qa, devops | `krci-debug-environment` | available | Why an environment is unhealthy, out of sync, or shows nothing deployed, and who owns the fix. |

## By role

| Role | Stages with skills |
|---|---|
| BA, PO, PM | plan, deploy |
| Developer | plan, code, build, deploy, operate |
| QA | plan, test, deploy, operate |
| DevOps | build, test, deploy, operate |
