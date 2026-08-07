# AI Integration Pattern

## Flow

Validate request, bound context, call provider with timeout and budget, evaluate or moderate output, and expose uncertainty.

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
