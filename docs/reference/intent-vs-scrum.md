# INTENT vs. Scrum

> **INTENT Framework v0.5** | Reference
>
> INTENT is not a Scrum replacement. It is a governance layer designed for teams where
> AI agents do significant execution work. This document compares the two across key
> dimensions so you can understand what changes and why.

---

## Comparison Table

| Dimension | Agile / Scrum | INTENT |
|-----------|---------------|--------|
| Fundamental unit | User story | Intent Contract |
| Cadence | Time-boxed sprints | Continuous proof-gate flow |
| QA approach | Embedded testing | Scenario Bank + Proof Tiers |
| Execution model | Humans write code | Agents execute under gates |
| Drift handling | Manual code review | Automated build/runtime/spec detection |
| Invariants | Implicit team norms | Constitution (versioned, enforced) |

---

## Dimension-by-Dimension Breakdown

### User Stories vs. Intent Contracts

In Scrum, the user story captures a need: "As a user, I want X so that Y." The story is deliberately lightweight. Implementation details emerge during sprint planning and development.

An Intent Contract captures the same need but adds structure that agents require to execute correctly: measurable outcomes, explicit constraints, non-goals, a proof plan, and risk classification. Agents cannot infer intent from a one-line story. They need boundaries, success criteria, and validation rules stated upfront.

**Why the change:** Human developers fill gaps with judgment and team context. Agents fill gaps with hallucination. The contract eliminates ambiguity before execution begins.

### Sprints vs. Proof-Gate Flow

Scrum operates in fixed time boxes (typically two weeks). Work is planned at sprint start, executed during the sprint, and reviewed at sprint end. The cadence is calendar-driven.

INTENT uses a continuous flow where work advances through phases (FRAME, EXPLORE, BUILD, VALIDATE, SHIP, LEARN) and gates between them. A feature moves from BUILD to VALIDATE not because two weeks passed, but because the proof evidence meets the gate criteria. There is no artificial deadline forcing incomplete work through.

**Why the change:** Agents can produce code in minutes, making two-week sprints an awkward fit. Gates tied to evidence quality are more meaningful than gates tied to calendar dates.

### Embedded Testing vs. Scenario Bank + Proof Tiers

Scrum teams write tests as part of development. Test strategy varies by team. Some teams have robust test suites, others rely on manual QA.

INTENT requires a Scenario Bank: a structured collection of scenarios written per Intent Contract before implementation begins. Each scenario has a risk tier (High, Medium, Low) that determines the required proof level. High-risk scenarios may require human review. Low-risk scenarios may pass with automated checks alone.

**Why the change:** When agents generate code, traditional test coverage metrics are insufficient. You need scenario-level validation that maps directly to the outcomes you specified. The Scenario Bank is the bridge between "what we intended" and "what we got."

### Human Execution vs. Agent Execution Under Gates

In Scrum, humans write code, review it, and merge it. The process trusts developer judgment within the team's norms.

INTENT assumes agents do significant execution work. Agents operate under autonomy budgets: defined limits on what they can do without human review. A low-risk UI change might execute end-to-end without human intervention. A high-risk security feature requires human review at every phase gate.

**Why the change:** Agents are fast but lack judgment. Gates and autonomy budgets replace the judgment that human developers provide implicitly.

### Manual Code Review vs. Automated Drift Detection

Scrum relies on pull request reviews and team knowledge to catch deviations from architecture and standards.

INTENT adds automated drift detection at three levels:

| Detection Level | What It Catches | When It Runs |
|----------------|-----------------|--------------|
| Build-time | Schema violations, architecture principle breaches, dependency violations | CI pipeline, every commit |
| Runtime | Behavioral drift, performance regression, trust envelope violations | Production monitoring, continuous |
| Spec-level | Contract intent vs. actual implementation mismatch | VALIDATE phase, pre-merge |

**Why the change:** Agents produce code too quickly for manual review to be the primary safety mechanism. Automated detection catches drift at machine speed.

### Implicit Norms vs. Constitution

Scrum teams develop shared norms over time: coding standards, architecture preferences, security practices. These norms live in team culture and (sometimes) wiki pages.

INTENT requires a Constitution: a versioned, enforced document that defines architecture principles, security requirements, agent boundaries, and governance rules. Every agent interaction must comply with the Constitution. Violations block progress. Amendments require a defined process.

**Why the change:** Agents cannot absorb team culture. They need explicit, machine-readable rules. The Constitution makes implicit norms explicit and enforceable.

---

## What Stays the Same

INTENT does not replace everything in Scrum. Several practices carry forward:

- **Retrospectives** still matter. The LEARN phase serves a similar function.
- **Daily coordination** still happens. Teams still need to communicate about blockers and progress.
- **Backlog prioritization** still exists. Intent Contracts need to be prioritized just like user stories.
- **Incremental delivery** is still the goal. INTENT ships features continuously, not in big-bang releases.

---

## Migration Path

If your team currently uses Scrum, you do not need to abandon it overnight.

**Week 1-2:** Start writing Intent Contracts alongside user stories for new features. Compare the two formats. Notice what the contract captures that the story does not.

**Week 3-4:** Add a Scenario Bank for one feature. Write scenarios before implementation. Run them as acceptance criteria.

**Week 5-6:** Draft your Constitution. Start with architecture principles you already follow but have never written down.

**Week 7-8:** Introduce proof gates for one workstream. Measure whether gate-based flow produces better outcomes than sprint-based deadlines.

After 8 weeks, you will have enough experience to decide how far to take the transition. Some teams adopt INTENT fully. Others keep sprint ceremonies for coordination but use INTENT artifacts for governance. Both approaches work.

---

## Related Docs

- [Roles & Team Models](./roles.md)
- [30/60/90 Rollout Plan](./rollout-30-60-90.md)
- [Quickstart Guide](../guides/quickstart.md)
