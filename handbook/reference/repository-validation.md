# Repository Validation Reference

Run the complete dependency-free source validation:

```bash
python3 -m compileall -q scripts
python3 scripts/generate_catalog.py --check
python3 scripts/check_placeholders.py
python3 scripts/review_due.py
python3 scripts/validate_repository.py
```

The checks cover catalog types and uniqueness, review freshness, generated views, internal Markdown links, documentation navigation, release version consistency, required governance files, workflow safety rules, empty files, JSON syntax, and repository-local paths.

External URL availability is intentionally handled by the scheduled Lychee workflow because network access and rate limits vary by environment.
