# Contributing

A good contribution is small: one skill, or one correction to a skill, with the eval that proves it. Read [docs/architecture.md](docs/architecture.md) first. It explains the layout, the routing, and the [skill contract](docs/architecture.md#skill-contract) that CI enforces. For a new skill, open an issue with the requests it should serve and the requests it leaves to its siblings.

## Set up

```bash
python -m venv .venv && . .venv/bin/activate
pip install pyyaml
```

Markdown lint runs with `npx --yes markdownlint-cli '**/*.md'`. Evals and manifest checks need [Claude Code](https://code.claude.com/docs). Everything else runs without an AI host.

## Add a skill

1. Find the skill's row in [docs/skill-map.md](docs/skill-map.md), or pick its stage and roles. Name it `krci-` plus its intent as `<verb>-<object>`, for example `krci-debug-build`. One skill per user intent.
2. Copy a template to `plugins/krci/skills/<name>/SKILL.md`: `templates/SKILL.diagnostic.md` for a skill that reads state and ends with a verdict, `templates/SKILL.procedure.md` for a skill that produces an artifact or walks through steps. Set `metadata.access`, `metadata.roles`, and `metadata.stage`.
3. Write eval cases in `plugins/krci/evals/<skill-without-krci>-<trap>/` and run them without the skill. Keep the failures, they are what the skill has to teach.
4. Write the skill against those failures. Check every command, flag, field, and label against the source or a real platform.
5. Mention the skill in `krci-overview` (section "Related skills", under its roles), in the README table (under its stage), and in `docs/skill-map.md`.
6. If a role bundle exists for one of its roles, add the skill to that bundle in `.claude-plugin/marketplace.json`.
7. Raise the plugin version in all three manifests and in its bundles (not needed for a change that touches only `evals/`): patch for fixes, minor for new skills or changed behavior, major for breaking changes.

## Evals

A case is a directory in the format of `claude plugin eval`:

```text
<case>/
├── prompt.md          # frontmatter: name, tags, max_turns, allowed_tools. Body: the user request
└── graders/*.md       # frontmatter: type, weight. Body: the pass criteria
```

- Tag the case with the skill it covers.
- The prompt is what a user would type. It does not name the skill.
- One case per trap the skill prevents, plus a pressure case for every rule that must hold under pressure.
- Criteria are observable in the answer: a command that appears or does not, a field that is read, a verdict line.
- Grader `type` is `llm` for judgment. `claude plugin eval` also offers `regex`, `tool_used`, `tool_order`, `file_exists`, and `baseline`: prefer `regex` for checks that are plain text, such as a command that must not appear.
- Run every case three times per arm and report the pass counts.

```bash
claude plugin eval plugins/<plugin> --no-publish --case '<case>*' --runs 3
```

Runs use your own account and cost tokens, so filter to your cases. `--no-publish` keeps the report on your machine. Results land in `evals/results/`, which Git ignores.

## Check

```bash
python scripts/validate.py
python -m unittest discover -s scripts
npx --yes markdownlint-cli '**/*.md'
claude plugin validate . --strict
```

`validate.py` prints the description characters that stay in every session. Keep the number in the pull request when it grows.

## Pull requests

- One commit per pull request, with a [Conventional Commits](https://www.conventionalcommits.org) subject, for example `feat(krci): add krci-debug-pipeline skill`.
- Put the eval scores with and without the plugin into the pull request.
- Keep installation-specific data out: no internal hostnames, project names, cluster names, or log lines copied from a private system.

## Report a problem with a skill

Open an issue with the request you made, the host and model you used, what the agent did, and what it should have done. A wrong fact in a skill is a bug.
