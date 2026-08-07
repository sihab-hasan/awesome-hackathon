# Payment Pattern

## Flow

Create server-side checkout in test mode, verify signed webhook, make processing idempotent, and never trust client price.

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
