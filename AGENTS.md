# Angelica game map guidelines

This file is the repository entry point for coding tools. Durable rules live in `docs/`; task-specific execution guidance lives in `.ai/`. Do not duplicate canonical documentation here.

This repository contains data only. The format is owned by the `angelica` repository: <https://github.com/AngelicaProject/angelica/blob/main/docs/formats/game-map-v1.md>. The tools that read and verify the map are the `angelica map` commands from that repository.

## Context loading

Load the instruction modules that match the task:

- Any change: `.ai/development.md`
- Git branches, commits, rebases, or pushes: `.ai/git.md`
- Pull requests: `.ai/pull-requests.md`
- Code review or review feedback: `.ai/code-review.md`
- CI or workflow failures: `.ai/ci.md`
- Documentation changes: `docs/AGENTS.md`

Then load the documentation for the task:

- Rules every entry follows: `docs/product/principles.md`
- Repository layout and how data flows to players: `docs/architecture/overview.md`
- Naming entries: `docs/architecture/naming.md`
- Updating the map after a game patch: `docs/architecture/patch-day.md`
- Using externally maintained data: `docs/architecture/import.md`
- Contribution workflow: `docs/development/README.md`

## Always-on rules

- An entry is added because a plugin or host service needs it, never speculatively.
- Every change to `entries/` is accompanied by build records regenerated with `angelica map verify` against the current game executable. Never edit `builds/` by hand.
- Never guess an address, offset, or signature. An entry that cannot be verified stays absent.
- Prefer locators anchored in code over constant offsets.
- Imported data keeps its `origin`, and its license notice stays in `THIRD_PARTY_NOTICES.md`.
- Never commit a game executable or any other game file.
- Correctness-sensitive boundaries: locators, checks, ABI declarations, thread declarations, and renames of entries that published plugins use.
- Never claim a verification, push, or CI run succeeded unless it was actually observed.

## Project notes

- Default branch: `main`.
