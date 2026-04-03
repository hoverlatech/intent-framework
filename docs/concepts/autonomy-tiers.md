# Autonomy Tiers

## What It Is

Autonomy Tiers (A0 through A4) define how much authority AI agents have over a given piece of work. They specify who decides, who executes, and who reviews. The scale moves from full human control (A0) to agent execution under strict automated gates (A4).

Every task in the INTENT Framework has an assigned autonomy tier. This assignment depends on risk classification, proof tier, and the specific Constitution rules governing the domain.


## Why It Exists

Giving agents unrestricted authority is reckless. Requiring human approval for every line of code is slow. Autonomy Tiers let you calibrate the balance based on risk and confidence.

The key insight: autonomy is not binary. Between "the agent does nothing" and "the agent does everything" lies a spectrum of useful collaboration modes. A team might let agents implement UI components with human review (A2) while requiring humans to lead payment system changes (A0). Autonomy Tiers make these decisions explicit and consistent.


## The Tiers

| Tier | Name | Agent Authority | Human Role | Typical Use |
|------|------|----------------|------------|-------------|
| A0 | Suggest | Proposes options; humans execute | Decision-maker | High-risk changes, architecture decisions |
| A1 | Draft | Drafts artifacts; humans edit | Author/editor | New features, complex refactors |
| A2 | Implement | Implements changes; humans review before merge | Reviewer | Standard feature work, bug fixes |
| A3 | Operate | Executes with exception-focused review | Auditor | Low-risk changes with strong proof |
| A4 | Execute | Merges and deploys under strict automated gates | Monitor | Automated maintenance, well-proven paths |


## Tier Details

### A0: Suggest

The agent provides analysis, options, and recommendations. Humans make all decisions and execute all changes. The agent is a research assistant, not an implementer.

**When to use:** Constitution violations, new architecture patterns, new external dependencies, high-risk domains (auth, payments, PII handling).

**Agent output:** Analysis documents, option comparisons, risk assessments, draft proposals for human review.

### A1: Draft

The agent produces draft artifacts (code, specs, configurations) that humans review, edit, and finalize. The human is the author; the agent accelerates the drafting process.

**When to use:** New feature development in medium-risk areas, complex refactoring, API contract changes.

**Agent output:** Draft code, draft Intent Contracts, draft test suites. All require human editing before acceptance.

### A2: Implement

The agent writes production-ready code and tests. Humans review the output before it merges. This is the most common autonomy tier for everyday development work.

**When to use:** Standard feature implementation, bug fixes, test additions, most medium-risk and low-risk work.

**Agent output:** Complete pull requests with code, tests, and documentation. Humans review and approve.

**Common pairing:** P1 x A2 is the most frequent combination in practice. Automated tests provide a safety net, and human review catches issues that tests miss. This delivers meaningful speed improvement while maintaining quality oversight.

### A3: Operate

The agent executes changes with minimal human oversight. Humans review exceptions, anomalies, and flagged items rather than every change. This requires strong proof foundations (P2+) and well-defined boundaries.

**When to use:** Low-risk changes with established patterns, automated dependency updates, well-proven workflows.

**Agent output:** Merged changes with audit trails. Humans receive summaries and review flagged items.

### A4: Execute

The agent independently merges, deploys, and monitors changes under strict automated gates. Humans monitor dashboards and intervene only when alerts fire. This requires the highest proof tier (P4) and comprehensive automated verification.

**When to use:** Automated maintenance tasks, deployments with full canary and rollback automation, systems with closed-loop telemetry validation.

**Agent output:** Deployed changes with full telemetry. Humans monitor production metrics and respond to anomalies.


## Escalation Rules

Three conditions trigger automatic escalation regardless of the current autonomy tier:

| Condition | Escalation Target | Rationale |
|-----------|-------------------|-----------|
| Constitution violation detected | A0 (always) | Non-negotiable governance boundary |
| New dependency or architecture pattern | A0 minimum | Structural decisions require human judgment |
| Agent confidence below project threshold | One tier lower | Uncertainty demands more human involvement |

Escalation is always toward more human control (lower tier number). An agent at A3 that detects low confidence drops to A2. An agent at A2 that encounters a Constitution concern drops to A0.

These escalation rules are enforced by the framework, not left to agent discretion. Agents cannot override escalation triggers.


## Autonomy and Risk

The [Risk Classification](risk-classification.md) directly constrains available autonomy tiers:

| Risk Level | Maximum Autonomy (BUILD) | Maximum Autonomy (RUNTIME) |
|-----------|-------------------------|---------------------------|
| High | Humans lead, agents assist (A0-A1) | Narrow envelope, fast escalation |
| Medium | Agents implement, humans review (A2) | Bounded categories, explicit escalation |
| Low + strong proof | Exception-review autonomy (A3-A4) | Expanded authority within validated envelope |

Your [Constitution](constitution.md) defines the specific maximums for your organization. The table above provides general guidance.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Proof Plan section assigns the autonomy tier |
| [Constitution](constitution.md) | Sets maximum autonomy per risk level; violations force A0 |
| [Proof Tiers](proof-tiers.md) | Higher proof enables higher autonomy |
| [Risk Classification](risk-classification.md) | Risk level constrains maximum autonomy |
| [Runtime Governance](runtime-governance.md) | Trust Envelope boundaries map to autonomy authority |
| [Phases](phases.md) | Autonomy tier selected in FRAME, enforced throughout |
| [Drift Detection](drift-detection.md) | Detected drift may trigger autonomy reduction |


## Practical Guidance

**Start at A2 for most teams.** If your team is new to agent-assisted development, A2 (implement with human review) is the safest starting point. It delivers meaningful speed gains while keeping humans in the approval loop.

**Earn higher autonomy through proof.** Moving from A2 to A3 is not a team decision alone. It requires demonstrable proof (P2+ with strong Scenario Bank coverage) that the agent produces reliable output in that domain. Track agent accuracy over time before increasing autonomy.

**Autonomy is per-task, not per-agent.** The same agent might operate at A3 for CSS changes and A0 for database migrations. Autonomy is scoped to the specific work and its risk profile, not to the agent's general capability.

**Watch for autonomy creep.** Teams sometimes informally increase agent authority without updating the formal tier assignment. Regular audits during the LEARN phase catch this. If agents are effectively operating at A3 but formally assigned A2, either formalize the upgrade (with appropriate proof) or enforce the boundary.

**Use escalation data to calibrate.** If an agent at A2 rarely has changes rejected in review, it may be ready for A3 in that domain. If an agent at A3 frequently triggers exceptions, it should drop to A2. Let the data guide tier adjustments.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Uniform autonomy | Same tier for all work regardless of risk | Assign tiers per task based on risk classification |
| Autonomy without proof | High autonomy without corresponding verification | Require proof tier minimums for each autonomy level |
| Rubber-stamp reviews | A2 assigned but reviews are perfunctory | Track review quality; add review checklists |
| Escalation suppression | Agents or teams ignoring escalation triggers | Enforce escalation through tooling, not policy |
| Tier as status | Teams treat higher autonomy as a prestige marker | Frame autonomy as risk management, not achievement |


## Template Reference

See `templates/intent-contract.md` for the Proof Plan section where autonomy tiers are assigned per Intent Contract.
