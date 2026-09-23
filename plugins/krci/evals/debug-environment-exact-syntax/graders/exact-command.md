---
type: regex
weight: 1
pattern: 'krci env get\s+payments\s+qa'
match: contains
target: last_message
---

The exact, correctly-shaped command appears somewhere in the answer: `krci env get payments qa`,
deployment before environment, both as positional arguments.
