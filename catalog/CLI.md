# Catalog CLI

Search without network access:

```bash
python3 scripts/catalog_query.py ai evaluation
python3 scripts/catalog_query.py --category observability
python3 scripts/catalog_query.py --audience organizer --stage organize
python3 scripts/catalog_query.py --platform mobile --risk high
python3 scripts/catalog_query.py --source official --json
```

Filters may be combined. Text terms match names, descriptions, best-use statements, categories, tags, audiences, stages, and platforms.

The CLI reads the canonical catalog directly and never modifies repository files.
