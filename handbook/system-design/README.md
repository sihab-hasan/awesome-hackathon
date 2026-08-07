# System Design for Hackathons

Design for the demo and a credible continuation path.

## Minimal architecture

```text
Client → application/API → primary database
                    ↘ approved external services
```

Add queues, multiple services, vector databases, or event streams only when the workflow genuinely needs them.

## Required decisions

- Source of truth for each entity
- Authentication and authorization boundary
- External API failure behavior
- Data retention and sensitive fields
- Deployment and rollback path
- Demo dataset and offline fallback

Document these decisions in a one-page architecture diagram.
