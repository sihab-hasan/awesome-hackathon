# Live Operations Board Blueprint

## Use when

Events update a shared operational view with stale-state and reconnect handling.

## System flow

```text
event → validate → project → stream → render → recover
```

## Repository shape

```text
src/
├── application/
├── domain-or-features/
├── adapters/
├── configuration/
├── observability/
└── tests/
```

## Required quality gates

- One complete vertical slice runs from a clean environment.
- Inputs, permissions, and external responses are validated.
- Secrets remain outside source control and client bundles.
- Failure, timeout, empty, and reconnect states are visible.
- Seeded fixtures or a simulator make the demo reproducible.
- The README explains architecture, setup, limitations, and fallback behavior.

## Demo gate

A judge can understand the state change, outcome, and limitation without developer-only tooling.
