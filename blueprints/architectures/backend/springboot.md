# Spring Boot Blueprint

## Use when

Java service or enterprise sponsor challenge.

## Suggested stack

Spring Boot + validation + persistence.

## Repository shape

```text
src/
├── application-or-routes/
├── features-or-domain/
├── integrations/
├── configuration/
├── observability/
└── tests/
```

## Required production habits

- Typed and validated configuration
- Health/readiness signal where applicable
- Structured errors and request correlation
- Secret-free source control
- One automated core-flow test
- Deterministic seed or fixtures
- Deployment and rollback instructions

## Demo gate

A clean user can complete the core workflow on the deployed build without developer intervention.
