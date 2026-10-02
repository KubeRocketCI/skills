---
type: regex
weight: 1
pattern: 'krci\s+(?:pipelinerun|run)\s+(?:list|ls)\b(?=(?:[^\n]*\\\n)*[^\n]*--deployment[=\s]+["'']?shop(?![\w-]))(?=(?:[^\n]*\\\n)*[^\n]*--env[=\s]+["'']?qa(?![\w-]))'
match: contains
target: last_message
---

A command in the answer selects the runs of the environment with `--deployment shop` and `--env qa` in `krci pipelinerun list`. The command may continue over several lines.
