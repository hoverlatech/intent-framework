# 30/60/90 Day Rollout Plan

> **INTENT Framework v0.5** | Reference
>
> This plan gets your team from zero to a functioning INTENT practice in 90 days.
> Each phase builds on the previous one. Do not skip ahead.

---

## Overview

| Phase | Days | Focus | Key Outcome |
|-------|------|-------|-------------|
| Foundation | 1-30 | Artifacts and vocabulary | Team writes Intent Contracts and scenarios fluently |
| Enforcement | 31-60 | Gates and governance | No code merges without scenario evidence |
| Calibration | 61-90 | Autonomy and measurement | Data-driven autonomy budgets, production governance |

---

## Days 1-30: Foundation

The goal is to build fluency with INTENT artifacts. Do not try to enforce anything yet. Focus on practice.

### Write Intent Contracts for New Features

Replace user stories with Intent Contracts for every new feature starting day one. Use the template at [`templates/intent-contract-template.md`](../../templates/intent-contract-template.md).

**Practical tips:**

- Start with features currently in planning. Do not retroactively convert old stories.
- The first few contracts will feel slow. That is normal. Teams typically reach fluency by contract number 5-8.
- Focus on the "Desired Outcomes" and "Constraints" sections. These are where most value comes from.
- Have two people review each contract independently. The reviewer should be able to explain the intent without reading the code.

### Seed the Scenario Bank

Write 3-5 scenarios per Intent Contract. Use the template at [`templates/scenarios-template.yaml`](../../templates/scenarios-template.yaml).

**What makes a good scenario:**

| Quality | Example |
|---------|---------|
| Specific | "User with expired session token attempts checkout" (not "handle edge cases") |
| Measurable | "Response time under 200ms for 95th percentile" (not "should be fast") |
| Risk-tagged | Each scenario has a risk tier: High, Medium, or Low |
| Independent | Each scenario can be validated on its own |

**Practical tips:**

- Write scenarios before implementation, not after.
- Include at least one negative scenario per contract (what should NOT happen).
- High-risk scenarios should cover security boundaries, data integrity, and financial transactions.

### Define Risk Categories

Establish what High, Medium, and Low risk mean for your domain. This is project-specific.

**Example risk definitions:**

| Tier | Definition | Examples |
|------|-----------|----------|
| High | Data loss, security breach, financial impact, compliance violation | Payment processing, auth changes, PII handling |
| Medium | User-facing behavior change, performance regression, integration change | UI flow changes, API contract changes, third-party integrations |
| Low | Internal tooling, documentation, non-user-facing refactoring | Dev scripts, logging changes, code style updates |

### Draft the Initial Constitution

Use [`templates/constitution-starter.md`](../../templates/constitution-starter.md) to create your project Constitution.

**Minimum viable Constitution (start here):**

1. Architecture principles (3-5 rules)
2. Security requirements (3-5 rules)
3. Agent boundaries (what agents can and cannot do)
4. Amendment process (how the Constitution changes)

Do not try to be comprehensive on day one. The Constitution will grow as you discover new invariants.

---

## Days 31-60: Enforcement

The goal is to make INTENT artifacts load-bearing. They should block bad work from merging, not just document good intentions.

### Enforce Scenario Gates Before Merge

No PR merges without passing scenario evidence. This is the single most important enforcement step.

**Implementation approach:**

1. Add a CI check that verifies scenario files exist for the relevant Intent Contract.
2. Require scenario pass/fail evidence in the PR description or as CI artifacts.
3. High-risk scenarios require explicit human sign-off (not just automated pass).

**Common resistance and how to handle it:**

| Objection | Response |
|-----------|----------|
| "This slows us down" | Measure time-to-merge before and after. Most teams find bugs earlier, reducing total cycle time. |
| "Not every change needs scenarios" | Low-risk changes need fewer scenarios, but still need at least one. The risk tier system handles proportionality. |
| "Our agents write good code already" | Good code that does not match the intent is still wrong. Scenarios validate intent, not just correctness. |

### Draft Trust Envelope, Escalation Contract, and Interaction State Model

If your project includes agent-facing surfaces (chatbots, copilots, automated workflows), draft these three artifacts:

- **Trust Envelope** ([`templates/trust-envelope-template.md`](../../templates/trust-envelope-template.md)): What agents can do autonomously vs. what requires human approval.
- **Escalation Contract** ([`templates/escalation-contract-template.md`](../../templates/escalation-contract-template.md)): When and how agents hand off to humans.
- **Interaction State Model** ([`templates/interaction-state-model-template.md`](../../templates/interaction-state-model-template.md)): Valid states, transitions, and edge cases for agent interactions.

### Measure Scenario Health

Start tracking these metrics weekly:

| Metric | Target by Day 60 |
|--------|-------------------|
| Scenario pass rate | Above 90% |
| Coverage (scenarios per contract) | 3-5 per contract |
| Flaky scenario rate | Below 5% |
| Contracts without scenarios | Zero |

### Enable Build-Time Drift Detection

Add drift detection to your CI pipeline. At minimum, check for:

- Constitution violations (architecture principles, security requirements)
- Schema or API contract changes that do not match the Intent Contract
- Dependency additions that violate declared constraints

---

## Days 61-90: Calibration

The goal is to use accumulated evidence to make data-driven decisions about agent autonomy and governance posture.

### Calibrate Autonomy Budgets

Review scenario pass history and risk tier data to set autonomy levels.

**Autonomy tier guidelines:**

| Autonomy Level | Criteria | Agent Behavior |
|----------------|----------|----------------|
| Full autonomy | Low-risk, 95%+ scenario pass rate over 30 days | Agent executes end-to-end without human review |
| Supervised autonomy | Medium-risk, 90%+ pass rate | Agent executes but human reviews before merge |
| Guided autonomy | High-risk or insufficient evidence | Agent proposes, human approves each step |
| Manual only | Critical risk or new domain | Human executes, agent assists |

**Practical tips:**

- Start conservative. It is easier to expand autonomy than to recover from a mistake.
- Expand autonomy per feature area, not globally. Payment processing and documentation updates should have different autonomy levels.
- Document every autonomy expansion decision with the evidence that justified it.

### Instrument Runtime Governance Metrics

For projects with live agent surfaces, instrument these metrics:

| Metric | What It Measures |
|--------|-----------------|
| Unsafe-answer rate | Percentage of agent responses that violate trust envelope |
| Escalation rate | How often agents hand off to humans |
| State violation rate | Interaction state transitions that do not match the model |
| Drift detection alerts | Count and severity of detected drift events |

### Run First LEARN Phase Review

At day 90, conduct your first formal LEARN phase review. This is a structured retrospective that compares production telemetry against Intent Contract assumptions.

**Review agenda:**

1. For each shipped feature: did production outcomes match the Intent Contract's desired outcomes?
2. Where did assumptions prove wrong? Update contracts and scenarios.
3. Which autonomy decisions were correct? Which need adjustment?
4. What new invariants should be added to the Constitution?
5. What scenarios are missing from the Scenario Bank?

Document findings and feed them back into the next cycle of contracts and scenarios.

---

## After Day 90

By day 90, you have a functioning INTENT practice. From here:

- Run LEARN phase reviews monthly (or per major release).
- Continuously expand the Scenario Bank as new edge cases emerge.
- Revisit autonomy budgets quarterly.
- Consider scaling from Thin Team to Swarm if your team is growing.

---

## Related Docs

- [Roles & Team Models](./roles.md)
- [INTENT vs. Scrum](./intent-vs-scrum.md)
- [Quickstart Guide](../guides/quickstart.md)
