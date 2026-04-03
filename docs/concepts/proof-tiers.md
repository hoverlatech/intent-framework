# Proof Tiers

## What It Is

Proof Tiers (P0 through P4) define the depth and rigor of verification applied to a piece of work. They answer the question: how confident are we that this code does what the Intent Contract says it should?

Each tier builds on the one below it. P0 is ad hoc, inconsistent verification. P4 is continuous, production-validated proof that intent is being met. Your target tier depends on the risk classification and business criticality of the work.


## Why It Exists

Not all code needs the same level of verification. A copy change on a marketing page does not need load testing and production telemetry. A payment processing flow does.

Proof Tiers give teams a shared vocabulary for verification expectations. Instead of debating "how much testing is enough," you classify the risk, select the appropriate proof tier, and follow the tier's requirements. This is especially important in agent-assisted development, where agents can generate code faster than humans can review it. Clear proof requirements ensure that speed does not come at the expense of correctness.


## The Tiers

| Tier | Name | What It Requires | Source of Truth |
|------|------|-----------------|-----------------|
| P0 | Ad hoc | Inconsistent, manual, or missing coverage | Code |
| P1 | Repeatable | Automated checks (unit tests, linting, type checks) | Code |
| P2 | Scenario-backed | Scenario Bank validation with structured test cases | Co-evolution (code + spec) |
| P3 | Risk-calibrated | P2 + load testing, security testing, failure injection | Co-evolution (code + spec) |
| P4 | Closed-loop | P3 + production telemetry validates intent continuously | Spec governs |

Each tier is cumulative. P3 includes everything in P2, which includes everything in P1.


## The Spec Continuum

Proof Tiers also define the relationship between specifications and code, which the framework calls the Spec Continuum:

| Range | Mode | Description |
|-------|------|-------------|
| P0-P1 | Spec-guided | Code is the source of truth. Specs inform but do not govern. |
| P2-P3 | Spec-anchored | Specs and code co-evolve. Changes to one require updates to the other. |
| P4 | Spec-as-source | Specs are the source of truth. Code must conform to specs, and production telemetry continuously validates alignment. |

This continuum matters because it determines how agents treat specifications. At P1, an agent can modify code freely as long as tests pass. At P4, an agent must update specs first and then modify code to match.


## Tier Details

### P0: Ad Hoc

No consistent verification process. Testing happens when someone remembers to do it, or when a bug surfaces. This tier is the default state of most prototypes and proof-of-concept work.

**When it is acceptable:** Throwaway prototypes, spike investigations, internal experiments that will never reach production.

**When it is not acceptable:** Anything that ships to users.

### P1: Repeatable

Automated checks run on every change. This includes unit tests, linting, type checking, and basic integration tests. The CI pipeline enforces these automatically.

**What P1 requires:**
- Automated test suite with meaningful coverage
- CI pipeline that blocks merges on failure
- Linting and type checking enforced

**Common pairing:** P1 x A2 is the most common combination in practice. Agents implement code with automated checks, and humans review before merge. This delivers faster execution while maintaining a human quality gate.

### P2: Scenario-Backed

Validation is driven by a Scenario Bank that captures expected outcomes, failure modes, and state paths. Test cases map directly to scenarios defined in the Intent Contract.

**What P2 adds beyond P1:**
- Structured Scenario Bank with scenario IDs, priorities, and state paths
- Test cases linked to specific scenarios
- Failure mode coverage verified against the scenario inventory
- Scenarios updated as the system evolves

See [Scenario Banks](scenario-banks.md) for details on scenario structure and management.

### P3: Risk-Calibrated

Verification extends beyond functional correctness to include non-functional requirements like performance, security, and resilience.

**What P3 adds beyond P2:**
- Load testing against defined performance thresholds
- Security testing (dependency scanning, SAST, DAST as appropriate)
- Failure injection (chaos testing, fault tolerance verification)
- Results traced back to Intent Contract quality bar

### P4: Closed-Loop

Production telemetry continuously validates that the system meets its intent. Specifications govern, and deviations between actual behavior and specified behavior trigger automated alerts and LEARN phase reviews.

**What P4 adds beyond P3:**
- Production telemetry dashboards aligned to Intent Contract outcomes
- Automated drift detection comparing actual behavior to spec
- Alerts on deviation from expected patterns
- LEARN phase triggers when telemetry diverges from intent
- Specs updated based on production learnings

See [Drift Detection](drift-detection.md) for details on how P4 monitoring works.


## Selecting the Right Tier

Use risk classification as the primary input:

| Risk Level | Minimum Proof Tier | Rationale |
|-----------|-------------------|-----------|
| Low | P1 | Automated checks catch regressions |
| Medium | P2 | Scenario-backed validation ensures feature completeness |
| High | P3 | Non-functional verification required for critical paths |
| High + live agents | P4 | Continuous validation for systems with autonomous behavior |

These are minimums defined in your [Constitution](constitution.md). Teams can always exceed the minimum.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Proof Plan section specifies target proof tier |
| [Constitution](constitution.md) | Sets minimum proof tiers per risk level |
| [Autonomy Tiers](autonomy-tiers.md) | Higher proof enables higher autonomy |
| [Risk Classification](risk-classification.md) | Risk level determines minimum proof tier |
| [Scenario Banks](scenario-banks.md) | Required starting at P2 |
| [Drift Detection](drift-detection.md) | Build-time drift checking starts at P1; full closed-loop at P4 |
| [Phases](phases.md) | Proof tier selected in FRAME, validated in VALIDATE |


## Practical Guidance

**Default to P1 for most work.** The majority of features in a typical product are medium or low risk. P1 with good automated tests covers them well. Reserve P2+ for work that justifies the additional overhead.

**Do not skip tiers.** Going from P0 to P3 without establishing P1 and P2 foundations creates brittle, unmaintainable verification. Build the lower tiers first.

**Proof tier is not permanent.** A feature might start at P1 and move to P3 as it becomes more critical. The LEARN phase often triggers proof tier increases when production incidents reveal insufficient verification.

**Use the Spec Continuum to guide agent behavior.** At P1, agents should write tests alongside code. At P2+, agents should update Scenario Banks. At P4, agents should update specs before touching code.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| P0 in production | No consistent verification for shipped code | Establish P1 as minimum for all production code |
| Proof theater | High tier claimed but checks are superficial | Audit actual verification against tier requirements |
| Tier inflation | Everything classified as P3+ regardless of risk | Align proof tiers to actual risk classification |
| Stale scenarios | P2 claimed but Scenario Bank not maintained | Include scenario maintenance in definition of done |
