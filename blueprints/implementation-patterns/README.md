# Implementation Patterns

Implementation patterns provide bounded examples for common capabilities without prescribing a whole application architecture.

## Pattern groups

API design, authentication, authorization, caching, databases, containers, email, file uploads, notifications, payments, realtime events, and WebSockets.

## Safety rule

Examples demonstrate integration shape, not production certification. Replace example secrets, validate all inputs, apply least privilege, configure rate limits, and confirm provider terms before public deployment.

## Review checklist

- The pattern has a clear trust boundary.
- Errors and retries are explicit.
- Sensitive data is not logged.
- External calls have timeouts and fallback behavior.
- The demo can operate with seeded or recorded data when the dependency fails.
