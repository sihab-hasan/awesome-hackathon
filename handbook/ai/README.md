# AI Project Engineering

AI should support a measurable user outcome rather than exist only as a feature label.

## Architecture

- Keep model credentials on the server.
- Define the exact model input, expected structured output, and fallback behavior.
- Separate retrieval, model generation, validation, and consequential actions.
- Use deterministic code for authorization, calculations, billing, and state transitions.
- Store prompts and evaluation cases with the source code.

## Evaluation

Create a small representative test set before polishing the interface. Record expected behavior, unacceptable behavior, latency, and cost. Evaluate the full workflow rather than one favorable prompt.

## Safety

- Treat model output as untrusted input.
- Isolate instructions from retrieved or user-provided content.
- Require confirmation before sending messages, making purchases, deleting data, or changing external systems.
- Disclose uncertainty and generated content where it affects user decisions.
- Avoid real sensitive data when synthetic data is sufficient.

Use the [AI safety checklist](../checklists/ai-safety.md) together with the general [security checklist](../checklists/security.md).
