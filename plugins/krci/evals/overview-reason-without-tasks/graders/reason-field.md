---
type: regex
weight: 1
pattern: 'tasksUnavailable[\s\S]*no_tasks|no_tasks[\s\S]*tasksUnavailable'
match: contains
target: last_message
---

The answer reads the field `tasksUnavailable` and names its value `no_tasks`, the one that ends the retries.
