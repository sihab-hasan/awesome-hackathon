# Security Policy

## Scope

This repository contains curated links, documentation, Python maintenance tooling, GitHub workflows, and release artifacts. Security concerns may include malicious or compromised links, exposed credentials, unsafe workflow changes, dependency compromise, generated-content injection, archive tampering, or guidance that creates material harm.

## Reporting

Use GitHub private vulnerability reporting for sensitive issues. Do not open a public issue for exposed credentials, active malicious links, workflow-injection paths, compromised release assets, private incident data, or supply-chain compromise.

A useful report includes the affected path or URL, impact, reproduction or evidence, affected versions, and a safe contact route. Do not access systems or data beyond what is necessary to demonstrate the issue.

## Response

Maintainers will acknowledge the report, restrict access to the minimum response group, assess impact, preserve necessary evidence, remove or quarantine unsafe content, rotate affected credentials, correct automation, invalidate compromised releases where possible, and publish an appropriately scoped remediation note.

## Supported versions

Security corrections are applied to the current maintained release. Historical archives remain immutable; release notes will identify affected versions and the safe replacement.

## Workflow and release controls

- Pull requests from forks receive read-only permissions.
- `pull_request_target` is prohibited.
- Release workflows use explicit permissions and protected tags or environments.
- Generated data must pass semantic validation before release.
- Release archives receive a checksum, source manifest, and provenance attestation.
- Workflow and dependency updates require review.

## Third-party resources

Inclusion is not a security endorsement. Users must review current documentation, permissions, data handling, licensing, account requirements, and incident history before using an external service with real users or sensitive data.
