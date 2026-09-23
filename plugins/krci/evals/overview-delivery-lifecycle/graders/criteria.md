---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Traces the story through the ticket key: finds the branch, pull request, or commit that carries `SHOP-142`, then the build of that change and the version it produced.
2. Reads where that version runs from the platform with the krci CLI, using `krci project deployments orders` or `krci env get shop qa` and `krci env get shop prod`, and compares the reported version per environment.
3. States that KubeRocketCI 3.15 does not update Jira: the Jira steps were removed from the pipelines, so the build version is not written back to the ticket, and linking the ticket to a version is up to the team or its own Jira integration.

Fail if the response claims that the platform posts versions, links, or statuses to Jira, or invents a command such as `krci jira` or `krci ticket`.
