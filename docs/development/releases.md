# Releases

Installed Angelica updates its game map from this repository's releases, independently of Angelica's own releases. The contract is owned by the angelica repository: `docs/development/releases.md` (map updates) and `docs/formats/update-feed-v1.md` (the feed and `map.pack`).

## Versions

A map version is `<year>.<month>.<number>` without leading zeros, such as `2026.10.1`, a SemVer version that sorts by release: the month's first release is `.1`, the next `.2`. A release is the tag `v<version>` on a commit of `main`.

## Publishing

1. Merge the change to `main` with its build record (`angelica map verify --write`).
2. Tag the merge commit and push the tag:

   ```text
   git tag -a v2026.10.1 -m "Game map 2026.10.1" <merge-commit>
   git push origin v2026.10.1
   ```

3. `.github/workflows/release.yml` builds the `angelica` tool from the angelica repository's `main`, packs the map with `angelica release map` into `map.pack`, signed with the release key (the repository secret `ANGELICA_RELEASE_SIGNING_KEY`; its public half is the repository variable `ANGELICA_RELEASE_PUBLIC_KEY`), writes the `map.json` feed, and publishes the release marked *latest*.

Installed Angelica reads the feed 20 seconds after the game starts and every hour and installs a newer map at once. A published version is never re-tagged; fix problems with the next version.
