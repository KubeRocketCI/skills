## What and why

<!-- One or two sentences. For a new skill: its stage and roles, which user requests it serves, and which it leaves to its siblings. -->

## Evals

| Case | Without plugin | With plugin |
|---|---|---|
| | 0/3 | 3/3 |

<!-- claude plugin eval plugins/<plugin> --no-publish --case '<case>*' --runs 3 -->

## Checklist

- [ ] Commands, flags, fields, and labels were checked against the source or a real platform
- [ ] `metadata.access`, `roles`, and `stage` are correct, a mutating skill has its confirmation gate
- [ ] Nothing company-specific: no internal hostnames, project names, cluster names, or private log lines
- [ ] The router `krci-overview`, the README table, `docs/skill-map.md`, and matching role bundles mention a new skill
- [ ] Plugin version bumped in all three manifests and its bundles
- [ ] `python scripts/validate.py`, its tests, and `claude plugin validate . --strict` pass. Description characters: <from validate.py>
