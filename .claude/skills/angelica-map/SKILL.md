---
name: angelica-map
description: Change the Angelica game map - add a map entry an adapter needs, a type, field, root, event, action, or domain of the object model, or a named sheet column, or bring the map up to a new game build on patch day - verified against the game's executable with angelica map verify. Use for any change under entries/, types/, enums/, domains.toml, roots.toml, events.toml, actions.toml, sheets/, or builds/.
---

# Changing the game map

Work in this repository. Load `AGENTS.md`, `.ai/development.md`, and `.ai/git.md` first. The format is owned by the angelica repository: `docs/formats/game-map-v2.md` there; the host's use of the map: `docs/architecture/game-map.md`.

The commands below are the `angelica` tool from an angelica checkout (`cargo build --release -p angelica-cli`, then `target/release/angelica`); `<game folder>` is the installed game's `game` folder, with `ffxiv_dx11.exe`.

## Before adding anything

- Add data only because a plugin or host service needs it now; name that consumer in the commit.
- Names follow `docs/architecture/naming.md`. A name never changes meaning; a changed meaning retires the name.
- Community research may suggest where to look (`docs/architecture/import.md`: keep `origin` and the notice). Never depend on it, never guess, and describe entries in game terms, never by other projects' plugins.
- Nothing that could take over the account (session tokens, login data) is ever mapped.

## Entries (`entries/<area>.toml`)

1. Find the code: `angelica exe disasm` at an address or entry, `angelica exe find` for a signature's matches, `angelica exe signature --within` for a unique signature that survives moved code.
2. Prefer locators anchored in code over constant offsets. A constant offset is acceptable only with a doc stating what was checked; bind it to code once the function's purpose is understood well enough to write an honest `doc`.
3. Declare ABI and thread as the entry format requires; the `doc` says what the function or field is, in game terms.

## The object model (`types/`, `enums/`, `roots.toml`, `events.toml`, `actions.toml`, `domains.toml`) and sheet columns (`sheets/<Sheet>.toml`)

- A type's fields are `field` entries of its structure; describe the type, check it with `angelica schema show <type> --map . --game <game>` and a query with `angelica query`, then read it in the running game with `angelica look "<query>" --installation <installation>` (a development build) and compare with what the game shows. A field keeps its name and meaning across builds; a number that identifies game data has its `sheet`.
- An event is a `function` or `location` entry whose arguments a plugin watches. To find the code an action of the player reaches, count candidate entries with `angelica look --trace <entry> --trace <entry> --installation <installation>` while doing it in the game; to find which bytes of an object change, save `angelica look --dump <bytes> "<path>" --json` before and after and compare them with `angelica look --compare <before> <after>`. Describe the arguments by position (a function) or register (a location), check with `angelica schema show <event>`, then see it fire with `angelica look --watch 10 "<event> { … }" --installation <installation>`.
- A field plugins may change gets `set`, with a `range`, only when the value exists on the player's computer alone (camera, what is drawn), never one the game sends to its servers; its domain needs approved `change` wording.
- An action is a function of the main thread that the game's own interface calls for the player. Find the call the interface makes (`angelica look --trace` while doing it by hand), check in the disassembly what the caller passes in each register, and describe every argument once: a parameter with its meaning, a constant the interface passes, a global, or an object a path reaches. Give it the conditions under which the player could do it (`when`, paths that must reach an object, such as `activity[in_combat = false]`), a low `rate`, and `ok` when the function returns whether the game took it. Its domain needs approved `act` wording. Check with `angelica schema show <action>` and `map verify`, which reports a condition path that does not fit.
- A field belongs to a domain whose approved wording covers it; a new domain or wording is the maintainer's decision. An array whose elements belong to different domains by a field's value has a `partition`.
- A column is named from what `angelica excel show <Sheet> --game <game> --map . --row <row>` lists, by type and values, under the layout fingerprint `show` prints.

## Verify and record

```text
angelica map verify --map . --game "<game folder>"
angelica map verify --map . --game "<game folder>" --write
```

Every changed entry must be present, every touched sheet known. `--write` regenerates `builds/<version>.toml`; never edit `builds/` by hand, and commit the record with the data.

To try it in the running game: from the angelica checkout, `angelica dev install --key <dev key> --installation <installation> --map <this checkout>` (no `--runtime`); the host reloads sheet schemas and the object model within a second. Entries that hooks use change only at the next game start.

## Patch day

Follow `docs/architecture/patch-day.md`: verify, locate the absent entries with `angelica exe`, check each against the code of the new build, re-name sheet columns for changed layouts, re-verify with `--write`, and list in the pull request what changed, what stays absent, and which plugins wait for it.
