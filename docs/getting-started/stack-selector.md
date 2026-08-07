# Hackathon Stack Selector

## Default rule

Use the stack with the highest team fluency that meets event rules and data constraints.

## Decision matrix

| Requirement | Preferred direction |
| --- | --- |
| Fast web prototype | Next.js, SvelteKit, Nuxt, or Vite with a managed backend |
| Python or ML-heavy logic | FastAPI service with a simple web client |
| Realtime collaboration | Firebase, Supabase Realtime, or a managed WebSocket service |
| Mobile-first | Expo/React Native or Flutter |
| Static content and forms | Astro or a static Vite site |
| Sensitive or offline data | Local-first storage or approved self-hosted services |
| Complex enterprise integration | One backend service that owns credentials and adapters |

## Rejection questions

Reject a tool when the team cannot answer:

- How is it deployed?
- Where are secrets stored?
- How is data exported or deleted?
- What happens when the service is unavailable?
- What does the free or event tier actually allow?
- Can the demo run from a clean machine?
