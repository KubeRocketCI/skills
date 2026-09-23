---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Identifies the cause class: Argo CD cannot reach the target cluster registered for the environment, which is a connectivity or cluster registration problem and not a defect in the application code, image, or Helm chart.
2. Rules out the recent chart change as the cause, because Argo CD fails before it compares or renders any manifest, and advises against reverting it as the fix.
3. States an explicit ownership verdict: this is for the platform team (or whoever operates the cluster registration and Argo CD) to fix, and nothing in the application repository will resolve it.
4. Keeps the developer inside their role: it does not send them to the `argocd` namespace, to Argo CD cluster secrets, or to `argocd cluster` or `argocd app` administration commands. Those checks go into the escalation bundle for the platform team.
5. Gives the developer an escalation bundle to hand over: the deployment and environment names, the target cluster name read from the platform (`Stage.spec.clusterName`, or `infrastructure.cluster` of `krci env get billing dev`) rather than only the IP address, the exact condition text, and when it started.

Fail if the response recommends reverting the chart change or changing application code, the Dockerfile, or chart values as the fix, if it tells the developer to inspect or edit Argo CD cluster registration themselves, or if it never says who owns the fix.
