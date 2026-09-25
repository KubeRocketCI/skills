---
type: regex
weight: 1
pattern: '^\s*(?:```\w*\s*)?(?:\*\*|__)?Owner\s*(?::|(?:\*\*|__)\s*:)'
match: contains
target: last_message
---

The answer starts with the `Owner:` line of the ownership verdict, optionally inside a code block or in bold. A paragraph before it fails, also one that rebuts the cause the user suggested.
