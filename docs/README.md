# Game map documentation

This repository contains the data of the game map. The format and the tools are owned by the `angelica` repository; this documentation owns the rules for the data and for maintaining it.

## Start here

- [Product](./product/README.md) — the rules every entry follows.
- [Architecture](./architecture/README.md) — repository layout, naming, patch day, and imported data.
- [Development](./development/README.md) — contribution workflow, review, and CI.

## Find documentation by task

| Task | Read first |
| --- | --- |
| Add an entry | [`product/principles.md`](./product/principles.md), [`architecture/naming.md`](./architecture/naming.md); an agent working on a plugin follows [`.ai/adding-entries.md`](../.ai/adding-entries.md) |
| Update the map after a game patch | [`architecture/patch-day.md`](./architecture/patch-day.md) |
| Start an entry from externally maintained data | [`architecture/import.md`](./architecture/import.md) |
| Understand the file format | [game map format v2](https://github.com/AngelicaProject/angelica/blob/main/docs/formats/game-map-v2.md) |
| Prepare a branch, commit, or pull request | [`development/git.md`](./development/git.md), [`development/pull-requests.md`](./development/pull-requests.md) |
| Review a change | [`development/code-review.md`](./development/code-review.md) |
| Investigate CI | [`development/ci.md`](./development/ci.md) |
| Write or reorganize documentation | [`development/documentation.md`](./development/documentation.md) |

## Source-of-truth rule

Put each durable rule in the document that owns it and link to it elsewhere. Rules about the format belong to the `angelica` repository.
