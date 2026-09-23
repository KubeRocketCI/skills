---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Handles the fact that `krci` JSON output is not uniform: some commands wrap the payload as `{"schemaVersion": "1", "data": ...}` and others print the payload bare. Either it normalizes generically (unwrap `.data` only when `schemaVersion` is present) or it correctly treats `krci project list` as a bare array and `krci env get` as enveloped under `.data`.
2. Reads the applications of the environment from `.data.projects[]` (fields `name`, `status`) for `krci env get`.
3. Does not rely on the exit code of `krci auth status` to detect a missing session, because that command exits 0 when unauthenticated. The guard inspects standard output for the `Authenticated` status line instead.

Fail if the response assumes `.data` for `krci project list`, or uses `krci auth status || ...` or `$?` of `krci auth status` as the guard.
