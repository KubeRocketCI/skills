---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Maps the portal term "deployment" to the `CDPipeline` custom resource (here named `payments`), not to an `apps/v1` Deployment.
2. Maps the portal term "environment" to the `Stage` custom resource, named `<deployment>-<environment>` (here `payments-qa`).
3. States that the application pods run in the namespace recorded in `Stage.spec.namespace`, and that the default form is `<platform-namespace>-<deployment>-<environment>`, that is, prefixed with the platform namespace.

Fail if the response treats "deployment `payments`" as a Kubernetes Deployment workload. Fail if it presents `payments-qa`, `qa`, or `payments` as the namespace where the pods run, even when it adds that `Stage.spec.namespace` is authoritative.
