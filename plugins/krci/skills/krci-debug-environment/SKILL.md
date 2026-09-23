---
name: krci-debug-environment
description: Why an environment is unhealthy or out of sync, and who owns the fix. Use when a Stage, an Argo CD Application, or a deployed project shows degraded, Unknown, Missing, or OutOfSync, or a pod shows ImagePullBackOff, CrashLoopBackOff, OOMKilled, or stays Pending. Not for a failing build or review run, or picking a version to deploy - krci-overview routes those once their own skill exists.
license: Apache-2.0
compatibility: Requires the krci CLI v0.15.0 or later with a portal session. v0.16.0 or later adds projects[].conditions[] and projects[].operation to krci env get, carrying the Argo CD condition text inline. kubectl under the user's own RBAC is optional, for pod/ReplicaSet events, previous-container logs, and resource status messages. Written against KubeRocketCI 3.15.
metadata:
  access: read-only
  roles: dev, qa, devops
  stage: operate
---

# Debug an environment

Settles why a deployed project in an environment is unhealthy, out of sync, or both, and whose job
it is to fix it, for a developer, QA engineer, or DevOps engineer watching that environment.

Vocabulary, tool tiers, the safety contract, and the ownership verdict come from `krci-overview`. Run its preflight before the first krci or kubectl call.

## Verdict

Start the answer with the ownership verdict from `krci-overview`: the `Owner:` line first, then `Cause`, `Evidence`, and `Next step`. Classify the state with the "Reading Argo CD Application state" table in `krci-overview`'s `references/ownership.md`; this skill does not restate that table, only the steps to gather the environment's own evidence for it. The `Owner:` line comes first also when the user or their lead already named a cause: answer that suspicion under `Cause`, never above the verdict.

## Procedure

1. Read the environment: `krci env get <deployment> <environment> -o json`, normalized per `krci-overview`'s JSON output section. Read `status` and `sync` per entry under `projects[]`, not the top-level `status` of the response, which is the `Stage`'s own lifecycle status (for example `created`) and says nothing about workload health. A Deployment can carry more than one project, each with its own state.
2. On krci CLI v0.16.0 or later, the same `projects[]` entry carries `conditions[]` and `operation` with the Argo CD condition text directly; read those before opening the Argo CD UI. Platform-group users often have no Argo CD access at all, so the UI is a weak fallback, not the first move. Match the condition text and the `status`/`sync` pair against `krci-overview`'s ownership table. Sync and health are independent axes: do not infer one from the other.
3. For `degraded` or long-`progressing` with no answer yet from step 2, read pod and ReplicaSet events in the environment's namespace (`infrastructure.namespace` of `krci env get`, not a guessed `<environment>` name) and classify with the table below. If `infrastructure.cluster` is not `in-cluster`, kubectl against the platform cluster cannot see these resources; use the target cluster's own context instead.
4. To compare live state against Git, read the condition text from step 2, or the values file in the GitOps repository; `krci deployment get` does not carry a Git-vs-cluster diff.
5. For "what was deployed and when", `krci pipelinerun list --project <project> --type deploy` returns nothing: deploy runs carry the project in a payload field the `--project` filter does not read, and matching by run-name prefix both misses approval-gated environments (`deploy-with-approve-…`, `deploy-diff-approve-…` name their runs differently) and over-matches (`qa` also matches `qa-eu`). List `--type deploy` and filter on the `app.edp.epam.com/cdstage=<deployment>-<environment>` label instead.
6. A restart, rollback, or scale is never the fix for `degraded`: it only masks the next reconcile. If you still propose one, it needs the user's explicit confirmation like any state-changing action, per the safety contract in `krci-overview`.

## Pod events

`status`/`sync` and the Argo CD condition say something is wrong; the pod's own events say what.

| Event or condition | Meaning | Owner |
|---|---|---|
| `ImagePullBackOff`/`ErrImagePull`, `401`/`403` | Registry authentication failed | platform team, unless the same image:tag already runs in another environment and this chart sets its own `imagePullSecrets` - then it's the application team's own broken reference |
| `ImagePullBackOff`/`ErrImagePull`, manifest or tag not found | The image reference itself is wrong, or the build never pushed it | application team |
| `CrashLoopBackOff` | The container starts and exits; the current attempt's log is often empty. Read the **previous** container's log: `kubectl logs --previous` | application team |
| `OOMKilled` | The container hit its memory limit | application team: the chart's resource limits or the process's own usage |
| `FailedScheduling` | No node satisfies the request | platform team, unless the chart's own `resources.requests` or `nodeSelector`/affinity is what can't be satisfied |
| Quota exceeded | Shows as `FailedCreate` on the **ReplicaSet**, not as a `Pending` pod event; check ReplicaSet events, not only pod events | application team asks for less, or platform team raises the namespace quota |
| `CreateContainerConfigError` | A referenced ConfigMap, Secret, or key is missing | application team's chart or values, unless the missing Secret is platform-managed |
| Stage carries a `detailedMessage` | Read it directly; it usually names the failing resource | depends on the message |

## Common mistakes

- Reading only the Stage's own `status` and skipping the per-project `status`/`sync` in `projects[]`: a Deployment with several projects can have one healthy and one degraded, and the top-level field is a different thing entirely (the Stage's lifecycle state, not health).
- Treating `outofsync` as proof of a manual edit worth reverting via Sync before checking what Git itself would deploy: if Git's version carries the same defect, Sync only reproduces it.
- Attributing every pull-secret or scheduling failure to the platform team without checking whether the chart supplies its own `imagePullSecrets`, `resources`, or `nodeSelector`: when it does, the misconfiguration is the application team's own.

## Further reading

- [Argo CD Integration](https://docs.kuberocketci.io/docs/operator-guide/cd/argocd-integration)
- [Manage Deployments](https://docs.kuberocketci.io/docs/user-guide/manage-environments)
