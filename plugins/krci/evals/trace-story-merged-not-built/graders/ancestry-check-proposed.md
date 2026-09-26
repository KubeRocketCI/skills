---
type: regex
weight: 1
pattern: 'git(?:\s+-\S+(?:\s+[^-\s]\S*)?)*\s+merge-base(?:\s+-\S+)*\s+--is-ancestor|git(?:\s+-\S+(?:\s+[^-\s]\S*)?)*\s+tag(?:\s+-\S+)*\s+--contains'
flags: mi
match: contains
target: last_message
---

The answer names an explicit ancestry command (`git merge-base --is-ancestor <sha> <tag>` or `git tag --contains <sha>`) as the way to confirm no built version contains the commit, rather than relying on comparing version numbers or timestamps.
