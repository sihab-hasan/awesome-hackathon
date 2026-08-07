# Reliability and Resilience

## Failure budget for a demo

Prioritize the few failures that could invalidate the core claim:

- deployment unavailable
- authentication failure
- external API quota or outage
- empty or malformed data
- model timeout or invalid output
- device or network disconnect

For each, define detection, user-visible behavior, recovery, and demo fallback. Use bounded timeouts, limited retries, idempotency for repeated submissions, and a circuit breaker or graceful degradation for unstable dependencies.

A recorded fallback should demonstrate the same build and workflow, not a different mockup presented as live behavior.
