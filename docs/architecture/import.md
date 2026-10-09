# Imported data

An entry may start from data maintained outside this repository: a community description of the game's types, functions, and fields. Imported data is a starting point; it becomes part of the map only through the same verification as any other entry.

## Importing an entry

`angelica map import` reads a local copy of a supported source and proposes an entry for a name the maintainer requests:

| Source data | Proposed entry |
| --- | --- |
| function signature | `function` with a `signature` locator; ABI from the source's parameter and return types |
| virtual function index | `function` with a `vtable` locator, and the `vtable` entry from the type's vtable signature |
| static address signature | `global` with a `signature` locator |
| field offset | `field` with a constant `offset` |
| names of functions at known addresses of a game version | hints for `angelica map recover`; never addresses in the map |

## Rules

- Entries are imported on demand, for a name a plugin or a service needs. The repository does not hold a bulk copy of any source.
- An imported entry records `origin = { source = "<source>", commit = "<commit>" }`.
- The thread of an imported function is `main` unless verified otherwise. The host refuses a hooked call from another thread, so a wrong declaration fails visibly instead of corrupting state.
- A constant offset is replaced by a code-anchored locator when one is found: a function whose behaviour is understood well enough to document reads the field, and `angelica exe signature --within` gives the instruction's signature inside it.
- Imported names are converted to this repository's [naming](./naming.md).
- A source's license notice is added to `THIRD_PARTY_NOTICES.md` with the first entry imported from it, as its license requires.
