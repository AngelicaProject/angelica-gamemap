# Patch day

The map is updated for a new game build without changes to Angelica or to plugins.

1. **Verify.** Run `angelica map verify --json` against the new executable. Present entries need nothing more; the report lists absent entries with reasons.
2. **Recover.** Run `angelica map recover` for the absent entries. It proposes new locators by matching each lost function's fingerprint from the previous build against the new one.
3. **Confirm.** Every proposal is checked against the decompilation of the new build: the function does what the entry's `doc` says, and its ABI and thread are unchanged. If the meaning changed, the entry is retired and a new name is introduced (see [`../product/principles.md`](../product/principles.md)).
4. **Fix the rest.** Entries that recovery could not propose are located by hand from the decompilation, preferring locators anchored in code.
5. **Sheets.** `angelica map verify` also reports every sheet schema whose sheet changed layout as unknown. For each, `angelica excel show <sheet> --map .` shows the new layout's fingerprint and columns; the maintainer finds each named column in the new layout by its type and values and adds a layout with the new fingerprint and positions. A column that is gone, or whose meaning changed, is retired as an entry would be.
6. **Re-verify.** Run `angelica map verify` again and commit the entries with the regenerated build record for the new version.
7. **Publish.** Merging publishes the map. Entries that are still absent stay absent; plugins that do not need them already work.

The pull request lists the entries that changed, the entries that remain absent, and the plugins that wait for them.
