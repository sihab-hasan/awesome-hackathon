# Release Process

## Versioning

The repository uses semantic versioning for its maintained data model and tooling:

- Major: incompatible schema, governance, or generator changes.
- Minor: substantial resource, guide, playbook, or automation additions.
- Patch: corrections, link replacements, and non-breaking documentation changes.

## Release checklist

1. Update `VERSION` and `CHANGELOG.md`.
2. Regenerate catalog views with `python3 scripts/generate_catalog.py`.
3. Run `python3 scripts/validate_repository.py`.
4. Run placeholder and Python syntax checks.
5. Build documentation with `zensical build --strict`.
6. Confirm the scheduled external-link workflow is healthy.
7. Create an annotated `vX.Y.Z` tag; use a signed tag when repository signing is configured.
8. Let the release workflow produce the ZIP archive and SHA-256 checksum.
9. Review the generated release notes and assets.

## Rollback

If a release contains broken generated data, unsafe guidance, or a schema regression, publish a correcting patch release. Do not silently replace immutable release assets.
