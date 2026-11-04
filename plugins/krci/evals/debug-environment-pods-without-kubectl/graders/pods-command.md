---
type: regex
weight: 1
pattern: 'krci\s+(?:env|e)\s+pods\s+["'']?shop["'']?\s+["'']?qa(?![\w-])'
match: contains
target: last_message
---

A command in the answer reads the pods of the environment with `krci env pods shop qa`.
