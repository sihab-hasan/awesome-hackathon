# Container Pattern

## Flow

Use a small runtime image, non-root user, health check, immutable configuration, and pinned dependencies.

## Failure cases

- Invalid or missing input
- Unauthorized caller
- Dependency timeout or quota
- Duplicate request
- Partial operation
- User retries

## Evidence to include

- Request/response or event contract
- One success test and one failure test
- Log or trace correlation
- Demo fixture and reset procedure
