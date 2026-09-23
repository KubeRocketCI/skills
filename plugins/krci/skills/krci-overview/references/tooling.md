# Tooling

Three tiers, tried in this order: the krci CLI, kubectl, the Git provider. Skills describe the information they need. This file says how each tier provides it.

## Contents

- [krci CLI](#krci-cli)
- [Sessions](#sessions)
- [JSON contract](#json-contract)
- [Errors and empty results](#errors-and-empty-results)
- [What krci does not cover](#what-krci-does-not-cover)
- [kubectl](#kubectl)
- [Git provider](#git-provider)

## krci CLI

Verified against krci `v0.15.0`. The CLI grows quickly, so `krci <group> <verb> --help` is the authority.

krci talks to the KubeRocketCI portal over HTTPS with the user's OIDC token. It never touches the Kubernetes API, so it works without a kubeconfig and for environments on remote clusters.

Install with `brew tap KubeRocketCI/homebrew-tap && brew install krci`, or take a binary from the [releases page](https://github.com/KubeRocketCI/cli/releases) (Linux and macOS on amd64 and arm64, Windows on amd64).

| Group (alias) | Verbs | Answers |
|---|---|---|
| `project` (`proj`) | `list`, `get <project>`, `deployments <project>`, `build <project>` | Which projects exist, their status, where each version is deployed. `build` starts the build pipeline of a branch the way the portal's Build button does, and changes state. |
| `deployment` (`dp`) | `list`, `get <deployment>` | Deployment flows, their projects and environments. |
| `env` (`e`) | `list`, `get <deployment> <environment>` | Health, sync, version, ingress URLs, quality gates, target cluster and namespace. |
| `pipelinerun` (`run`) | `list`, `get <run>`, `start <pipeline>` | Run history and failure diagnosis. `start` changes state. |
| `sonar` | `list`, `get`, `gate`, `issues` | Quality gate and issues per project, branch, or pull request. |
| `sca` | `list`, `get`, `components`, `findings` | Dependency-Track components and vulnerabilities. |
| `auth` | `login`, `status`, `logout` | Session. |

The `list` verbs of `project`, `deployment`, `env`, and `pipelinerun` also answer to `ls`.

Filters of `pipelinerun list`: `--project`, `--pr`, `--branch`, `--author`, `--type`, `--status`. `--type` matches the `app.edp.epam.com/pipelinetype` label exactly: `review`, `build`, `deploy`, `clean`, `security`, `tests`, `release`. `--status` takes `succeeded`, `failed`, `running`, `timeout`, or `cancelled`, in any case.

With `--reason`, the most recent finished match is diagnosed, so a run name is not needed up front. Running runs are skipped. The failed task's log is cut to its last 25 lines. `--logs` appends the full log.

`sonar list`, `sonar issues`, `sca list`, and `sca components` page with `--page` (from 1) and `--page-size` (at most 500).

`project build <project> [--branch <branch>]` and `pipelinerun start <pipeline>` accept `--dry-run`, which prints the PipelineRun that would be created, as YAML or with `-o json`, and starts nothing. Show it to the user before asking to confirm the real run.

## Sessions

Interactive login is a browser flow with OIDC and PKCE. An agent cannot complete it, the user runs it once:

```bash
krci auth login --portal-url https://<portal-host>
```

Check the session by reading standard output. Both a valid and a missing session exit 0, and the "not authenticated" message goes to standard error:

```bash
krci auth status 2>/dev/null | grep -q 'Authenticated' || echo "no krci session"
```

Tokens refresh automatically while the refresh token is valid. There is one portal per configuration, no named contexts. The configuration lives in `~/.config/krci/config.yaml` on every operating system.

Headless use, for CI or a remote agent, replaces the login with environment variables. The token is an OIDC ID token or a Kubernetes service account token. It is supplied by the environment, never typed into a prompt or written to a file the agent creates.

| Variable | Meaning |
|---|---|
| `KRCI_PORTAL_URL` | Portal base URL, HTTPS only. Required. |
| `KRCI_TOKEN` | Bearer token, used as is, without refresh. |
| `KRCI_CLUSTER_NAME`, `KRCI_NAMESPACE` | Cluster name and platform namespace. Required: without a login nothing discovers them, and every portal command refuses to run without them. |
| `KRCI_KEYRING_BACKEND` | `keyring` (default) or `file`. Use `file` where no OS keyring exists, as in containers and CI. |
| `KRCI_ISSUER_URL`, `KRCI_CLIENT_ID`, `KRCI_SCOPES` | OIDC settings for `krci auth login` when the portal does not provide them. |

## JSON contract

Every data command accepts `-o json`. Two shapes exist:

| Shape | Commands |
|---|---|
| `{"schemaVersion": "1", "data": ...}` | `env list`, `env get`, `project deployments`, `sonar *`, `sca *`, `pipelinerun start`, `project build` |
| bare payload | `project list`, `project get`, `deployment list`, `deployment get`, `pipelinerun list`, `pipelinerun get` |

Normalize before reading fields:

```bash
unwrap='if type == "object" and has("schemaVersion") then .data else . end'
krci project list -o json | jq "$unwrap | .[].name"
krci env get <deployment> <environment> -o json | jq "$unwrap | .projects[] | {name, status, sync, version}"
```

| Command | Payload after normalizing |
|---|---|
| `project list` | array of `{name, namespace, type, language, buildTool, framework, gitServer, status, available}` |
| `project deployments <project>` | `{project, rows[]}`, rows of `{deployment, env, deployed, status, sync, version, imageTag, imageDigest, cluster, namespace, triggerType, deployedAt, ingressUrls, argocdUrl}` |
| `env list` | `stages[]` of `{deployment, env, cluster, namespace, triggerType, status, order}` |
| `env get` | `{deployment, env, status, infrastructure{cluster, namespace, triggerType, deployPipeline, cleanPipeline}, qualityGates[], projects[]}` |
| `env get` `qualityGates[]` | `{type, stepName, autotestName, branchName}` |
| `env get` `projects[]` | `{name, status, sync, version, imageTag, imageDigest, ingressUrls, argocdUrl, deployedAt, valuesOverride}` |
| `pipelinerun list` | `{pipelineRuns[], logs?, tasks?}`. With `--reason`, `tasks[]` carries `{name, status, duration, failedStep, exitCode, message, logs}` |
| `sonar list` | `{projects[], paging{pageIndex, pageSize, total}}` |
| `sca list` | `{items[], totalCount}` |

A project that is registered in an environment but never deployed has `null` in `status`, `sync`, and `version`. That is an empty environment, not an error. SonarQube measures are strings, convert with `tonumber` before comparing.

## Errors and empty results

Exit code 0 means the command worked, also when the result is empty. Exit code 1 covers every failure. Check the exit code before parsing: with `-o json`, an enveloped command prints `{"schemaVersion": "1", "error": {"message": ...}}` on standard output, so the normalizer above yields `null` instead of failing.

Read commands turn HTTP status codes into plain messages. `project build` and `pipelinerun start` also report a stable reason from the portal, such as `codebase_branch_not_found`, `build_pipeline_not_configured`, or `build_in_progress`.

An unknown `--type` or `--status` value is not rejected. It returns an empty list with exit code 0, which looks like "nothing ran". Use only the values listed above.

## What krci does not cover

| Need | Tier that provides it |
|---|---|
| Pod logs and events of a deployed application | kubectl in the environment namespace |
| Why Argo CD cannot sync: conditions, operation state, per-resource diff | kubectl on the Application resource, or the Argo CD link from `krci env get` |
| Status message of a Codebase, CDPipeline, or Stage | kubectl on the resource, see the fields in [vocabulary.md](vocabulary.md) |
| Image tags available for deployment | kubectl on the CodebaseImageStream |
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
