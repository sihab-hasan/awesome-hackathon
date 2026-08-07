# Browser Assistant Blueprint

## Use when

A permission-minimized extension enhances the active page without leaking browsing data.

## System flow

```text
content script → message boundary → background logic → optional API → UI
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
