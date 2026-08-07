# Contributing

## Before contributing

Read the [Curation Policy](docs/maintainers/curation.md), [Quality Standard](docs/maintainers/quality-standard.md), [Editorial Checklist](docs/maintainers/editorial-checklist.md), and [Code of Conduct](CODE_OF_CONDUCT.md). Search the catalog and open pull requests before proposing a duplicate.

## Resource contribution

1. Edit only `catalog/resources.json` for catalog records.
2. Use the canonical official or primary HTTPS URL.
3. Add a factual description, distinct hackathon use case, normalized tags, audiences, stages, platforms, risk level, source type, status, and current review date.
4. Disclose employment, investment, referral, sponsorship, ambassador, or project affiliation in the pull request.
5. Run catalog generation and the complete validation suite.

Do not manually edit category pages, catalog indexes, resource packs, statistics, the search index, or the generated README catalog region.

## Documentation contribution

Place participant education in `handbook/`, execution procedures in `playbooks/`, reusable structures in `blueprints/`, event operations in `organizers/`, and evaluation guidance in `judges/`. Link to canonical guidance instead of duplicating it.

Guidance should expose assumptions, prerequisites, trade-offs, failure modes, privacy, security, accessibility, safety, and the smallest useful next action. Do not present temporary pricing or service limits as permanent.

## Local validation

```bash
python3 -m pip install --requirement requirements-validation.txt
python scripts/check_all.py
```

Useful focused commands:

```bash
python3 scripts/generate_catalog.py
python3 scripts/catalog_query.py --category ai
python3 scripts/review_due.py --strict
python3 scripts/validate_structured_files.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

## Pull requests

Keep changes focused. Explain the user need, evidence, alternatives considered, generated files, affiliation, and validation performed. Generated diffs must correspond to canonical source changes.

## Commit style

Use concise conventional prefixes such as `catalog:`, `docs:`, `fix:`, `ci:`, `test:`, `security:`, or `chore:`.
