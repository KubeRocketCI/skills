---
name: krci-verb-object
description: <What the skill produces, one clause>. Use when <triggers, in the words users type>. Not for <neighboring intent> (use <sibling-skill>).
license: Apache-2.0
compatibility: <Required tools, or "No tools required" for a skill that only writes files>. <Optional tools>. Written against KubeRocketCI <version>.
metadata:
  access: read-only
  roles: <comma-separated: ba, po, pm, dev, qa, devops, or all>
  stage: <comma-separated: plan, code, build, test, deploy, operate, or all>
---

# <Title>

<Two sentences: what the user has at the end and for whom.>

Platform vocabulary and the safety contract come from `krci-overview`. <Keep only when the skill calls krci or kubectl:> Run its preflight before the first krci or kubectl call.

## Inputs

| Input | Where it comes from | If it is missing |
|---|---|---|
| <project name> | <krci project list, or the user> | <ask, or stop> |

## Steps

1. <Read what the platform expects: the file, field, or convention that decides.>
2. <Produce or change the artifact in the working tree.>
3. <Show the result to the user.>

## Output

<The files or text the user gets, where they go, and what the platform does with them.>

## Checks

- <How the user or the agent confirms that the result works on the platform, read-only.>

## Common mistakes

- <The trap observed in baseline testing, and what to do instead.>

## Further reading

- [<Documentation page>](https://docs.kuberocketci.io/docs/<path>)
