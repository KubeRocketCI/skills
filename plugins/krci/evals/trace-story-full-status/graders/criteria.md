---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Does not stop at, or wait on, Jira's development panel. It names the fallback link from the story to code: the story key inside a commit's title, and proceeds from there instead of asking the user to fix Jira.
2. Covers every project on the platform, not just one: it lists all projects first (`krci project list -o json`) and then searches each project's repository for a commit whose title carries `SHOP-158`, rather than guessing a single project name or asking the user which project to check. It searches all branches of each repo, not only the default branch (for example `git log --all --grep`), so a commit that only exists on a feature branch is not missed.
3. Determines merged status per project by checking whether the commit is reachable from the project's default branch (an ancestry or "contains" check against the default branch tip), not merely that `git log --all --grep` found it somewhere.
4. Determines the first version containing the commit from tags, sorted by creation time, and explicitly accounts for two tag shapes: a semver project's tag is `build/<version>` and the version is the part after the `build/` prefix (for example `build/0.1.0-SNAPSHOT.3` means version `0.1.0-SNAPSHOT.3`), while a default-versioning project's tag equals the version directly (`<branch>-<timestamp>`). It does not treat `build/<version>` as itself the version string, and does not assume every project uses the same versioning scheme.
5. Determines which environments contain the story by ancestry, not by comparing version numbers or timestamps: for each environment's currently deployed version (from `krci project deployments <project> -o json`), it checks whether the commit is an ancestor of that version's tag (for example `git merge-base --is-ancestor <sha> <tag>` or `git tag --contains <sha>` membership), so a later or newer-looking version that came from a branch that never merged the commit is correctly excluded.
6. Before calling an environment's deployment confirmed, it checks the deployment's `status` and `operation` fields (or `sync`), not just that a `version` value is present, since a failed or unhealthy deployment is not confirmed running.

Fail if the response tells the user to fix or re-check the Jira development panel as the next step, checks only one project without first enumerating all of them, presents `build/<version>` as the version itself, or declares an environment as running the story purely because its version number or deploy timestamp is higher/later than the first version found, without an ancestry check.
