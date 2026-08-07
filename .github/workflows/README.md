# Workflows

- `ci.yml` — Python syntax, generated catalog views, schema semantics, internal links, and strict documentation build.
- `catalog-review.yml` — scheduled 180-day editorial freshness enforcement.
- `markdown-lint.yml` — Markdown style.
- `spell-check.yml` — spelling and project vocabulary.
- `link-check.yml` — scheduled and pull-request external URL checks.
- `codeql.yml` — Python security analysis with the extended query suite.
- `dependency-review.yml` — vulnerable dependency and license review for pull requests.
- `pages.yml` — strict Zensical build and GitHub Pages deployment.
- `release.yml` — validated immutable release archive and SHA-256 checksum.
- `stale.yml` — conservative inactive issue and pull-request handling.

Workflows use least-privilege permissions. Third-party actions should be pinned to a reviewed commit SHA where practical; official GitHub actions are tracked by Dependabot at their supported major versions.
