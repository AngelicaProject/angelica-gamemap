# Patch day

The map is updated for a new game build without changes to Angelica or to plugins.

1. **Verify.** Run `angelica map verify --json` against the new executable. Present entries need nothing more; the report lists absent entries with reasons.
2. **Locate.** Absent entries are located by hand from the decompilation of the new build, preferring locators anchored in code. `angelica exe disasm` shows the code at an address or entry, `angelica exe find` checks a signature, and `angelica exe signature` proposes one that survives moved code.
3. **Confirm.** Every new locator is checked against the decompilation: the function does what the entry's `doc` says, and its ABI and thread are unchanged. If the meaning changed, the entry is retired and a new name is introduced (see [`../product/principles.md`](../product/principles.md)). An entry absent because a `contains` check failed means a fact of the game's code that an adapter relies on changed; the adapter's section in the `angelica` repository ([game structures](https://github.com/AngelicaProject/angelica/blob/main/docs/formats/game-structures.md)) says what the fact means. The check's signature is updated only when the new code keeps the same fact; when the fact itself changed, the adapter changes in Angelica first, and the entry stays absent until then.
4. **Sheets.** `angelica map verify` also reports every sheet schema whose sheet changed layout as unknown. For each, `angelica excel show <sheet> --map .` shows the new layout's fingerprint and columns; the maintainer finds each named column in the new layout by its type and values and adds a layout with the new fingerprint and positions. A column that is gone, or whose meaning changed, is retired as an entry would be.
5. **Re-verify.** Run `angelica map verify` again and commit the entries with the regenerated build record for the new version.
6. **Publish.** Merge, then tag the merge commit with the next map version ([releases](../development/releases.md)); installed Angelica picks the map up within the hour. Entries that are still absent stay absent; plugins that do not need them already work.

The pull request lists the entries that changed, the entries that remain absent, and the plugins that wait for them.
