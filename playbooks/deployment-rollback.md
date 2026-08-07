# Deployment Rollback Playbook

## Trigger

Use when a new deployment fails health checks, breaks the core user journey, corrupts data, exposes secrets, or degrades the demo beyond the agreed threshold.

## Sequence

1. Freeze further deployments.
2. Identify the last verified artifact and configuration.
3. Preserve logs from the failed release.
4. Roll back code and configuration together.
5. Verify health, authentication, data access, and the demo path.
6. Announce the stable version to the team.

## Data caution

Do not reverse database migrations blindly. Prefer backward-compatible changes, backups, and forward fixes when rollback would destroy data.

## Exit criteria

The previous release is healthy, the demo script works, the failed release is documented, and no one resumes feature work without an explicit decision.
