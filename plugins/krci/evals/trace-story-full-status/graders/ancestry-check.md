---
type: regex
weight: 1
pattern: 'git(?:\s+-\S+(?:\s+[^-\s]\S*)?)*\s+merge-base(?:\s+-\S+)*\s+--is-ancestor|git(?:\s+-\S+(?:\s+[^-\s]\S*)?)*\s+tag(?:\s+-\S+)*\s+--contains'
flags: m
match: contains
target: last_message
---

The answer names an explicit ancestry command (`git merge-base --is-ancestor <sha> <tag>` or `git tag --contains <sha>`) to decide whether an environment's version contains the story commit. Comparing version numbers or deploy timestamps instead, without either command, fails this check.
