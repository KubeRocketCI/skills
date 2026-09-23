---
name: krci-verb-object
description: <What the skill covers, one clause>. Use when <triggers, in the words users type>. Not for <neighboring intent> (use <sibling-skill>).
license: Apache-2.0
compatibility: <Required tools, for example the krci CLI v0.15.0 or later with a portal session>. <Optional tools>. Written against KubeRocketCI <version>.
metadata:
  access: read-only
  roles: <comma-separated: ba, po, pm, dev, qa, devops, or all>
  stage: <comma-separated: plan, code, build, test, deploy, operate, or all>
---

# <Title>

<Two sentences: the question this skill settles and for whom.>

Vocabulary, tool tiers, the safety contract, and the ownership verdict come from `krci-overview`. Run its preflight before the first krci or kubectl call.

## Verdict

Start the answer with the ownership verdict from `krci-overview`: the `Owner:` line first, then `Cause`, `Evidence`, and `Next step`. The analysis follows the block.

## Procedure

1. <Read the state. Prefer krci, fall back to kubectl, say which field decides.>
2. <Classify with the table below.>
3. <Go one level deeper only for the class that matched.>

## Decision table

| Observation | Meaning | Next |
|---|---|---|
| <exact message or field value> | <cause class> | <step, or a file in references/> |

## Common mistakes

- <The trap observed in baseline testing, and what to do instead.>

## Further reading

- [<Documentation page>](https://docs.kuberocketci.io/docs/<path>)
