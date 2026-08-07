# Observability

A hackathon prototype needs enough visibility to diagnose the demo, not an enterprise monitoring estate.

## Minimum signals

- Structured server logs without secrets.
- Correlation or request identifiers.
- Clear client-side error states.
- Health or readiness endpoint for a backend.
- Basic latency and failure counts for the core workflow.
- External dependency failures recorded with safe context.

## Demo operations

Know where to inspect deployment logs and how to reset seeded data. Keep a short troubleshooting runbook with the three most likely failure modes and their fallback steps.
