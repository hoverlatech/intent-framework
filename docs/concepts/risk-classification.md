# Risk Classification

## What It Is

Risk Classification assigns a tier (High, Medium, or Low) to every piece of work in the INTENT Framework. This classification drives downstream decisions about proof requirements, autonomy levels, review processes, and deployment strategies. It is determined during the FRAME phase and recorded in the Intent Contract's Proof Plan.

Risk classification is not a subjective judgment call. The framework provides concrete criteria for each tier based on what the change touches and what could go wrong.


## Why It Exists

Without explicit risk classification, teams default to one of two failure modes:

1. **Treat everything as high risk.** Every change gets the same heavy review process. Velocity drops. Engineers lose trust in the process and start working around it.

2. **Treat everything as low risk.** Changes ship fast, but critical systems lack appropriate oversight. An agent modifies a payment flow with the same review process used for button color changes.

Risk Classification solves this by making the stakes explicit and tying them to concrete governance decisions. High-risk work gets more human oversight, deeper verification, and stricter deployment controls. Low-risk work moves fast with lightweight processes. The system is calibrated, not uniform.


## The Tiers

| Risk Tier | Criteria | Examples |
|-----------|----------|----------|
| High | Touches auth, payments, PII, infrastructure, safety systems | OAuth flow, billing logic, escalation logic, database migrations, encryption changes |
| Medium | User-facing features, API contract changes, schema updates | New API endpoint, dashboard workflow, search functionality, notification system |
| Low | Content, styling, docs, internal tooling | Copy updates, UI polish, internal admin tools, documentation changes |


## Classification Criteria

### High Risk

A change is high risk if it touches any of the following:

- **Authentication or authorization.** Login flows, session management, role-based access, token handling.
- **Payment processing.** Billing logic, subscription management, refund flows, financial calculations.
- **Personally identifiable information (PII).** Data collection, storage, transmission, or deletion of user data subject to privacy regulations.
- **Infrastructure.** Database schemas, deployment configurations, networking rules, service mesh changes.
- **Safety systems.** Rate limiting, abuse detection, content moderation, escalation logic in live agent systems.

High-risk changes require human leadership in the BUILD phase. Agents assist but do not lead. The maximum autonomy tier during BUILD is typically A1 (draft). Proof tier minimums are P3 or higher.

### Medium Risk

A change is medium risk if it:

- **Is user-facing.** Visible to end users in production, affecting their experience or workflows.
- **Changes API contracts.** Modifies request/response shapes, introduces new endpoints, or deprecates existing ones.
- **Alters data schemas.** Database column additions, type changes, or new relationships (that do not involve PII or auth).
- **Introduces new integrations.** Third-party API integrations, webhook handlers, or external service dependencies.

Medium-risk changes follow the standard A2 pattern: agents implement, humans review before merge. Proof tier minimums are P2.

### Low Risk

A change is low risk if it:

- **Affects only content.** Marketing copy, help text, error messages, documentation.
- **Is purely cosmetic.** CSS changes, UI polish, icon updates, layout adjustments.
- **Is internal tooling.** Developer tools, build scripts, internal dashboards with no external exposure.
- **Has no production user impact.** Test infrastructure, CI configuration, local development setup.

Low-risk changes with strong proof foundations (P1+) can operate at A3 or A4. The overhead should be minimal.


## Governed Autonomy by Risk

Risk classification directly governs how much autonomy agents receive, both during development (BUILD phase) and at runtime for live agent systems.

### During BUILD

| Risk | Agent Role | Human Role |
|------|-----------|------------|
| High | Agents assist (A0-A1) | Humans lead decisions and implementation |
| Medium | Agents implement (A2) | Humans review all changes before merge |
| Low + strong proof | Agents operate autonomously (A3-A4) | Humans review exceptions only |

### At Runtime (Live Agent Systems)

| Risk | Agent Authority | Governance Approach |
|------|----------------|-------------------|
| High | Narrow envelope, fast escalation | Tight Trust Envelope boundaries, low escalation thresholds |
| Medium | Bounded categories, explicit escalation | Defined output categories with clear escalation paths |
| Low + strong proof | Expanded authority within validated envelope | Broader Trust Envelope with telemetry monitoring |


## How to Classify

Follow this decision process during FRAME:

1. **Check the high-risk criteria first.** If the change touches auth, payments, PII, infrastructure, or safety systems, it is high risk. No exceptions.

2. **Check for user-facing impact.** If end users will see or interact with the change, it is at least medium risk.

3. **Check for contract changes.** If APIs, schemas, or integrations change, it is at least medium risk.

4. **Default to low.** If none of the above apply, classify as low risk.

5. **Consult the Constitution.** Your project's Constitution may define additional high-risk or medium-risk criteria specific to your domain. Always check.

When in doubt, classify one tier higher. It is cheaper to over-classify and relax later than to under-classify and discover the gap in production.


## Risk Can Change

Risk classification is not permanent. Several situations warrant reclassification:

- **Scope expansion.** A low-risk UI change that grows to include API modifications becomes medium risk.
- **Dependency discovery.** EXPLORE phase reveals that a feature touches auth systems not initially identified.
- **Production incidents.** LEARN phase reveals that a "low-risk" area caused significant production issues.
- **Regulatory changes.** New compliance requirements elevate the risk of previously low-risk data handling.

When risk changes, update the Intent Contract's Proof Plan. Proof tier and autonomy tier may need adjustment to match.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Risk tier recorded in the Proof Plan section |
| [Constitution](constitution.md) | Defines risk criteria and tier boundaries for the project |
| [Proof Tiers](proof-tiers.md) | Risk level sets minimum proof tier requirements |
| [Autonomy Tiers](autonomy-tiers.md) | Risk level caps maximum autonomy |
| [Runtime Governance](runtime-governance.md) | Risk level determines Trust Envelope strictness |
| [Phases](phases.md) | Classification happens in FRAME, may update in LEARN |
| [Drift Detection](drift-detection.md) | Higher risk triggers stricter drift monitoring |


## Practical Guidance

**Classify early, revisit as needed.** Risk classification happens in FRAME, but do not treat it as locked. If EXPLORE reveals new risk factors, update the classification before entering BUILD.

**Do not negotiate risk down for speed.** If a change touches payments, it is high risk regardless of deadline pressure. The framework exists precisely to prevent this kind of shortcutting.

**Use risk classification for resource allocation.** High-risk work should involve your most experienced engineers as reviewers. Low-risk work is a good training ground for newer team members and for calibrating agent autonomy.

**Track classification accuracy.** During LEARN, check whether the risk classification matched the actual impact. If medium-risk work consistently causes production issues, your classification criteria may need tightening.

**Make classification visible.** Risk tier should be visible in your project management tools, PR templates, and deployment dashboards. When everyone can see the risk level, appropriate scrutiny follows naturally.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Everything is medium | Default classification without analysis | Apply the decision process systematically |
| Risk negotiation | Lowering risk tier to reduce process overhead | Enforce classification criteria; address process complaints separately |
| Static classification | Never updating risk after initial assignment | Review classification at phase transitions |
| Missing domain risks | Generic criteria miss industry-specific concerns | Customize risk criteria in Constitution for your domain |
| Classification without consequence | Risk tier assigned but does not affect proof or autonomy | Wire risk classification to proof and autonomy tier selection |
