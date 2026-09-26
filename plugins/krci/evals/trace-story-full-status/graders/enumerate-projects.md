---
type: regex
weight: 1
pattern: 'krci\s+project\s+list\b'
flags: m
match: contains
target: last_message
---

The answer includes `krci project list` (optionally with `-o json`) as the first step, to enumerate every project before searching any single repository for the commit. A plan that starts from one guessed or assumed project name, without this command, fails this check.
