# Continuous integration

CI has no game executable: the executable is never committed or downloaded by a workflow. Verification against the executable happens on a maintainer's machine, and its result is the committed build record.

## Gates

`.github/workflows/ci.yml` runs on every pull request and every push to `main`.

- `map`: builds the `angelica` tool at the commit `tool.toml` pins and runs `angelica map check --map .`. It checks that:
  - the map loads: every file follows the format, every entry name has the form of [naming](../architecture/naming.md) and the area of its file, and every reference names an entry;
  - every file in `builds/` is a build record named `<game version>.toml`, whose `entries_sha256` equals the hash of the current map, so no entry changed without a new record;
  - every record gives every entry exactly one result, present or absent, names no other entry, and confirms constant offsets only for present fields that have one;
  - `THIRD_PARTY_NOTICES.md` exists when any entry has an `origin`.

  Whether the recorded addresses are right for the executable is checked by `angelica map verify` on a maintainer's machine, and the rest of the naming rules in review.
- `workflows`: `actionlint` (with shellcheck) and `zizmor`, with the workflow rules of the `angelica` repository.

## Failure handling

Confirm the run belongs to the current head, identify the failing step, read the logs, and fix the data or the build record rather than weakening the gate.
