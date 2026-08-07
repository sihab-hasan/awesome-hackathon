# AI Safety Checklist

- [ ] The user benefit and acceptable failure behavior are documented.
- [ ] Model output is treated as untrusted and validated before use.
- [ ] Authorization, calculations, and irreversible state changes remain deterministic.
- [ ] Retrieved documents and user content cannot silently override system policy.
- [ ] Consequential external actions require explicit confirmation.
- [ ] Sensitive or regulated data is not sent to an unapproved provider.
- [ ] The interface discloses generated content and material uncertainty.
- [ ] A representative evaluation set covers success, refusal, malformed input, and adversarial input.
- [ ] Timeouts, rate limits, cost limits, and provider outages have visible fallback behavior.
- [ ] Demo claims match the tested system rather than an idealized capability.
