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

## Object model

A type has the name the `field` entries of its structure have in their `of`: `inventory.inventory_item`. A type's field is named for what it holds, as columns are: `class_job`, `max_health`, `position_x`; an array in the plural: `containers`, `statuses`. A field's name may differ from its entry's last word when the entry's name says how the game stores it (`at = "inventory.inventory_item.item_id"` for the field `item`). A root is named for the object plugins start from: `player`, `inventory`. An event is named for what happened, in the past tense: `action_used`; its arguments are named as fields are. A domain is named for what a player would call the data: `inventory`, `armoury`, `retainers`. An enum's values are named for what they mean in the game: `bag_1`, `crystals`. Names in the object model are stable as column names are.

## Sheet columns

A column of a sheet schema is named for what it holds, in lowercase words joined by underscores: `name`, `singular`, `description`, `level_item`. A repeated group of columns is numbered from 0 at the end: `base_param_0`, `base_param_1`. A column that refers to rows of another sheet is named for that sheet's subject: `item_ui_category`. A name is stable: renaming a column used by published plugins keeps the old name in the schema for at least one major version of the plugin API.

Names describe what the game does, in plain English words. Names from decompilers (`sub_142087C00`) and addresses are never used in names.
