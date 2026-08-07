# E-commerce Blueprint

## Core slice

- catalog
- search/filter
- cart
- checkout sandbox
- order confirmation

## Architecture

Use one client, one application/API boundary, one primary data store, and only the external integrations required by the core slice.

## Acceptance criteria

- New user can understand the first action.
- Main workflow completes with clear success and failure states.
- Authorization is enforced server-side.
- Seeded demo data can be reset.
- Deployed build and backup recording are ready.

## Stretch features

Add analytics, advanced search, notifications, collaboration, or personalization only after the acceptance criteria pass.
