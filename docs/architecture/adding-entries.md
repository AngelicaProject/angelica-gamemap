# Add what a plugin needs

A plugin reads and changes the game only through the map. When the map lacks a field, an event, or an action that a plugin needs, the plugin's author, or the coding agent working for them, can add it here and send it as a pull request. The plugin can use the new entry on the author's own computer right away, and on players' computers once the map is released.

This page is the workflow. The rules every entry follows are in [`AGENTS.md`](../../AGENTS.md) and [principles](../product/principles.md); names follow [naming](./naming.md).

## What you need

- The game, and Angelica installed in it.
- The `angelica` command, and a clone of this repository.
- A disassembler that your agent can drive. For anyone: [Ghidra](https://github.com/NationalSecurityAgency/ghidra/releases) 12.0 or later with [ReVa](https://github.com/cyberkaida/reverse-engineering-assistant) (Apache-2.0), an MCP server inside Ghidra. With IDA Pro: [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) (MIT), or the [Hex-Rays IDA MCP server](https://github.com/HexRaysSA/ida-mcp) for IDA 9.4 and later.

Never commit the game's executable or anything taken from it but the entry itself.

## Set up Ghidra and ReVa

1. Install a Java runtime that Ghidra supports, then unpack Ghidra 12.0 or later.
1. Download the ReVa release for your Ghidra version and install it with **File > Install Extensions** in Ghidra's project window. Restart Ghidra.
1. In the project window, select **File > Configure**, then **Configure all plugins**, and turn on **ReVa Application Plugin**.
1. Create a project, import `ffxiv_dx11.exe` from the game's `game` folder, and let the analysis finish. It takes a while on the first import.
1. In the Code Browser, select **File > Configure**, then **Configure all plugins**, turn on **ReVa Plugin**, and select **File > Save Tool**.
1. Connect your agent to ReVa. For Claude Code:

   ```text
   claude mcp add --scope user --transport http ReVa -- http://localhost:8080/mcp/message
   ```

   ReVa listens on port 8080 of this computer while Ghidra runs. Keep it on `localhost`: its tools include a scripting environment.

## Turn on dev mode

Dev mode lets `angelica look` read the running game and lets Angelica use a map you are working on instead of the released one. It gives plugins nothing more. Turn it on in Angelica under **Settings > For developers**, or:

```text
angelica dev mode on --installation "%LOCALAPPDATA%\Angelica"
```

While it is on, a note at the top right of the screen says **Dev mode is on**.

## Find it in the running game

Start from what the map already has. `angelica schema search <words> --map .` lists the roots, types, and fields near what you need.

- `angelica look --dump 512 "<path>" --installation <installation> --json > before.json`, then do the thing in the game, dump again into `after.json`, and run `angelica look --compare before.json after.json`: the bytes that changed are where the value lives.
- `--follow <offset>` follows a pointer the map does not describe yet, from the object the path reaches: `--dump 256 --follow 0x1A8 "player"`.
- `--writes <offset> --size <bytes> "<path>"` lists the instructions that write a field while you play, by their offset in the executable. Open that offset in the disassembler: the instruction just before it wrote the field. This finds both the code that changes a value and an anchor for the field's offset.
- `--trace <entry>` counts how often the game reaches a function of the map, to find the one an action of yours calls.

All of these run against the game on your computer only.

## Find it in the code

Ask your agent to read the function in Ghidra (through ReVa) or IDA, and to check every number against the code: the offset an instruction reads, the size of an array the code walks, the arguments a call passes. Then turn what it found into an entry:

1. Write the entry in the area's file in `entries/`, and the type, field, event, or action in the object model, as [naming](./naming.md) and the format describe.
1. Locate it in code, not by a constant: `angelica exe signature --game <game folder> --rva <offset>` proposes a signature for a function or location, and `--within` one for an `in` locator that reads a field's offset. `angelica exe find` shows every match of a signature.
1. Verify the map against your game:

   ```text
   angelica map verify --map . --game "<game folder>" --write
   ```

   Every entry you added must be present.
1. Try it in the game:

   ```text
   angelica map try --map . --installation "%LOCALAPPDATA%\Angelica"
   ```

   Angelica switches to your map within a second. `angelica look "<query>" --installation <installation>` reads your new field; check that it holds what its `doc` says. Entries that hooks use, such as events, take effect at the next start of the game.
1. Run the plugin against it. A plugin that reads the new field works on your computer now.

`angelica map try --clear --installation <installation>` goes back to the released map.

## Send it

1. Run `angelica map check --map .`, as CI does.
1. Open a pull request with the entry and the build record. Say which plugin needs it and how you checked it in the game.

A reviewer checks that the entry follows the rules, that a field fits the approved words of its domain and exposes nothing that could compromise the account, and that an action calls only what the game's own interface calls. A new domain, or new words for one, waits for the maintainer's approval; an action gets the strictest review. Once the map is released, the plugin works for every player.

If you cannot add it yourself, file an [API request](https://github.com/AngelicaProject/angelica/blob/main/docs/plugins/api-requests.md) instead.
