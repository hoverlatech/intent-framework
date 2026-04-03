# Phases

## What It Is

The INTENT Framework organizes work into six core phases and one optional pre-phase. These phases replace traditional sprint-based rituals with a continuous, proof-gated flow. Work moves forward when it meets the exit criteria for its current phase, not when a calendar says it should.

The phases are:

**DISCOVER** (optional) **-> FRAME -> EXPLORE -> BUILD -> VALIDATE -> SHIP -> LEARN**


## Why It Exists

Sprint-based workflows assume a predictable cadence. Two-week sprints, planning on Monday, retro on Friday. This cadence creates artificial pressure to fill time (when work is light) or cut corners (when work is heavy). It also creates awkward boundaries: a feature that is 90% done at sprint end either gets rushed or rolls over.

The INTENT Framework replaces calendar cadence with proof gates. Work flows through phases based on readiness, not scheduling. This aligns naturally with agent-assisted development, where execution speed varies dramatically depending on task complexity and autonomy tier.

The framework's second principle, "Flow over cadence," captures this directly. Continuous proof-gate progression replaces calendar rituals.


## The Phases

### DISCOVER (Optional Pre-Phase)

**Purpose:** Identify opportunities, problems, or needs before formal work begins.

**Activities:**
- Market research, user feedback analysis, technical discovery
- Problem identification and initial sizing
- Deciding whether to proceed to FRAME

**Exit criteria:** A problem worth solving has been identified with enough context to write an Intent Contract.

**When to skip:** When the problem is already well-understood (bug reports, compliance requirements, technical debt with clear scope).

### FRAME

**Purpose:** Define the intent. Create the Intent Contract that specifies what needs to be true when the work is complete.

**Activities:**
- Write the Intent Contract (problem statement, outcomes, scenarios, constraints)
- Classify risk tier
- Select proof tier and autonomy tier
- Identify runtime governance needs
- Establish the review checklist

**Exit criteria:** Approved Intent Contract with complete Proof Plan (risk tier, proof tier, autonomy tier).

**Key decisions:** This is where governance gets embedded. Risk classification, proof requirements, and autonomy levels are set here, not bolted on later. See [Intent Contracts](intent-contracts.md) for the full structure.

### EXPLORE

**Purpose:** Resolve unknowns and refine the approach before committing to implementation.

**Activities:**
- Technical spikes and prototypes
- Architecture exploration
- Dependency analysis
- Intent Contract refinement (updating scenarios, resolving open questions)
- Scenario Bank initial population

**Exit criteria:** All critical open questions from the Intent Contract are resolved. Technical approach is validated. Scenario Bank has initial entries.

**Agent role:** Agents typically operate at A0-A1 during EXPLORE, providing analysis and drafts while humans make architectural decisions.

### BUILD

**Purpose:** Implement the solution according to the Intent Contract.

**Activities:**
- Code implementation (at assigned autonomy tier)
- Test development aligned to proof tier
- Scenario Bank expansion
- Runtime governance artifact creation (if applicable)
- Continuous Constitution compliance checking

**Exit criteria:** Implementation complete. All proof tier requirements met. Scenario Bank coverage sufficient.

**Agent role:** This is where autonomy tiers have the most impact. At A2, agents produce complete PRs for review. At A3+, agents may merge and deploy within defined boundaries. Risk level determines the ceiling:

| Risk Level | Agent Role in BUILD |
|-----------|-------------------|
| High | Humans lead, agents assist (A0-A1) |
| Medium | Agents implement, humans review (A2) |
| Low + strong proof | Exception-review autonomy (A3-A4) |

### VALIDATE

**Purpose:** Verify that the implementation meets the Intent Contract requirements at the specified proof tier.

**Activities:**
- Run full Scenario Bank validation
- Execute non-functional tests (P3+)
- Verify runtime governance artifacts (if applicable)
- Compare implementation against Intent Contract outcomes
- Final human review against review checklist

**Exit criteria:** All proof tier requirements verified. Review checklist complete. No unresolved Constitution violations.

**Key distinction from BUILD:** BUILD includes continuous testing during development. VALIDATE is the formal verification gate before shipping. Even if all tests passed during BUILD, VALIDATE runs the full suite as a final check.

### SHIP

**Purpose:** Deploy the validated work to production.

**Activities:**
- Deployment execution (canary, blue-green, or direct depending on risk)
- Production smoke testing
- Monitoring setup verification
- Drift detection baseline establishment (P4)
- Rollback readiness confirmation

**Exit criteria:** Successfully deployed to production. Monitoring active. Rollback path verified.

**Agent role at SHIP:** Deployment autonomy follows the same risk-based rules. High-risk deployments require human execution. Low-risk deployments with strong proof can be agent-driven.

### LEARN

**Purpose:** Gather production insights and feed them back into the framework.

**Activities:**
- Production telemetry review
- Drift detection analysis
- Incident review (if any)
- Intent Contract retrospective (did the outcomes hold?)
- Constitution and Scenario Bank updates based on findings
- Proof tier and autonomy tier reassessment

**Exit criteria:** Learnings documented. Framework artifacts updated. Next cycle informed.

**This phase is not optional.** Teams that skip LEARN accumulate blind spots. Production behavior diverges from assumptions. Agents operate on stale context. The LEARN phase closes the loop.


## Flow, Not Cadence

Phases do not have fixed durations. A low-risk bug fix might move from FRAME to SHIP in hours. A high-risk platform change might spend weeks in EXPLORE and BUILD.

The key mechanism is proof gates, not time gates. Each phase has explicit exit criteria. When the criteria are met, work moves forward. When they are not met, the work stays in its current phase regardless of how long it has been there.

This also means multiple work items can be in different phases simultaneously. One feature might be in BUILD while another is in VALIDATE and a third is in LEARN. There is no need to synchronize phases across work items.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Created in FRAME, refined in EXPLORE, implemented in BUILD, verified in VALIDATE |
| [Constitution](constitution.md) | Consulted in every phase; established before FRAME |
| [Proof Tiers](proof-tiers.md) | Selected in FRAME, built toward in BUILD, verified in VALIDATE |
| [Autonomy Tiers](autonomy-tiers.md) | Set in FRAME, enforced in BUILD, may adjust in LEARN |
| [Risk Classification](risk-classification.md) | Determined in FRAME, governs behavior in all subsequent phases |
| [Scenario Banks](scenario-banks.md) | Seeded in FRAME/EXPLORE, expanded in BUILD, validated in VALIDATE, updated in LEARN |
| [Drift Detection](drift-detection.md) | Active in BUILD (CI), SHIP (runtime), and LEARN (spec drift) |
| [Runtime Governance](runtime-governance.md) | Defined in FRAME/EXPLORE, built in BUILD, verified in VALIDATE |


## Practical Guidance

**Do not skip FRAME.** The temptation to jump straight to BUILD is strong, especially for "obvious" work. Resist it. Even simple work benefits from a lightweight Intent Contract. The 15 minutes spent in FRAME saves hours of rework in BUILD.

**EXPLORE is not optional for uncertain work.** If the Intent Contract has more than two open questions, invest in EXPLORE. Agents are excellent at rapid prototyping during EXPLORE, operating at A0-A1 to quickly test assumptions.

**LEARN feeds the next FRAME.** Production insights from LEARN should directly inform future Intent Contracts. If LEARN reveals that a feature's actual usage differs from assumptions, the next iteration should update the Proof Plan accordingly.

**Track phase transitions.** Knowing how long work spends in each phase reveals bottlenecks. If work consistently stalls in VALIDATE, your BUILD process may need better continuous testing. If work stalls in EXPLORE, your FRAME process may need better open question identification.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Skipping FRAME | Jumping to BUILD without defining intent | Require Intent Contract before BUILD begins |
| Calendar gates | Moving phases based on schedule, not readiness | Enforce exit criteria before phase transitions |
| Skipping LEARN | Shipping and moving on without production review | Schedule LEARN reviews; track completion |
| Phase waterfall | Treating phases as strictly sequential with no iteration | Allow backflow (e.g., BUILD discoveries update EXPLORE findings) |
| Uniform pacing | Expecting all work items to move at the same speed | Accept that different risk/complexity levels have different phase durations |
