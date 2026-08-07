# Resource Lifecycle

## States

- **Active** — maintained, reviewed within policy, and recommended for its stated use case.
- **Deprecated** — still reachable but no longer recommended for new projects; a replacement should be documented.
- **Archived** — retained only for historical context and excluded from default recommendations.

## Intake

New proposals enter through the resource issue form. Maintainers verify identity, canonical URL, source type, relevance, duplication, terms, pricing summary, access requirements, safety considerations, and the proposed category metadata.

## Review

A review updates `reviewed_on` only after a human checks the resource itself—not merely the HTTP status. The reviewer confirms that the description and best-use statement remain accurate.

## Monitoring

Weekly link checks identify unavailable or redirected URLs. Scheduled catalog-review automation identifies entries approaching the 180-day editorial-review limit. Security reports can trigger immediate quarantine or removal.

## Deprecation and removal

A resource may be deprecated when maintenance slows, terms change substantially, the product is superseded, or the project no longer fits the stated use case. Remove resources that become malicious, deceptive, illegal, or persistently unavailable.

## Provenance

Catalog pull requests provide a visible audit trail. Release archives include checksums. Generated files are never edited directly; their origin remains `catalog/resources.json`.
