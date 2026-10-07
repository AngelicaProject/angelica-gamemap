# Naming

An entry name is lowercase dotted words: `<area>.<subject>[.<member>]`. Words inside a part use underscores.

## Areas

An area groups entries about one part of the game and is the name of its file in `entries/`. Areas are added when the first entry needs one. Examples of the intended granularity:

- `excel`: the game's Excel data in memory: pages, rows, resolvers.
- `text`: game strings and text functions.
- `resource`: loading game files.
- `ui`: game windows, their nodes, and agents.
- `character`: characters, their models, and their equipment.
- `action`: using actions.
- `inventory`: containers and items.

## Subjects and members

- A function that belongs to a game type is `<area>.<type>.<function>`: `excel.store_row.hash_table`, `text.utf8_string.to_upper`.
- A vtable is `<area>.<type>.vtable`; a slot used as a function gets its own function entry with a `vtable` locator.
- A field is `<area>.<type>.<field>`: `ui.unit_base.name`.
- A patch is named for what it changes, not for its bytes: `ui.chat_log.skip_length_check`.

Names describe what the game does, in plain English words. Names from decompilers (`sub_142087C00`) and addresses are never used in names.
