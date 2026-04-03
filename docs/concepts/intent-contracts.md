# Intent Contracts

## What It Is

An Intent Contract is the primary specification artifact in the INTENT Framework. It replaces traditional user stories, PRDs, and feature specs with a single, outcome-centric document that captures what needs to be true when work is complete.

Where a user story says "As a user, I want to reset my password," an Intent Contract asks: what problem does password reset solve, what does success look like in measurable terms, what are the failure modes, and what level of proof do we need?

Intent Contracts serve both humans and agents. They are structured enough for AI agents to act on autonomously, and clear enough for engineering leaders to review and approve quickly.


## Why It Exists

Traditional specs have three recurring problems in agent-assisted development:

1. **Ambiguity tolerance.** User stories leave room for interpretation. That works when a senior engineer fills in the gaps with judgment. It fails when an AI agent fills them in with hallucination.

2. **Missing failure paths.** Most specs describe the happy path. Intent Contracts require at least one failure scenario, forcing teams to think about what goes wrong before code ships.

3. **Disconnected governance.** Risk classification, proof requirements, and autonomy levels typically live in separate documents (or nowhere). Intent Contracts bundle these decisions with the feature definition itself.


## Structure

An Intent Contract contains the following sections:

| Section | Purpose |
|---------|---------|
| Problem Statement | Who is affected, current state, impact of inaction |
| Desired Outcomes | Measurable success criteria |
| Constraints and Non-Goals | Explicit boundaries on scope |
| User Context | Who the users are and how they interact with the system |
| Quality Bar | Performance, accessibility, reliability expectations |
| Scenarios | Minimum 3, including at least one failure case |
| Proof Plan | Risk tier, proof tier, autonomy tier for this work |
| Runtime Governance Context | Trust Envelope and escalation considerations if applicable |
| Open Questions | Unresolved items that need answers before or during BUILD |
| Review Checklist | Verification criteria for human reviewers |


## The Problem Statement

The problem statement follows a structured format:

- **Who** is affected (specific user segment or system component)
- **Current state** describing the existing behavior or gap
- **Impact of inaction** explaining what happens if the problem is not solved

This framing forces clarity. If you cannot articulate the impact of inaction, the work may not be worth doing.


## Desired Outcomes

Outcomes must be measurable. "Improve the onboarding experience" is not an outcome. "New users complete account setup within 3 minutes with fewer than 2 errors" is.

Each outcome should be verifiable through the proof tier selected in the Proof Plan. If you specify a P2 proof tier, your outcomes need to be expressible as scenarios in a Scenario Bank. If you specify P4, your outcomes need to be measurable via production telemetry.


## Scenarios

Every Intent Contract includes a minimum of three scenarios:

1. **Happy path.** The standard successful flow.
2. **Edge case.** A less common but valid usage pattern.
3. **Failure case.** What happens when something goes wrong.

Scenarios in Intent Contracts feed directly into Scenario Banks during the BUILD phase. Writing them well here saves significant rework later. See the [Scenario Banks](scenario-banks.md) concept doc for the full scenario structure.


## The Proof Plan

The Proof Plan section ties together three classification decisions:

- **Risk tier** (High, Medium, Low) determines the level of human oversight required
- **Proof tier** (P0 through P4) determines the verification depth
- **Autonomy tier** (A0 through A4) determines the agent authority level

These three dimensions interact. High-risk work at P1 proof should never run at A3 autonomy. The framework provides guidance on valid combinations in the [Risk Classification](risk-classification.md), [Proof Tiers](proof-tiers.md), and [Autonomy Tiers](autonomy-tiers.md) docs.


## Runtime Governance Context

If the feature involves a live agent system (chatbot, automated workflow, autonomous service), the Intent Contract must reference or define:

- Which Trust Envelope categories apply
- What escalation classes are relevant
- Whether new interaction states are introduced

This section can reference existing runtime governance artifacts or flag that new ones need to be created during BUILD. See [Runtime Governance](runtime-governance.md) for details.


## How It Relates to Other Concepts

Intent Contracts are created during the **FRAME** phase and refined during **EXPLORE**. They are the input to BUILD and the reference point for VALIDATE.

| Concept | Relationship |
|---------|-------------|
| [Phases](phases.md) | Created in FRAME, refined in EXPLORE, validated against in VALIDATE |
| [Constitution](constitution.md) | Must comply with all Constitution requirements |
| [Proof Tiers](proof-tiers.md) | Proof Plan section selects the target tier |
| [Autonomy Tiers](autonomy-tiers.md) | Proof Plan section sets agent authority |
| [Risk Classification](risk-classification.md) | Proof Plan section classifies risk |
| [Scenario Banks](scenario-banks.md) | Scenarios seed the Scenario Bank |
| [Runtime Governance](runtime-governance.md) | Runtime section references governance artifacts |
| [Drift Detection](drift-detection.md) | Contract serves as the baseline for drift checks |


## Practical Guidance

**Start with the problem, not the solution.** If your team jumps to "we need a new API endpoint," back up. What outcome does that endpoint achieve? Who benefits? What breaks if we do nothing?

**Write scenarios before implementation details.** Scenarios clarify requirements faster than prose. If you cannot write three scenarios, you do not understand the feature well enough.

**Match proof to risk.** A low-risk copy change does not need P3 proof. A payment flow should not ship with P1. Use the risk tier to calibrate effort.

**Treat the contract as a living document.** Intent Contracts evolve during EXPLORE and BUILD. Open Questions get resolved. Scenarios get added. The LEARN phase may trigger updates based on production data.

**Use the template.** The `templates/intent-contract.md` template provides the full structure with guidance comments. Do not start from a blank page.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Solution-first contracts | Describes implementation, not outcomes | Rewrite problem statement and outcomes first |
| Missing failure scenarios | Only covers happy path | Add at least one failure scenario before approval |
| Mismatched tiers | High-risk work with low proof requirements | Review risk/proof/autonomy alignment |
| Stale contracts | Contract not updated after EXPLORE discoveries | Update during phase transitions |
| Kitchen-sink contracts | Tries to cover too many outcomes | Split into multiple contracts with clear boundaries |


## Template Reference

See `templates/intent-contract.md` for the full Intent Contract template with inline guidance.
