# Angelica game map guidelines

This file is the repository entry point for coding tools. Durable rules live in `docs/`; task-specific execution guidance lives in `.ai/`. Do not duplicate canonical documentation here.

This repository contains data only. The format is owned by the `angelica` repository: <https://github.com/AngelicaProject/angelica/blob/main/docs/formats/game-map-v2.md>. The tools that read and verify the map are the `angelica map` commands from that repository.

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
- A type, field, event, or action of the object model (`types/`, `roots.toml`, `events.toml`, `actions.toml`, `enums/`) is added when a plugin needs it, after `angelica look` showed in the running game that it holds what its `doc` says. It is never data that could compromise the account, keeps its name and meaning across builds, and belongs to a domain whose approved wording covers it; a number that identifies game data has its `sheet`.
- A new domain in `domains.toml`, and any change to a domain's wording or class, including its `act` wording, is approved by the maintainer.
- A field is marked `set` only when its value exists on the player's computer alone and is never sent to the game's servers, with a range the game itself tolerates.
- An outcome of a decision point returns only a value the function itself returns on a path that does nothing, checked in the disassembly.
- An action calls only a function the game's own interface calls for the player, with the arguments it passes, under the conditions the player could do it; its rate stays low.
- A column is named in `sheets/` when a plugin needs it, from the values `angelica excel show` lists, and `angelica map verify` reports its sheet as known.
- An element is named in `windows/` when a plugin needs it, after it was seen in the game to be what its `doc` says, and `angelica map verify` reports its window as known.
- Never guess an address, offset, or signature. An entry that cannot be verified stays absent.
- Prefer locators anchored in code over constant offsets.
- Imported data keeps its `origin`, and its license notice stays in `THIRD_PARTY_NOTICES.md`.
- Never commit a game executable or any other game file.
- Correctness-sensitive boundaries: locators, checks, ABI declarations, thread declarations, and renames of entries that published plugins use.
- Never claim a verification, push, or CI run succeeded unless it was actually observed.

## Project notes

- Default branch: `main`.
