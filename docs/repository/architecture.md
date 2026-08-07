# Repository Architecture

## Purpose

This repository separates curated external resources from original operational guidance. The catalog is the source of truth for external links; generated category pages and README excerpts must never be edited manually.

## Information architecture

```text
docs/         Repository operations, maintainer policy, project metadata, and start-here documentation
catalog/      Machine-readable resource records, schema, indexes, and generated reports
resources/    Generated category pages and focused packs
handbook/     Participant guidance from discovery through submission
blueprints/   Architecture decisions, product specifications, patterns, and reference builds
playbooks/    Time-boxed execution and incident-recovery procedures
checklists/   Stage gates for planning, implementation, safety, deployment, and submission
organizers/   Event design, operations, safety, judging, and submission management
judges/       Calibration, conflicts, scoring, questions, and feedback practice
tracks/       Focused routes for AI, data, mobile, web, hardware, and social impact
prompts/      Structured prompts for planning and implementation support
project-ideas/ Problem-first briefs with scope, evidence, risks, and validation paths
community/    Contribution, showcase, event, sponsorship, and recognition policies
scripts/      Deterministic generation, search, freshness, and validation tools
tests/        Repository behavior and catalog invariants
```

## Source-of-truth rules

1. Add or change an external resource only in `catalog/resources.json`.
2. Regenerate derived views with `python3 scripts/generate_catalog.py`.
3. Treat `resources/<category>/README.md`, catalog indexes, search indexes, packs, statistics, and the generated README catalog region as build outputs.
4. Keep participant education in `handbook/`, operational procedures in `playbooks/`, and reusable solution structures in `blueprints/`.
5. Keep repository-operation and maintainer documentation under `docs/` so the project root stays limited to standard GitHub entry files.
6. Do not duplicate the same guidance under multiple top-level folders. Link to the canonical page instead.

## Change flow

```text
Proposal → evidence and disclosure → catalog or documentation edit
→ generation → semantic validation → tests → review → merge → scheduled re-review
```

## Stability boundaries

The public catalog schema is versioned. Resource IDs remain stable when names or URLs change. Generated paths use category slugs. Breaking schema changes require a migration script, a changelog entry, and a major repository release.

## Quality boundaries

The repository does not claim that every external resource is free, available in every country, suitable for regulated data, or operationally reliable. Each entry records a current use case and review date; users must verify terms, quotas, licenses, privacy, and availability for their event and jurisdiction.
