# Blueprint Library

The blueprint library converts broad project ideas into explicit technical and delivery decisions. It does not attempt to provide one universal starter codebase.

## Structure

- [`architectures/`](architectures/) — stack-neutral and framework-specific architecture decisions.
- [`product-specs/`](product-specs/) — feature boundaries, user journeys, data models, risks, and submission scope.
- [`implementation-patterns/`](implementation-patterns/) — focused patterns for authentication, APIs, storage, payments, realtime behavior, and deployment.
- [`reference-builds/`](reference-builds/) — complete build plans connecting problem framing, architecture, delivery, testing, and demo evidence.

## Required blueprint sections

Every blueprint should define the target user, core workflow, data classification, system boundary, external dependencies, failure modes, security controls, accessibility considerations, test plan, deployment path, fallback demo, and what must be removed before production use.

## Selection rule

Choose the blueprint closest to the team’s existing skills. A hackathon is a poor time to combine several unfamiliar frameworks, databases, cloud providers, and AI systems.
