# Catalog CLI Reference

Search the local resource catalog without external services:

```bash
python3 scripts/catalog_query.py ai evaluation
python3 scripts/catalog_query.py --category hosting
python3 scripts/catalog_query.py --tag open-source
python3 scripts/catalog_query.py --source official --json
```

Review catalog freshness:

```bash
python3 scripts/review_due.py
```

The source of truth is `catalog/resources.json`; human-facing lists are generated with `python3 scripts/generate_catalog.py`.
