---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Gives the exact command `krci env get payments qa` (deployment name then environment name as
   two positional arguments), not an invented verb or shape such as `krci get environment`,
   `krci stage get`, `krci env status`, or a single combined argument.
2. Names `status` and `sync` as two independent fields on each entry of `projects[]`: `status` for
   health, `sync` for drift against Git. Explicitly treats them as separate axes, not one combined
   "health" value.
3. Does not claim the Stage itself carries a single top-level health field; the state lives per
   project, under `projects[]`.
4. If it mentions `-o json`, correctly notes the payload may be wrapped in a
   `{"schemaVersion": ..., "data": ...}` envelope that must be unwrapped before reading `projects`.

Fail if the response invents a command or flag that does not exist in the krci CLI, conflates sync
and status into a single field, gets the argument order or count wrong, or never names the command.
