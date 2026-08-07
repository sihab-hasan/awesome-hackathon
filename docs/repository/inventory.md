# Repository Inventory

## Release summary

| Item | Count |
| --- | ---: |
| Curated resources | 197 |
| Resource categories | 41 |
| Markdown documents | 316 |
| Handbook pages | 47 |
| Catalog-generated views | 72 |
| Blueprint files | 87 |
| Organizer documents | 21 |
| Judge documents | 6 |
| Playbooks | 9 |
| Checklist documents | 11 |
| Tracks | 8 |
| Prompt documents | 11 |
| Project-idea documents | 11 |
| GitHub workflows | 11 |
| Automated repository tests | 9 |
| Final files | 378 |
| Directories including root | 143 |

## Professional structure

```text
awesome-hackathon/
├── README.md                # Contents-first public entry point
├── CONTRIBUTING.md          # Contributor entry point
├── CODE_OF_CONDUCT.md       # Community expectations
├── SECURITY.md              # Vulnerability reporting
├── SUPPORT.md               # Support boundaries and routes
├── CHANGELOG.md             # Release history
├── LICENSE
├── CITATION.cff
├── VERSION
├── docs/                    # Repository, maintainer, project, and getting-started docs
│   ├── README.md            # Documentation index
│   ├── getting-started/     # Quickstart, FAQ, and stack selection
│   ├── maintainers/         # Curation, governance, quality, releases, maintenance
│   ├── repository/          # Architecture, inventory, validation, website operations
│   └── project/             # Roadmap, disclaimer, acknowledgements
├── catalog/                 # Canonical schema 2.0 resource data and generated reports
├── resources/               # Generated category pages and focused resource packs
├── handbook/                # Participant field guide
├── blueprints/              # Architectures, specs, patterns, and reference builds
├── playbooks/               # 24/48/72-hour execution and incident recovery
├── checklists/              # Planning through submission gates
├── organizers/              # Event design, delivery, safety, and reusable records
├── judges/                  # Rubric, calibration, conflicts, questions, feedback
├── tracks/                  # Focused participant routes
├── prompts/                 # Structured engineering and delivery prompts
├── project-ideas/           # Problem-first, scoped project briefs
├── community/               # Events, showcase, sponsorship, recognition policies
├── scripts/                 # Generation, search, freshness, and validation
├── tests/                   # Repository invariants and behavior tests
├── site-assets/             # Public documentation styling and browser enhancements
├── artifacts/               # Machine-readable readiness evidence
├── .github/                 # Issue forms, review templates, ownership, automation
├── mkdocs-site.yml          # Full-site Zensical configuration template
└── mkdocs.yml               # Compact handbook validation configuration
```

## Catalog dimensions

Every resource records a stable ID, category, canonical URL, factual description, tags, cost summary, source type, lifecycle status, practical use case, review date, audiences, project stages, platforms, and risk level.

The machine-readable catalog is the only source of truth for external resources. Category pages, focused packs, statistics, indexes, the search index, and the README resource excerpt are deterministic outputs.

## Release evidence

- `artifacts/repository-readiness-report.json` — machine-readable readiness status
- `SOURCE-MANIFEST.sha256` — generated during tagged releases; not committed to the source tree
- `docs/repository/validation.md` — human-readable validation evidence and boundaries
- Release-adjacent `.zip.sha256` — final archive checksum
