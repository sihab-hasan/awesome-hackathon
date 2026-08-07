# API Pattern

## Flow

Validate input, apply authorization, execute use case, map known errors, and return a correlated response.

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
