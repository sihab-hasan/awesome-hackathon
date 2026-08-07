# Final Validation Report

## Status

### PASSED — Awesome Hackathon v1.0.0 end-state repository

Validation date: **2026-08-07**

## Repository evidence

- 197 curated resources
- 41 normalized resource categories
- 316 Markdown documents
- 47 participant-handbook pages with complete navigation
- 72 deterministic catalog-generated views
- 87 blueprint files across architectures, product specifications, implementation patterns, and reference builds
- 21 organizer operations documents and templates
- 6 judge operations documents
- 9 execution and recovery playbooks
- 11 checklist documents
- 11 GitHub workflows
- 9 automated repository tests
- 378 final repository files
- 143 directories including the repository root

## Passed checks

### Catalog and curation

- JSON Schema Draft 2020-12 validation
- Schema version 2.0 field enforcement
- Unique stable resource IDs
- Unique global resource names
- Unique canonical URLs
- Valid HTTPS URLs with no tracking parameters
- Valid source types, statuses, audiences, stages, platforms, and risk levels
- Official/source-type consistency
- Normalized tags and category slugs
- Active-resource editorial review age within 180 days
- Resource issue-form categories synchronized with the catalog

### Generated repository views

- All 41 category pages exist
- Search index resource count matches the catalog
- Catalog reports, focused packs, category indexes, and README catalog excerpt are synchronized
- Generator idempotence passed
- No legacy duplicate `awesome/`, `templates/`, `starter-kits/`, `examples/`, or `docs/` trees remain

### Documentation and structure

- Internal Markdown links resolve
- Every handbook Markdown page is represented in `mkdocs.yml`
- Full public-site generation maps all 316 repository Markdown documents into the web documentation
- Generated full-site navigation contains all 316 source pages plus the complete documentation map with no duplicate or missing paths
- Navigation contains no missing pages
- Required governance, security, support, contribution, quality, architecture, and maintenance documents exist
- Organizer, judge, participant, blueprint, playbook, checklist, track, prompt, and project-brief layers are separated by responsibility
- No unresolved placeholders, empty files, escaping symlinks, embedded/nested Git metadata in the distributed source, environment-specific paths, CRLF line endings, trailing whitespace, or committed Python caches
- Live repository validation correctly ignores the checkout root `.git` directory and untracked local caches while continuing to validate tracked source files
- Review-date validation is timezone-data independent and works on standard Windows Python installations without a system IANA timezone database
- Repository-writing scripts emit deterministic UTF-8/LF text on Windows, macOS, and Linux

### Automation and release

- JSON, YAML, and CFF parsing passed
- Python source compilation passed
- Repository unit tests passed: 9/9
- Required CI, documentation, link, security, dependency, lint, spelling, freshness, Pages, and release workflows exist
- Unsafe `pull_request_target` and overbroad `write-all` permissions are prohibited by validation
- Version consistency passed across `VERSION`, `pyproject.toml`, `CITATION.cff`, and the README badge
- Release workflow produces an immutable archive, SHA-256 checksum, release-time source manifest, and provenance attestation

## Validation commands

```bash
python3 -m pip install --requirement requirements-validation.txt
python3 scripts/generate_catalog.py --check
python3 scripts/check_placeholders.py
python3 scripts/review_due.py --strict
python3 scripts/validate_structured_files.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

## External validation boundaries

External URLs, service availability, prices, quotas, licenses, regional eligibility, event legitimacy, and privacy terms can change after release. The scheduled link workflow checks live URLs continuously; editorial review remains necessary.

The strict documentation build is enforced by CI. It was not executed in the generation environment because the configured internal package registry did not expose the pinned documentation package. The release environment independently validated the complete 316-page source mapping, generated 317-page navigation (including the complete map), structured configuration, repository internal links, and all repository tests.
