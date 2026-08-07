# Authentication and Authorization

Authentication proves identity; authorization decides what that identity may do.

## Hackathon-safe baseline

- Use a maintained provider or framework.
- Prefer secure server-managed sessions or well-understood token flows.
- Keep secrets server-side.
- Enforce authorization on the server for every protected action.
- Separate admin functions from regular user functions.
- Add logout and session-expiry behavior.
- Seed demo accounts without publishing real credentials.
