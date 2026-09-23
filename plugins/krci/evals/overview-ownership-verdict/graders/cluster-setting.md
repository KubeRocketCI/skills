---
type: regex
weight: 1
pattern: 'Stage\.spec\.clusterName|infrastructure\.cluster|krci\s+env\s+get\s+billing\s+dev'
match: contains
target: last_message
---

The answer reads the environment's target cluster from the platform, `Stage.spec.clusterName` or `infrastructure.cluster` of `krci env get billing dev`, instead of relying on the IP address in the condition.
