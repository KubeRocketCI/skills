---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Says that the lead is wrong for this environment: it runs on the cluster of the portal (`infrastructure.cluster` is `in-cluster`), so the user's portal session is enough to read its pods and events with krci.
2. Gives `krci env pods shop qa` for the state of each pod and container (status, reason, exit code, or how the previous run ended), and `krci env events shop qa`, with or without `--warnings` or `--pod <pod>`, for what the scheduler, the kubelet, and the controllers reported.
3. Leaves to kubectl, or to someone with access to the namespace, only what krci does not show, such as the log of the previous container run. Reading the pods and events does not wait for the DevOps engineer.

Fail if the response agrees that nothing can be seen without kubectl, sends the user to wait or to escalate before reading the pods and events with krci, or invents krci syntax, for example `krci env logs`, `krci pods`, `krci get pods`, or a `--pods` flag.
