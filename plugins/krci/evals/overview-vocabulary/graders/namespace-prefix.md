---
type: regex
weight: 1
pattern: '(?:platform[- _]?namespace|<[^>\n]*namespace[^>\n]*>)[>`*]*-(?:payments-qa|<deployment>-<environment>|payments-<env|<cdpipeline>-<stage>)'
flags: i
match: contains
target: last_message
---

The answer gives the default environment namespace with the platform namespace as its prefix, for example `<platform-namespace>-payments-qa`, not `payments-qa`.
