# Map principles

1. **Verified or absent.** An entry is present for a build only when `angelica map verify` resolved it against that build's executable. There is no hand-written address.
2. **Needed, not collected.** An entry exists because a plugin or a host service uses it. The map is not a catalog of everything known about the game.
3. **Anchored in code.** A locator that the tools can resolve again on the next build (a signature, a vtable slot, an operand of a matched instruction) is preferred over a constant. Constant offsets are listed in every build record so they stay visible.
4. **One meaning per name.** An entry name means the same thing in every build. When the game changes what a function or field does, the entry gets a new name and the old one is retired instead of being pointed at something else.
5. **Names are stable.** Renaming an entry that published plugins use keeps the old name as an alias, as the format requires.
6. **Provenance is kept.** An entry that started from external data records its `origin`, and the license notice the source requires is kept.
7. **Correct ABI and thread.** The arguments, return kind, and thread of a function entry describe the game's real function. A wrong declaration corrupts the game's state, so it is reviewed as carefully as the locator.
