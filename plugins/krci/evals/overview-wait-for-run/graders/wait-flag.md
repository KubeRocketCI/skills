---
type: regex
weight: 1
pattern: 'krci\s+(?:pipelinerun|run)\s+get\b(?:[^\n]*\\\n)*[^\n]*--wait\b'
match: contains
target: last_message
---

A command in the answer waits for the run with `krci pipelinerun get <run> --wait`. The command may continue over several lines.
