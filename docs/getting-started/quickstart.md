# Quick Start

## For participants

1. Read the event rules and judging criteria.
2. Choose one target user and one useful outcome.
3. Use the [stack selector](stack-selector.md) and a relevant [blueprint](../../blueprints/README.md).
4. Build the smallest vertical slice before adding integrations.
5. Run the [testing](../../checklists/testing.md), [security](../../checklists/security.md), [deployment](../../checklists/deployment.md), and [demo](../../checklists/demo-day.md) gates.
6. Submit evidence using the [final submission checklist](../../checklists/final-submission.md).

## For repository users

```bash
python3 scripts/catalog_query.py --stage build --platform web
python3 scripts/generate_catalog.py --check
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

## For organizers

Begin with the [organizer operations manual](../../organizers/README.md), [timeline](../../organizers/timeline.md), [safety process](../../organizers/safety.md), and [judging rubric](../../judges/rubric.md).

## For repository maintainers

Before the first push, follow the [GitHub push guide](../maintainers/github-push.md).
