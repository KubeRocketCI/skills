# Tooling

Three tiers, tried in this order: the krci CLI, kubectl, the Git provider. Skills describe the information they need. This file says how each tier provides it.

## Contents

- [krci CLI](#krci-cli)
- [Sessions](#sessions)
- [JSON contract](#json-contract)
- [Errors and empty results](#errors-and-empty-results)
- [Deploy history of one environment](#deploy-history-of-one-environment)
- [What krci does not cover](#what-krci-does-not-cover)
- [kubectl](#kubectl)
- [Git provider](#git-provider)

## krci CLI

Verified against krci `v0.19.0`. The CLI grows quickly, so `krci <group> <verb> --help` is the authority.

krci talks to the KubeRocketCI portal over HTTPS with the user's OIDC token. It never touches the Kubernetes API, so it works without a kubeconfig and for environments on remote clusters.

Install with `brew tap KubeRocketCI/homebrew-tap && brew install krci`, or take a binary from the [releases page](https://github.com/KubeRocketCI/cli/releases) (Linux and macOS on amd64 and arm64, Windows on amd64).

| Group (alias) | Verbs | Answers |
|---|---|---|
| `project` (`proj`) | `list`, `get <project>`, `deployments <project>`, `versions <project>`, `build <project>` | Which projects exist, their status, where each version is deployed, which versions were built per branch. `build` starts the build pipeline of a branch the way the portal's Build button does, and changes state. |
| `deployment` (`dp`) | `list`, `get <deployment>` | Deployment flows, their projects and environments, and the status message of each. |
| `env` (`e`) | `list`, `get <deployment> <environment>` | Health, sync, version, Argo CD conditions and last sync operation, ingress URLs, quality gates, target cluster and namespace. |
| `pipelinerun` (`run`) | `list`, `get <run>`, `start <pipeline>` | Run history, failure diagnosis, waiting for a run to end, and the results a run produced. `start` changes state. |
| `sonar` | `list`, `get`, `gate`, `issues` | Quality gate and issues per project, branch, or pull request. |
| `sca` | `list`, `get`, `components`, `findings` | Dependency-Track components and vulnerabilities. |
| `auth` | `login`, `status`, `logout` | Session. |

The `list` verbs of `project`, `deployment`, `env`, and `pipelinerun` also answer to `ls`.

Filters of `pipelinerun list`: `--project`, `--pr`, `--branch`, `--author`, `--type`, `--status`, `--deployment`, `--env`. `--type` matches the `app.edp.epam.com/pipelinetype` label exactly: `review`, `build`, `deploy`, `clean`, `security`, `tests`, `release`. `--status` takes `succeeded`, `failed`, `running`, `timeout`, or `cancelled`, in any case. A run that hit its timeout is `timeout`, not `failed`. `--deployment <deployment>` and `--env <environment>`, which works only together with `--deployment`, select deploy and clean runs, see [Deploy history of one environment](#deploy-history-of-one-environment).

With `--reason`, the newest match is diagnosed, so a run name is not needed up front. The failed task's log is cut to its last 25 lines. `--logs` in place of `--reason` returns the full log of that run in `logs`. With both flags only the diagnosis comes back.

When `--reason` has no task data to show, it leaves `tasks` out and says why in `tasksUnavailable`:

| `tasksUnavailable` | The run | Next step |
|---|---|---|
| `run_not_finished` | is pending or still running | Wait with `krci pipelinerun get <run> --wait --reason`, or add `--status failed` to diagnose the newest failed run instead |
| `not_indexed` | has finished, and Tekton Results has no task data for it yet | Ask again in a moment |
| `no_tasks` | has finished without scheduling a task, for example cancelled while pending or rejected before its first task | Do not ask again: there is nothing to diagnose. Read the run's `status` |

`--logs` has no such field: a run that has not finished comes back without `logs`.

`pipelinerun get <run> --wait` blocks until the run ends and then prints it, with `--reason` or `--logs` when given. It exits 0 only when the run succeeded: a failed, cancelled, or timed-out run is still printed, and the command exits 1. `--timeout` (default `1h`, only with `--wait`) limits the wait, and a wait that runs out prints nothing and exits 1. Use it instead of polling `get` or `list` in a loop.

A run that is still in the cluster carries `results`, its pipeline results by name. `VCS_TAG` of a succeeded build run is the Git tag of the version it produced: `build/<version>` for a `semver` project, the version itself with `default` versioning. A build that failed after its `get-version` task carries `VCS_TAG` too, although the tag may never have been pushed, so read `status` first. `APPLICATIONS_PAYLOAD` of a deploy run holds the versions it rolled out. A run read back from the history has no `results`: the versions of a branch are then in `krci project versions <project>`.

`sonar list`, `sonar issues`, `sca list`, and `sca components` page with `--page` (from 1) and `--page-size` (at most 500).

`project build <project> [--branch <branch>]` and `pipelinerun start <pipeline>` accept `--dry-run`, which prints the PipelineRun that would be created, as YAML or with `-o json`, and starts nothing. Show it to the user before asking to confirm the real run.

`project build` needs the build endpoint of the portal, which arrived after KubeRocketCI 3.15.0. On 3.15.0 the portal does not have it, and krci answers `portal has no endpoint for this command (…); upgrade the portal`, also with `--dry-run`. On such a platform a build starts from a merge or from the Build button of the portal.

## Sessions

Interactive login is a browser flow with OIDC and PKCE. An agent cannot complete it, the user runs it once:

```bash
krci auth login --portal-url https://<portal-host>
```

Check the session by the exit code. A valid session exits 0. A missing or expired session, or a token the portal rejects, exits 1 with the reason on standard error:

```bash
krci auth status >/dev/null 2>&1 || echo "no krci session"
```

Tokens refresh automatically while the refresh token is valid. There is one portal per configuration, no named contexts. The configuration lives in `~/.config/krci/config.yaml` on every operating system.

Headless use, for CI or a remote agent, replaces the login with environment variables. The token is an OIDC ID token or a Kubernetes service account token. It is supplied by the environment, never typed into a prompt or written to a file the agent creates.

| Variable | Meaning |
|---|---|
| `KRCI_PORTAL_URL` | Portal base URL. Required. `krci auth login` accepts only an HTTPS URL. |
| `KRCI_TOKEN` | Bearer token, used as is, without refresh. |
| `KRCI_CLUSTER_NAME`, `KRCI_NAMESPACE` | Cluster name and platform namespace. Required: without a login nothing discovers them, and every portal command refuses to run without them. |
| `KRCI_KEYRING_BACKEND` | `keyring` (default) or `file`. Use `file` where no OS keyring exists, as in containers and CI. |
| `KRCI_ISSUER_URL`, `KRCI_CLIENT_ID`, `KRCI_SCOPES` | OIDC settings for `krci auth login` when the portal does not provide them. |

## JSON contract

Every data command accepts `-o json`. Two shapes exist:

| Shape | Commands |
|---|---|
| `{"schemaVersion": "1", "data": ...}` | `env list`, `env get`, `project deployments`, `project versions`, `auth status`, `sonar *`, `sca *`, `pipelinerun start`, `project build` |
| bare payload | `project list`, `project get`, `deployment list`, `deployment get`, `pipelinerun list`, `pipelinerun get` |

Normalize before reading fields:

```bash
unwrap='if type == "object" and has("schemaVersion") then .data else . end'
krci project list -o json | jq "$unwrap | .[].name"
krci env get <deployment> <environment> -o json | jq "$unwrap | .projects[] | {name, status, sync, version}"
```

| Command | Payload after normalizing |
|---|---|
| `project list` | array of `{name, namespace, type, language, buildTool, framework, gitServer, gitUrl, status, available}` |
| `project deployments <project>` | `{project, rows[]}`, rows of `{deployment, env, deployed, status, sync, version, imageTag, imageDigest, cluster, namespace, triggerType, deployedAt, ingressUrls, argocdUrl, conditions, operation}` |
| `project versions <project>` | `{project, streams[]}`, streams of `{branch, image, versions[]}`, versions of `{name, created, digest?}`, newest first. `versions` is empty for a branch that was never built |
| `env list` | `stages[]` of `{deployment, env, cluster, namespace, triggerType, status, order}` |
| `env get` | `{deployment, env, status, order, detailedMessage, description, infrastructure{cluster, namespace, triggerType, deployPipeline, cleanPipeline}, qualityGates[], projects[]}`. `status` and `detailedMessage` are the environment's own: `created`, or `failed` with the reason |
| `env get` `qualityGates[]` | `{type, stepName, autotestName, branchName}` |
| `env get` `projects[]` | `{name, status, sync, version, imageTag, imageDigest, ingressUrls, argocdUrl, deployedAt, valuesOverride, conditions[], operation}` |
| `projects[].conditions[]` | `{type, message, lastTransitionTime}`, the Argo CD Application conditions, such as `ComparisonError` |
| `projects[].operation` | `{phase, message, startedAt, finishedAt}` of the last sync, `null` until the first sync. `phase` is `Running`, `Succeeded`, `Failed`, `Error`, or `Terminating` |
| `pipelinerun list`, `pipelinerun get` | `{pipelineRuns[], logs?, tasks?, tasksUnavailable?}`, newest run first, `get` with its one run. With `--reason`, `tasks[]` carries `{name, status, duration, failedStep, exitCode, message, logs}`, or `tasksUnavailable` says why there are none |
| `pipelineRuns[]` | `{name, portalUrl, status, pipeline, project, type, branch, prNumber, prUrl, author, startTime, duration, targetBranch, commitSha, deployment, env, results}`. `status` is `Running`, `Succeeded`, `Failed`, `Timeout`, or `Cancelled`, and empty for a run that has not started yet. A field that does not apply is left out. A deploy or clean run has an empty `project` and carries `deployment` and `env` |
| `pipelineRuns[].results` | pipeline results by name, only while the run is in the cluster. `VCS_TAG` on a build run that got past `get-version`, whatever its `status`. `APPLICATIONS_PAYLOAD` on a deploy run whose `deploy-app` task succeeded: a JSON string, `fromjson` turns it into `{<project>: {imageTag, imageDigest?, customValues?}}`, cut to the projects that fit into the result size |
| `sonar list` | `{projects[], paging{pageIndex, pageSize, total}}` |
| `sca list` | `{items[], totalCount}` |
| `auth status` | `{authenticated, user?, name?, groups[], expiresAt}`. Without a valid session it exits 1 and prints the error envelope |

`status` and `sync` of a project are lowercase: `healthy`, `progressing`, `degraded`, `suspended`, `missing`, `unknown`, and `synced`, `outofsync`, `unknown`. `version` is the version the Application points at, and `deployedAt` is when the last sync finished, whatever its `operation.phase`. Neither proves that the version runs, and `operation.phase` `Succeeded` says only that Argo CD applied the manifests. Whether a deploy went through is read from its run, see [Deploy history of one environment](#deploy-history-of-one-environment).

A project of an environment shows one of three shapes when it runs nothing:

| Shape | Meaning |
|---|---|
| `version` and `imageTag` `"NaN"`, `status` `healthy`, `sync` `unknown`, a `ComparisonError` saying `unable to resolve 'NaN'` (`'build/NaN'` for `semver` projects), `operation` `null` | The environment was created and never deployed. `NaN` is the placeholder version of a new environment. |
| a real `version`, `status` `missing`, `sync` `outofsync`, `operation` `null` | The environment was cleaned. The Application keeps the last deployed version and has no resources. |
| every field `null` | No Application exists. A healthy environment always has one, so read the environment's own `status` and `detailedMessage`. `failed` names the reason. An empty `status` means the environment is still being created: it waits while the previous environment in the order has no image stream, for example because that environment failed. |

SonarQube measures are strings, convert with `tonumber` before comparing.

## Errors and empty results

Exit code 0 means the command worked, also when the result is empty. Exit code 1 covers every failure, and a `pipelinerun get --wait` whose run did not succeed. Check the exit code before parsing: with `-o json`, a command of the enveloped shape prints `{"schemaVersion": "1", "error": {"message": ...}}` on standard output, so the normalizer above yields `null` instead of failing. A flag or an argument that a command rejects is reported on standard error only.

Read commands turn HTTP status codes into plain messages. `project build` and `pipelinerun start` turn the reason the portal gives into one line, such as `branch '<branch>' of project '<project>' not found` or `a build is already running for branch '<branch>' of project '<project>'`.

An unknown `--type` value is not rejected. It returns an empty list with exit code 0, which looks like "nothing ran", and so does a `--deployment` or `--env` name that does not exist. An unknown or empty `--status` value is rejected with exit code 1, and the message lists the valid values. Use only the values listed above.

## Deploy history of one environment

Deploy and clean runs carry no `app.edp.epam.com/codebase` label, so `krci pipelinerun list --project <project> --type deploy` is always empty. Select them by deployment and environment, with the names `krci env get` takes:

```bash
krci pipelinerun list --deployment <deployment> --env <environment> --type deploy -o json
```

The newest run comes first. Without `--type deploy` the clean runs of the environment are listed too, and `--deployment` alone lists the runs of every environment of the flow. The list holds the runs still in the cluster plus the 10 most recent matches from Tekton Results. Add `--reason` for the tasks of the newest run, with the step and log tail of the one that failed.

The deploy itself is the task `deploy-app` of the run. It points the applications at the version, syncs them, and then waits for them to become healthy, so it fails when the sync fails and also when the applications do not come up. In the second case Argo CD still reports the sync as `Succeeded`. The task has one step, `wait-for-deploy`, so the log tail says which part failed. The other tasks of the run are `pre-deploy` and `post-deploy`, the environment's quality gates, such as `approve` or `init-autotests` and `wait-for-autotests`, and `promote-images`: a run that failed or timed out in a task after `deploy-app` did deploy, and a `Running` run may be waiting for an approval.

The versions a run rolled out are in its `results.APPLICATIONS_PAYLOAD` while the run is in the cluster. For an older run, `krci pipelinerun get <run> --logs` prints the whole payload in the `new_tags=` line of the `deploy-app` task.

Finished runs are matched by the labels `app.edp.epam.com/cdpipeline` and `app.edp.epam.com/cdstage`, which Tekton Results has to keep for each run. The KubeRocketCI add-ons configure that, see [Install Tekton](https://docs.kuberocketci.io/docs/operator-guide/install-tekton). Runs archived without the labels stay unmatched: `--deployment` and `--env` then find only the runs still in the cluster, and `--type deploy` shows the finished deploy runs with no `deployment` and `env`. Tell those apart by name: a deploy from the portal is named `deploy-<deployment>-<environment>-<suffix>`, an automatic deploy after the environment's trigger template, `deploy-`, `deploy-with-approve-`, `deploy-diff-approve-`, or `deploy-…-auto-` for autotests, and a custom trigger template can use another prefix.

The versions a project had in an environment, including runs that Tekton Results no longer holds, are in the history of its Argo CD Application. Each entry has `deployedAt` and the `image.tag` Helm parameter:

```bash
kubectl get applications.argoproj.io <deployment>-<environment>-<project> -n <platform-namespace> \
  -o jsonpath='{range .status.history[*]}{.deployedAt}{"\t"}{.source.helm.parameters[?(@.name=="image.tag")].value}{"\n"}{end}'
```

## What krci does not cover

| Need | Tier that provides it |
|---|---|
| Pod logs and events of a deployed application | kubectl in the environment namespace |
| Per-resource diff between Git and the cluster | kubectl on the Application resource, or the Application's page in Argo CD: `argocdUrl` of `krci env get` is its path on the Argo CD server |
| Status message of a Codebase or CodebaseBranch | kubectl on the resource, see the fields in [vocabulary.md](vocabulary.md) |
| Deploying, promoting, approving a quality gate | The portal. A skill that does this through the cluster says so and passes the confirmation gate. |

## kubectl

kubectl acts under the user's own identity. Find out what that identity may do before building a plan on it:

```bash
kubectl auth whoami
kubectl auth can-i --list -n <platform-namespace>
```

Read-only verbs are `get`, `describe`, `logs`, `events`, `top`, `auth`, `api-resources`, and `explain`. Everything else changes state and falls under the safety contract.

Two traps:

- Run history lives in Tekton Results. A finished PipelineRun stays in the cluster only as long as the platform's retention allows, so an empty `kubectl get pipelineruns` says nothing about history. Use krci for anything that is not running now.
- An environment whose cluster is not `in-cluster` runs elsewhere. The platform cluster holds its Stage and its Argo CD Application, not its pods. Application status then comes from the Application resource, or from kubectl with a kubeconfig for the target cluster if the user has one.

## Git provider

Use `gh`, `glab`, or plain `git` when the answer is in Git rather than in the platform:

- Pull request state, checks, and review comments for a failed review run.
- Which branch, pull request, or commit carries a ticket key.
- Whether the Git tag of a version exists in the application repository. See the versioning rules in [vocabulary.md](vocabulary.md).
- What the GitOps repository sets for an environment in `<deployment>/<environment>/<project>-values.yaml`.
