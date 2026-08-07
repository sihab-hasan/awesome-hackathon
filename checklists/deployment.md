# Deployment Checklist

Use this list as a release gate. Record unresolved items as explicit risks rather than silently skipping them.

- [ ] Production environment variables configured securely.
- [ ] Database migrations reviewed and backed up.
- [ ] Health endpoint and runtime logs available.
- [ ] Resource limits or provider quotas understood.
- [ ] Custom domains and certificates verified if used.
- [ ] Rollback artifact identified.
- [ ] Smoke test executed after deploy.
- [ ] Demo URL tested from a separate device or network.

## Sign-off

Record the owner, timestamp, tested artifact, and any accepted exception.
