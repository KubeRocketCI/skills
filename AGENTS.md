# AGENTS.md

Instructions for coding agents that work on this repository. Users of the skills never see this file: installers copy skill directories only.

## What this repository is

Agent skills for everyone who delivers software on the KubeRocketCI platform, from the ticket to production: BA, PO, PM, developers, QA, and DevOps engineers. Markdown, JSON manifests, and one Python validator with its tests. There is no build step.

[docs/architecture.md](docs/architecture.md) explains the layout, the routing, and the skill contract. `plugins/krci/skills/krci-overview` is the reference implementation of the contract. [CONTRIBUTING.md](CONTRIBUTING.md) has the steps for adding a skill and the eval format.

## Commands

```bash
python scripts/validate.py                # contract checks, needs PyYAML
python -m unittest discover -s scripts    # validator tests
npx --yes markdownlint-cli '**/*.md'     # style, config in .markdownlint.yaml
claude plugin validate . --strict         # manifest schema
claude plugin details krci@kuberocketci-skills  # context cost, after installing
claude plugin eval plugins/krci --no-publish --case '<case>*' --runs 3
```

## Layout

- `plugins/<plugin>/` is one install unit with one tool set and one safety posture. `krci` serves every delivery role. Roles are metadata, not directories.
- `plugins/<plugin>/skills/<skill>/SKILL.md` is the only place where knowledge lives. Skills stay flat, one directory each.
- `plugins/<plugin>/agents/` holds optional thin adapters that preload skills. They contain no knowledge.
- `plugins/<plugin>/evals/<case>/` holds `prompt.md` and `graders/*.md`.
- Each plugin has three manifests: `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`. Their `name` and `version` are equal.
- Both marketplaces, `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`, list every plugin. The Claude marketplace can also list role bundles: subsets of one plugin's skills, installed from the marketplace root.
- `templates/` holds the two skill shapes: `SKILL.diagnostic.md` and `SKILL.procedure.md`.
- `docs/skill-map.md` lists planned and available skills per stage and role.

## Rules

- Skill frontmatter uses only the six Agent Skills fields: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`, plus `disable-model-invocation` for procedures that only the user starts.
- `metadata` carries `access` (`read-only` or `mutating`), `roles` (`ba`, `po`, `pm`, `dev`, `qa`, `devops`, or `all`), and `stage` (`plan`, `code`, `build`, `test`, `deploy`, `operate`, or `all`).
- `mutating` means changing state outside the working tree: the cluster, the portal, a Git remote, or the ticket tracker. A skill that only writes files in the working tree is `read-only`.
- Skill names start with `krci-` and equal their directory name: hosts that install without the plugin namespace put all skills into one folder. After the prefix, a task skill name reads `<verb>-<object>`, one skill per user intent. The router `krci-overview` is the exception.
- A description says when to use the skill and which sibling takes the neighboring intent, in at most 400 characters (the router 1024). It does not summarize the procedure.
- A task skill names `krci-overview` for vocabulary, preflight, and the safety contract instead of restating them.
- A read-only skill has no state-changing command in a fenced block or a script. No skill prints secret values.
- Skill bodies name actions and platform tools (`krci`, `kubectl`, `git`), never a host's own tools.
- Check every command, flag, field, and label against the source or a real platform before writing it down. The platform repositories are under [github.com/epam](https://github.com/epam) (`edp-*`) and [github.com/KubeRocketCI](https://github.com/KubeRocketCI).
- Write eval cases before the skill and run them without it first. A case that passes without the skill is replaced. Case names start with the skill name without `krci-`.
- Role craft that does not depend on the platform (writing a story, a test plan) belongs in [KubeRocketCI/claude-plugins](https://github.com/KubeRocketCI/claude-plugins), not here.
- A change under `plugins/<plugin>/`, except in `evals/`, raises that plugin's version in all three manifests and its bundles: patch for fixes, minor for new skills or changed behavior, major for breaking changes.
- Link to [docs.kuberocketci.io](https://docs.kuberocketci.io) instead of restating documentation.
- State a constraint once, at normal volume, with its reason.
- Nothing specific to one installation: no internal hostnames, project names, or cluster names.
- Documentation describes what is in the repository. Research notes, comparisons, and decision history stay out of it.
