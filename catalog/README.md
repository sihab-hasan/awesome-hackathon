# Catalog System

`resources.json` is the canonical resource dataset. Every category page, report, search index, and focused pack is generated from it.

## Files

- `resources.json` — reviewed resource records
- `schema.json` — machine-readable catalog contract
- `categories.json` — generated category metadata
- `search-index.json` — offline search dataset
- `packs/` — generated task-oriented resource selections
- `INDEX.md` and reports — generated human-readable views

## Workflow

1. Edit `catalog/resources.json`.
2. Run `python3 scripts/generate_catalog.py`.
3. Run `python3 scripts/validate_repository.py`.
4. Run `python3 -m unittest discover -s tests -v`.
5. Submit the data and generated views together.

Generated files must not contain manually maintained resource metadata.
