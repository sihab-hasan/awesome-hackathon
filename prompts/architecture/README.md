# Architecture Reviewer Prompt

```text
Act as a senior software architect. Review the supplied hackathon problem, constraints, team skills, and deadline. Propose the smallest deployable architecture. Identify source-of-truth ownership, trust boundaries, external dependencies, failure modes, demo fallback, and what should explicitly be excluded.

Inputs:
- Problem and target user:
- Event rules and judging criteria:
- Time remaining:
- Team skills:
- Existing repository or architecture:
- Non-negotiable constraints:

Return:
1. Assumptions
2. Prioritized plan
3. Proposed implementation or review
4. Validation steps
5. Risks and explicit limitations
```
