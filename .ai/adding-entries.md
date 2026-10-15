# Adding what a plugin needs

Instructions for a coding agent that works on a plugin and finds that the game map lacks something it needs: a field, a type, an event, an action, a sheet column, or a window element. The plugin API is the map, so the way forward is to add it here. The plugin can use it on the user's computer as soon as you try the map locally, and on players' computers once the map is released.

Read `AGENTS.md` first: its always-on rules decide what may be added at all. Names follow `docs/architecture/naming.md`; the format is the angelica repository's `docs/formats/game-map-v2.md`.

## 0. Before you start

1. Make sure it is really missing. `angelica schema search <words> --map <map>` lists roots, types, fields, events, actions, and domains; `angelica schema show <name> --map <map>` shows one. Map work takes hours; a near miss in the schema takes minutes.
1. Tell the user in one message what is missing, that you can add it to the map, and what that involves: turning on dev mode in their Angelica, reading the running game while they play, and in the end a pull request to this repository. Wait for their agreement. Without it, write an API request instead (the angelica repository's `docs/plugins/api-requests.md`).
1. Decide its domain now (section 5): whether an existing domain covers it, whether it needs a new domain or new words, or whether it can never be offered. Tell the user which, because a new domain or new words wait for the maintainer's approval before the map is released, and an action (`act`) gets the strictest review.

## 1. Tools

Install only what the step in front of you needs. Check first; install what is missing only after telling the user what and how big, and getting their agreement.

### Always

| Tool | Check | Install |
| --- | --- | --- |
| Git | `git --version` | `winget install --id Git.Git -e` |
| GitHub CLI, signed in | `gh auth status` | `winget install --id GitHub.cli -e`, then the user runs `gh auth login` |
| Rust | `cargo --version` | `winget install --id Rustlang.Rustup -e` |
| `angelica` | `angelica --version` | `cargo install --locked --git https://github.com/AngelicaProject/angelica angelica-cli` |
| This repository | a clone you can push a branch from | `gh repo fork AngelicaProject/angelica-gamemap --clone` |
| The game and Angelica | the user's installation: `%LOCALAPPDATA%\Angelica`, and the game's `game` folder with `ffxiv_dx11.exe` | the user's; never download the game or its files |

With these you can read the running game (`angelica look`), disassemble the executable (`angelica exe`), and write, verify, and try entries. Many fields need nothing more.

### Only when needed: Ghidra and ReVa

Install them when `angelica exe disasm` is not enough to understand the code: a long function, its callers, references to a value, a vtable, strings, or a decompiled view. They are about 600 MB and the first analysis of the executable takes about 20 minutes, so do not install them for a field whose writer `look --writes` and `exe disasm` already show.

| Tool | Check | Install |
| --- | --- | --- |
| JDK 25 or later | `java -version` | `winget install --id EclipseAdoptium.Temurin.25.JDK -e` |
| Python 3.10 or later | `python --version` | `winget install --id Python.Python.3.12 -e` |
| Ghidra and ReVa | see below | see below |

Put everything in one folder outside `AppData`, here `%USERPROFILE%\angelica-tools`: some agent hosts, such as the Claude desktop app, give their processes a private copy of `AppData`, and a tool installed there is invisible to the user, while Ghidra itself fails to start its script framework.

1. Choose the versions. ReVa is built for exact Ghidra versions; take the newest ReVa release and the newest Ghidra version it has an asset for:

   ```shell
   gh release view -R cyberkaida/reverse-engineering-assistant --json tagName,assets --jq '.tagName, (.assets[].name | select(endswith("reverse-engineering-assistant.zip")))'
   ```

   An asset `ghidra_12.1.3_PUBLIC_<date>_reverse-engineering-assistant.zip` is for Ghidra 12.1.3, whose release tag is `Ghidra_12.1.3_build`.
1. Download both into a new empty folder and check them against the digests GitHub lists:

   ```shell
   gh release download Ghidra_<version>_build -R NationalSecurityAgency/ghidra -p "ghidra_<version>_PUBLIC_*.zip" -D <download folder>
   gh release download <ReVa tag> -R cyberkaida/reverse-engineering-assistant -p "ghidra_<version>_PUBLIC_*_reverse-engineering-assistant.zip" -D <download folder>
   gh release view Ghidra_<version>_build -R NationalSecurityAgency/ghidra --json assets --jq '.assets[] | .name + " " + .digest'
   ```

   Compare each file's SHA-256 (`Get-FileHash`) with its `sha256:` digest; a mismatch means the download is broken or not what it claims. A large download can break off: `curl -L -C -` resumes it from the asset's URL.
1. Unpack Ghidra into `%USERPROFILE%\angelica-tools`, then unpack the ReVa archive into Ghidra's own `Ghidra\Extensions` folder. There it is installed without Ghidra's window.
1. Make the Python environment with the PyGhidra that Ghidra ships; nothing is downloaded:

   ```shell
   python -m venv %USERPROFILE%\angelica-tools\reva-env
   %USERPROFILE%\angelica-tools\reva-env\Scripts\python -m pip install --no-index --find-links <Ghidra>\Ghidra\Features\PyGhidra\pypkg\dist pyghidra
   ```

1. Analyze the executable into a project once per game build. Copy `ffxiv_dx11.exe` into the tools folder first: Ghidra's batch files fail on a path with parentheses, such as `Program Files (x86)`. Write the labels script with `angelica map labels --map <this repository> --game <game folder> --output <scripts folder>\AngelicaMapLabels.java`; it names every entry the map already has. Then, with `APPDATA` and `LOCALAPPDATA` set to `%USERPROFILE%\angelica-tools\ghidra-settings` for the process, and in the background, since it takes about 20 minutes:

   ```shell
   <Ghidra>\support\analyzeHeadless.bat <projects folder> ffxiv -import <copied ffxiv_dx11.exe> -scriptPath <scripts folder> -postScript AngelicaMapLabels.java
   ```

   The log ends with `Analysis succeeded`, `<n> labels from the game map`, and `Save succeeded`. After a game patch, analyze the new executable into a new project.
1. Serve the project, with the same `APPDATA` and `LOCALAPPDATA`, in a terminal that stays open while you work:

   ```shell
   %USERPROFILE%\angelica-tools\reva-env\Scripts\python tools\reva\serve.py --ghidra <Ghidra> --projects <projects folder> --project ffxiv
   ```

   It prints `ReVa serves ffxiv on http://127.0.0.1:8080/mcp/message`. Keep it on this computer: ReVa's tools include a scripting environment.
1. Use it. `python tools/reva/call.py --list` lists ReVa's tools; `python tools/reva/call.py get-decompilation programPath=ffxiv_dx11.exe functionNameOrAddress=camera.camera.set_distance` decompiles a function by its map name or address. To have ReVa's tools as MCP tools in later sessions, register the server with your host, for Claude Code `claude mcp add --scope user --transport http ReVa -- http://localhost:8080/mcp/message`; it takes effect in a new session.

Ghidra places the executable at its own image base, `0x140000000` for this game; `look --writes` prints each place at that base too.

## 2. Turn on dev mode

```shell
angelica dev mode on --installation %LOCALAPPDATA%\Angelica
```

Dev mode lets `angelica look` read the running game and lets Angelica use your local map instead of the released one; plugins get nothing more. A note at the top right of the game says **Dev mode is on**. Ask the user to start the game with a character in the world.

## 3. Find it in the running game

Start from an object the map already reaches. Every command but `--compare` takes `--installation %LOCALAPPDATA%\Angelica`.

- **Where a value lives.** `angelica look --dump 512 "<path>" --json > before.json`, ask the user to change the value in the game, dump again into `after.json`, and run `angelica look --compare before.json after.json`. The bytes that changed, and their offset, are your candidate.
- **Behind a pointer.** `--dump 256 --follow 0x1A8 "<path>"` reads the object the pointer at that offset leads to; repeat `--follow` to go further.
- **Which code writes it.** `angelica look --writes <offset> --size <bytes> --seconds 45 "<path>"`, started while the user does the thing in the game, lists where each writing instruction ended, as an offset in the executable and as an address at Ghidra's image base. The instruction that ends exactly there wrote the field. This is the usual way to the function behind something the player does, and to the code that anchors a field's offset.
- **Which function an action calls.** `--trace <entry> --seconds 20` counts how often the game reaches functions of the map.

Ask the user to act only for the seconds a command runs, and say exactly what to do.

## 4. Find it in the code

- `angelica exe disasm --game <game folder> --rva <offset>` disassembles from an address to the end of its function. A small function that calls nothing often has no entry in the exception directory; its start is the first instruction after the `CC` bytes that pad the function before it.
- With ReVa: decompile, list callers (`get-callers-decompiled`), references, vtables, and strings. Check every number you write down against the instructions themselves: the offset an instruction reads, the size of an array the code walks, the arguments a call passes.
- FFXIVClientStructs may tell you where to look. Never copy from it without checking in the code and the game; an entry taken from it keeps its `origin` (`docs/architecture/import.md`).

## 5. Choose the domain

Every field, event argument, and action belongs to a domain, and the domain is what the player approves, in the domain's own words: a plugin lists it in its manifest's `[lens] read`, `[lens] act`, or `[lens] change`, and the player sees the domain's `read`, `act`, or `change` words. The words promise the player what a plugin can do with that permission, so choosing a domain is choosing what the player is told. The format of `domains.toml` is the angelica repository's `docs/formats/game-map-v2.md` (Domains); how the player sees them is its `docs/architecture/permissions.md`.

1. Read the domains: `domains.toml`, or `angelica schema search <words> --map .` and `angelica schema show <domain> --map .`, with their `doc`, `class`, and words.
1. Pick the domain whose words already say it. Read the words as a player who approved them: a player who allowed "Sees the items you carry" expects a plugin to know their bags' items and quantities, not their retainers' or their gil history. If that player would be surprised, the domain does not cover it. What it covers depends on the operation:
   - reading a field or receiving an event: its `read` words;
   - an action: its `act` words; a domain without `act` has no actions;
   - a field plugins may `set`, or an outcome at a decision point: its `change` words; a domain without `change` has nothing plugins change.
1. Check the class. `you` is about the player alone; `display` changes only what the player sees; `others` shows anything about other players, their names, messages, or characters. Data about other players never goes into a `you` domain. The host grants only these three classes: a domain of another class, such as acting toward other players, is never granted, so do not propose one for a plugin.
1. When an existing domain covers it, put the field, argument, or action in that domain (a type's `domain`, or the field's own). That needs no approval: fields join a domain under the words it already has.
1. When no domain covers it, do not stretch one. Propose a new domain in `domains.toml`, narrow, for what this kind of plugin needs, not everything near it:
   - its name is what a player would call the data, as `docs/architecture/naming.md` says (`retainers`, `armoury`);
   - `doc` says what it holds;
   - `class` is the one the data reaches, as above;
   - `read` is one plain line in English and Russian, in the form of the others ("Sees …" / "Видит …"), saying everything a plugin with it can read;
   - `act` or `change` only when the plugin needs to act or change in it, in the same form ("Uses …", "Changes …").
1. When a domain covers the reading but lacks the `act` or `change` words the operation needs, adding those words is new wording: propose them the same way.
1. A new domain or new words wait for the maintainer's approval; say so in the pull request, with the proposed words quoted, and tell the user. Meanwhile the plugin works on this computer: the local map describes the domain, so Angelica shows it to the user for approval.
1. Some data has no domain and never will: anything that could take over or compromise the account, such as session tokens or login data. Do not add it, or mark the field `forbidden = true` when the type needs it described; tell the user the plugin cannot have it, and design around it.

## 6. Write the entry

1. Put a function, location, global, or vtable in the area's file in `entries/`, a field's entry beside them, and the object model's part in `types/`, `roots.toml`, `events.toml`, `actions.toml`, or `enums/`, in the domain section 5 chose.
1. Locate it in code, never by a constant you could anchor. `angelica exe signature --game <game folder> --rva <offset>` proposes a unique signature for a function or location. For a field, take the instruction that reads or writes it and run `--within`, adding `--function <start>` when the function is a leaf: the signature is then unique inside that function and leaves out the displacement, which the `in` locator reads (`{ in = "<function entry>", signature = "...", operand = "disp" }`).
1. A function entry's `abi` and `thread` are what the disassembly shows: the registers it reads for arguments and what it returns. Declare `void` when nothing reads the return value, and `thread = "any"` unless you have seen it run only on the main thread.
1. An entry found by your own work has no `origin`. When it replaces one that had an `origin`, remove it and any sentence saying the value was still to be checked.

## 7. Verify and try

1. `angelica map verify --map . --game <game folder> --write` resolves every entry against the user's executable and writes the build record. Every entry you added is present. When an entry in code replaced a constant offset, the offset it derives equals the constant, and the record confirms one constant offset less.
1. `angelica map check --map .` must pass, as CI runs it.
1. `angelica map try --map . --installation %LOCALAPPDATA%\Angelica` puts the map into Angelica as its local map; dev mode must be on. Within a second the game uses it.
1. `angelica look "<query>"` reads what you added. Check with the user that it holds what its `doc` says, in the game. An entry that hooks use, such as an event, takes effect at the next start of the game.
1. Run the plugin against it, in the game. It works on this computer now.

## 8. Send it

1. Branch, commit, and open a pull request as `.ai/git.md` and `.ai/pull-requests.md` say: the entries, the types, and the regenerated build record; never the executable or anything taken from it. Say which plugin needs it and how you checked it in the game, with the commands you ran.
1. Tell the user it is sent, and what is left: the review, and the maintainer's approval when a domain or an action is involved.
1. When the user no longer needs the local map, `angelica map try --clear --installation %LOCALAPPDATA%\Angelica` and `angelica dev mode off --installation %LOCALAPPDATA%\Angelica`. Once the map with the entry is released, the plugin works on the released map.
