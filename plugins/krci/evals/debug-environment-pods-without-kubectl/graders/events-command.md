---
type: regex
weight: 1
pattern: 'krci\s+(?:env|e)\s+events\s+["'']?shop["'']?\s+["'']?qa(?![\w-])'
match: contains
target: last_message
---

A command in the answer reads the events of the environment with `krci env events shop qa`.
