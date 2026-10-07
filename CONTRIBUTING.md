# Contribute to the Angelica game map

The canonical guidance lives in [`docs/`](./docs/README.md). Start with the [principles](./docs/product/principles.md) and the [contribution workflow](./docs/development/contributing.md).

## Before making a change

- Have the game executable the change is for and the pinned version of the `angelica` tool.
- Name new entries according to [`naming.md`](./docs/architecture/naming.md).
- Regenerate the build records with `angelica map verify` and commit them with the change.

## Pull requests

Follow the [pull request standards](./docs/development/pull-requests.md). The description states the game version, the entries added or changed, and which plugin or service needs them.
