# Educational Game Blueprint

## Use when

A short game loop tied to one measurable learning objective.

## System flow

```text
objective → challenge → feedback → progression → assessment
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
