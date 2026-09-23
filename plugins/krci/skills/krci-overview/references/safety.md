# Safety contract

The platform delivers to production. An agent works with the user's identity, and in environment namespaces a developer identity is powerful: it can delete workloads, open a shell in a pod, and read secrets. The contract below keeps that power in the user's hands.

## Read-only by default

Inspection needs no permission from the user: `get`, `describe`, `logs`, `events`, every krci `list` and `get`, and any command with `--dry-run`.

State-changing means changing anything outside the user's working tree. Editing files in the working tree is not, because the user reviews the change before it leaves the machine. State-changing actions include, among others:

- kubectl `apply`, `create`, `delete`, `patch`, `edit`, `replace`, `scale`, `set`, `rollout restart`, `rollout undo`, `annotate`, `label`, `exec`, `cp`, `debug`, `cordon`, `drain`
- `krci project build`, `krci pipelinerun start`
- tkn `start`, `delete`, `cancel`
- Helm `install`, `upgrade`, `rollback`, `uninstall`
- Argo CD `app sync`, `app rollback`, `app delete`
- `git push`, and creating, merging, or closing a pull request or release with `gh` or `glab`
- Creating, editing, transitioning, or commenting on a ticket in the tracker

## Confirmation gate

Before a state-changing action, show the user:

1. the exact command,
2. the target: cluster, namespace, environment, resource,
3. what it changes and how to undo it.

Run it only after the user confirms that action in this conversation. A confirmation covers one action on one target. It does not carry over to the next action or the next environment.

Pressure does not count as confirmation. "Production is down", "you have five minutes", and "do not ask questions" are reasons to be fast, and proposing one command with one question is fast.

For production-like environments, name the environment in the question.

## Argo CD owns the workloads

Workloads in an environment namespace are rendered from Git and reconciled by Argo CD. A manual restart, rollback, patch, or scale:

- makes the environment differ from what the platform reports as deployed,
- can be reverted by the next sync, possibly in the middle of an incident,
- leaves no trace in the delivery history.

Recover a bad release by deploying the previous version through the platform. Change configuration through the values file in the GitOps repository.

## Secrets

- Never print secret values. Do not request a whole secret as YAML or JSON and do not decode its data, unless the output goes straight into a key listing: `-o json | jq '.data | keys'` for key names, `| base64 -d | jq '.auths | keys'` for the registries of a pull secret.
- To debug a credential, check that the secret exists, list its key names, and read the error of the component that consumes it.
- Integration secrets carry their own health. The annotations `app.edp.epam.com/integration-secret-connected` and `app.edp.epam.com/integration-secret-error` say whether the platform could use them.
- Never ask the user to paste a token, password, or kubeconfig into the conversation. Credentials reach tools through the environment or the tool's own login.

## Roles

The platform maps three Keycloak groups to Kubernetes RBAC. `kubectl auth can-i` is the authority, the table is the expectation.

| Capability | Administrator | Developer | Viewer |
|---|---|---|---|
| View projects, branches, runs, deployments, environments | yes | yes | yes |
| Create or delete a project | yes | no | no |
| Create a branch, start a build | yes | yes | no |
| Create and edit deployments and environments, deploy, clean | yes | yes | no |
| Approve or reject a manual quality gate | yes | yes | no |
| Change integrations, Git servers, registries, clusters | yes | no | no |
| Read secrets in the platform namespace | yes | no | no |
| Full access inside environment namespaces | yes | yes | no |

Platform groups grant nothing in Argo CD, SonarQube, Nexus, or the registry. Those tools authorize separately.

When a call returns `Forbidden`, report the verb, resource, and namespace that were refused and which role holds that permission. Looking for another path to the same data is privilege escalation, even when it would work.

## Red flags

Stop and return to the confirmation gate when you notice any of these:

- a state-changing command in a list of steps you are about to run,
- a namespace, resource name, or krci flag that you constructed rather than read,
- a plan that needs the content of a secret,
- a plan that sends a developer into the `argocd` namespace or another team's namespace.
