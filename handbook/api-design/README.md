# API Design

- Use resource-oriented names and predictable status codes.
- Validate every input at the boundary.
- Return stable error shapes with request IDs.
- Make retried writes idempotent.
- Apply timeouts to every external request.
- Document authentication, rate limits, examples, and failure modes.
- Never expose upstream API keys to the browser.

For a hackathon, a small coherent API is better than many partial endpoints.
