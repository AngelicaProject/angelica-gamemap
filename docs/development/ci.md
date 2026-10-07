# Continuous integration

CI has no game executable: the executable is never committed or downloaded by a workflow. Verification against the executable happens on a maintainer's machine, and its result is the committed build record.

## Gates

- The map parses with the pinned `angelica` tool, and every entry follows the format and the naming rules.
- Every entry named in a build record exists, and every entry has a result in the build record of each supported game version.
- The `entries_sha256` of every build record equals the hash of the current map, so no entry changed without a new record.
- `THIRD_PARTY_NOTICES.md` exists when any entry has an `origin`.
- Workflows pass `actionlint` and `zizmor`, with the workflow rules of the `angelica` repository.

## Failure handling

Confirm the run belongs to the current head, identify the failing step, read the logs, and fix the data or the build record rather than weakening the gate.
