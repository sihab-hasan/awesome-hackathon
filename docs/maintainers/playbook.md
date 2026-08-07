# Maintainer Playbook

## Maintainer responsibilities

Maintainers protect editorial independence, schema stability, link quality, contributor safety, and deterministic generation. They review evidence rather than popularity, marketing claims, or sponsor pressure.

## Pull-request review sequence

1. Confirm the contribution fits the repository scope.
2. Check affiliation and conflict disclosure.
3. Verify the canonical URL, source type, description, and specific hackathon use case.
4. Compare the proposal with existing entries to prevent duplication.
5. Check price, account, region, quota, license, privacy, and age restrictions when relevant.
6. Run generation, structured validation, repository validation, freshness checks, and tests.
7. Review generated diffs for accidental churn.
8. Request focused corrections or approve with a clear rationale.

## Resource review outcomes

- **Accept:** evidence is current and the resource fills a distinct need.
- **Revise:** the resource is useful but metadata, scope, or disclosure is incomplete.
- **Merge:** an existing entry already represents the same canonical resource.
- **Deprecate:** still referenced for migration context but no longer recommended for new work.
- **Archive:** unavailable, abandoned, unsafe, or no longer verifiable.
- **Reject:** promotional, duplicative, harmful, misleading, or outside scope.

## Scheduled maintenance

Weekly automation checks freshness metadata and links. Monthly maintenance reviews recurring failures, stale categories, security notices, policy changes, and generated-page drift. Each release records material catalog and governance changes.

## Security and abuse

Security reports use private advisories. Do not request secrets or sensitive participant data in public issues. Remove exposed credentials from repository history, rotate them at the provider, preserve minimal incident evidence, and document remediation without republishing secrets.

## Release procedure

1. Update `VERSION`, `CHANGELOG.md`, `pyproject.toml`, and `CITATION.cff`.
2. Run `python scripts/check_all.py` from a clean checkout.
3. Confirm the documentation build and scheduled-link configuration.
4. Tag `v<version>` only after review approval.
5. Verify the release archive, checksum, source manifest, and provenance attestation.
6. Record known external-link limitations in the release notes.

## Access management

Grant least privilege. Review inactive maintainers periodically. Require branch protection, review for workflow changes, protected release environments, and independent approval for changes to security, governance, or release automation.
