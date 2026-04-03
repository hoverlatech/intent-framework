# Constitution

## What It Is

The Constitution is the supreme governing document for your project or organization within the INTENT Framework. It defines non-negotiable rules that every AI agent interaction, every code change, and every deployment must comply with. No Intent Contract, no automation, no agent decision can override the Constitution.

Think of it as the set of invariants your system must always satisfy. Architecture principles, security requirements, testing standards, and agent boundaries all live here. When an agent encounters a conflict between its task and the Constitution, the Constitution wins. Always.


## Why It Exists

Agent-assisted development introduces a new class of governance challenge. Agents can generate code quickly, but they lack organizational context. They do not inherently know that your company never stores PII in logs, or that all API endpoints require authentication, or that database migrations must be backward-compatible.

The Constitution solves this by making implicit organizational knowledge explicit and machine-readable. It serves three purposes:

1. **Guardrails for agents.** Agents check their work against Constitution rules before proposing changes. Violations trigger automatic escalation to human review (A0).

2. **Consistency across teams.** When multiple teams use the framework, the Constitution ensures shared standards. No team can independently decide to skip authentication on internal endpoints.

3. **Auditability.** Every decision has a traceable path back to governing principles. When something goes wrong, you can identify whether the Constitution was followed or violated.


## Structure

A Constitution typically contains these sections:

| Section | Purpose |
|---------|---------|
| Architecture Principles | Foundational technical decisions (e.g., microservices, event-driven) |
| Security Requirements | Authentication, authorization, data handling, encryption standards |
| Reliability Standards | Uptime targets, failover requirements, data durability |
| Testing Standards | Minimum coverage, required test types, CI/CD gate criteria |
| Agent Boundaries | What agents can and cannot do without human approval |
| Risk Classification | Default risk tiers for different types of changes |
| Proof Tier Thresholds | Minimum proof tiers per risk level |
| Autonomy Policy | Maximum autonomy tiers per risk level |
| Runtime Governance Requirements | When Trust Envelopes and Escalation Contracts are mandatory |
| Amendment Process | How the Constitution itself gets updated |


## Constitution as Escalation Trigger

One of the most important properties of the Constitution is its role in the escalation system. When any agent detects a potential Constitution violation, the work automatically escalates to A0 (human decision-making). This is not configurable and not overridable.

This means:

- An agent working at A3 (operate with exception review) that encounters a Constitution conflict drops to A0 immediately
- CI/CD pipelines that detect Constitution violations block deployment regardless of other passing checks
- Runtime systems that detect Constitution violations trigger alerts and, depending on severity, may halt operations

This hard escalation boundary is what makes the Constitution effective. Without teeth, it becomes documentation that agents ignore.


## Writing Effective Constitution Rules

Good Constitution rules are:

- **Specific and testable.** "All API endpoints must require authentication" is testable. "Security is important" is not.
- **Scoped appropriately.** Constitution rules apply to everything. If a rule only applies to one service, it belongs in that service's Intent Contract, not the Constitution.
- **Stable.** Constitution rules should change infrequently. If you are amending the Constitution every sprint, the rules are too specific.
- **Enforceable.** Every rule should have a corresponding check, whether automated in CI, validated at runtime, or verified during human review.


## How It Relates to Other Concepts

The Constitution sits at the top of the governance hierarchy. Everything else operates within its boundaries.

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Must comply with Constitution; cannot override it |
| [Proof Tiers](proof-tiers.md) | Constitution sets minimum proof tiers per risk level |
| [Autonomy Tiers](autonomy-tiers.md) | Constitution sets maximum autonomy per risk level; violations force A0 |
| [Risk Classification](risk-classification.md) | Constitution defines risk tier criteria |
| [Runtime Governance](runtime-governance.md) | Constitution is the top of the governance stack (Constitution > Trust Envelope > Escalation Contract > Interaction State Model) |
| [Drift Detection](drift-detection.md) | Constitution violations are the highest-severity drift category |
| [Phases](phases.md) | Constitution is established before or during FRAME; consulted in every phase |


## Runtime Governance Stack

For live agent systems, the Constitution is the apex of a four-layer governance hierarchy:

1. **Constitution** (non-negotiable rules)
2. **Trust Envelope** (authorized output boundaries)
3. **Escalation Contract** (paths to human involvement)
4. **Interaction State Model** (valid states and transitions)

Each layer must conform to the layer above it. A Trust Envelope cannot authorize outputs that the Constitution prohibits. An Escalation Contract cannot skip escalation for Constitution violations. See [Runtime Governance](runtime-governance.md) for full details on the lower three layers.


## The Amendment Process

Constitutions are not immutable, but changes should be deliberate. A good amendment process includes:

1. **Proposal.** Any team member can propose a change with rationale.
2. **Impact analysis.** Identify all Intent Contracts, agents, and systems affected.
3. **Review.** Senior engineering leadership reviews the proposal.
4. **Approval.** Changes require explicit sign-off from designated approvers.
5. **Rollout.** Update all affected systems, agents, and CI/CD configurations.
6. **Communication.** Notify all teams of the change and its implications.

Avoid the trap of making the amendment process so heavy that teams work around the Constitution instead of updating it.


## Practical Guidance

**Start small.** Your first Constitution does not need 50 rules. Start with the 10 things that would cause real damage if an agent got them wrong. Expand over time based on incidents and learnings.

**Make it machine-readable.** If agents need to check their work against the Constitution, the rules need to be in a format agents can parse. Structured YAML or JSON sections alongside prose explanations work well.

**Test your Constitution.** Write scenarios that intentionally violate Constitution rules and verify that your CI/CD pipeline, runtime governance, and agent escalation systems catch them.

**Review quarterly.** The LEARN phase may surface Constitution gaps. Schedule regular reviews, but resist the urge to add rules reactively after every incident. Look for patterns first.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Aspirational rules | Rules describe ideals, not enforceable standards | Rewrite as testable requirements |
| Over-specificity | Rules are so detailed they change constantly | Move specific rules to Intent Contracts |
| No enforcement | Constitution exists but nothing checks compliance | Add CI validators and runtime checks |
| Amendment avoidance | Teams work around outdated rules | Streamline the amendment process |
| Copy-paste Constitution | Adopted from another org without adaptation | Customize to your actual architecture and risk profile |


## Template Reference

See `templates/constitution.md` for a starter Constitution template with example rules and guidance comments.
