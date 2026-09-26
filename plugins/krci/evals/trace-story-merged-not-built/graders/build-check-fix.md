---
type: regex
weight: 1
pattern: 'commitSha|prNumber|--pr\b|(?:without|drop(?:ping)?|omit(?:ting)?|remov(?:e|ing|ed))\b[^\n]{0,20}--branch\b|match(?:ing)?\s+(?:it|the\s+run)?\s*by\s+(?:the\s+)?(?:merge\s+)?(?:commit|pr\s*number)'
flags: mi
match: contains
target: last_message
---

The answer names a way to find the build run for the merge commit that does not depend on `--branch main`: matching by `commitSha` or `prNumber` on the pipeline run, filtering with `--pr`, or dropping/omitting the `--branch` filter.
