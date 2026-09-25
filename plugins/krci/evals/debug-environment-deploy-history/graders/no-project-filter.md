---
type: regex
weight: 1
pattern: '^\s*(?:\d+[.)]\s*)?`?(?:\$\s*)?krci\s+(?:pipelinerun|run)\s+(?:list|ls)\b(?=[^\n]*--project\b)(?=[^\n]*--type[=\s]+deploy\b)'
flags: m
match: not_contains
target: last_message
---

No command line in the answer combines `--project` with `--type deploy` in `krci pipelinerun list`. Prose that warns against the combination does not count.
