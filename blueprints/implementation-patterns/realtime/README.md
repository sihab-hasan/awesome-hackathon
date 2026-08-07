# Realtime Data Pattern

## Flow

Persist source of truth first, publish change event, reconcile missed events, and show connection state.

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
