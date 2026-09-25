---
type: llm
weight: 1
---

Pass only if the response does all of the following:

1. Handles the fact that `krci` JSON output is not uniform: some commands wrap the payload as `{"schemaVersion": "1", "data": ...}` and others print the payload bare. Either it normalizes generically (unwrap `.data` only when `schemaVersion` is present) or it correctly treats `krci project list` as a bare array and `krci env get` as enveloped under `.data`.
2. Reads the applications of the environment from `.data.projects[]` (fields `name`, `status`) for `krci env get`.
3. Detects a missing session with a guard that fails when the session is missing, expired, or rejected: the non-zero exit code of `krci auth status` (krci v0.16.0 and later exit 1 without a valid session), optionally combined with a check of its output.

Fail if the response assumes `.data` for `krci project list`, or uses a guard that passes without a valid session.
