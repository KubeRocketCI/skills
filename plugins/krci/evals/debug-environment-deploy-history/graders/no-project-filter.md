---
type: regex
weight: 1
pattern: '^\s*(?:\d+[.)]\s*)?`?(?:\$\s*)?krci\s+(?:pipelinerun|run)\s+(?:list|ls)\b(?=(?:[^\n]*\\\n)*[^\n]*--project\b)(?=(?:[^\n]*\\\n)*[^\n]*--type[=\s]+deploy\b)'
flags: m
match: not_contains
target: last_message
---

No command in the answer combines `--project` with `--type deploy` in `krci pipelinerun list`, also when it continues over several lines. Prose that warns against the combination does not count.
