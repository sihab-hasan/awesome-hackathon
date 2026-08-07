# Data Projects

## Start with a data contract

Document each source, owner, license, refresh frequency, schema, missing-value behavior, geographic scope, and time range. A visually impressive dashboard cannot repair ambiguous data.

## Pipeline

```text
source → validation → normalization → analysis → presentation
```

Preserve raw inputs, make transformations reproducible, and separate calculated values from source values. Use small fixtures for tests and a deterministic demo dataset.

## Claims

Label estimates, simulated values, and generated annotations. Explain sampling limitations and avoid implying causation from correlation. For public-interest projects, include the date and provenance of displayed data.
