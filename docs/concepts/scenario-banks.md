# Scenario Banks

## What It Is

A Scenario Bank is a structured collection of scenarios that captures expected outcomes, failure modes, runtime signals, and state paths for a feature or system. It is the "intent-level memory of correctness" for your project, serving as both a validation baseline and a living record of how the system should behave.

Scenario Banks go beyond traditional test suites. A test suite tells you whether code passes or fails. A Scenario Bank tells you what correctness means: what should happen, what should not happen, what signals to watch for, and how the system should transition between states.


## Why It Exists

Traditional test suites have a coverage problem that is not about line coverage percentages. They cover the cases the developer thought of at implementation time. They rarely capture:

- Failure modes discovered in production
- Clarifications made during code review
- Edge cases found during incident response
- Runtime behaviors that require specific signal monitoring

Scenario Banks solve this by capturing scenarios from multiple sources across the entire lifecycle. A scenario might originate from an Intent Contract during FRAME, from a production incident during LEARN, or from a clarification during BUILD. All of them live in the same structured repository, linked to the features they validate.

In agent-assisted development, Scenario Banks are especially valuable. Agents can validate their work against the full scenario inventory before submitting for review. When a Scenario Bank is comprehensive, agent-generated code is more likely to be correct on the first pass.


## Scenario Structure

Each scenario in a Scenario Bank follows a defined structure:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier for the scenario |
| `name` | Human-readable name |
| `source` | Where the scenario originated (spec, clarification, production, incident) |
| `priority` | Criticality level (critical, important, edge-case) |
| `state_path` | Expected sequence of system states |
| `escalation_class` | Applicable escalation class (E0, E1, E2, EX) if relevant |
| `trust_envelope_categories` | Trust Envelope categories exercised by this scenario |
| `preconditions` | Required system state before the scenario begins |
| `steps` | Sequence of actor/action pairs |
| `expected_outcome` | What should be true when the scenario completes |
| `failure_mode` | What this scenario tests against (how it could go wrong) |
| `signals_to_capture` | Telemetry and logging requirements during execution |
| `runtime_checks` | Assertions to validate during or after execution |
| `automation_status` | Whether the scenario is automated, manual, or pending |


## Scenario Sources

Scenarios enter the bank from four primary sources:

| Source | When | Examples |
|--------|------|---------|
| Spec | FRAME/EXPLORE phase | Happy path from Intent Contract, failure scenarios, edge cases |
| Clarification | BUILD phase | "What should happen if the user's session expires mid-checkout?" |
| Production | SHIP/LEARN phase | Observed user behavior patterns not covered by existing scenarios |
| Incident | LEARN phase | Failure paths discovered during outages or bugs |

Each source carries different implications for priority and automation:

- **Spec scenarios** are typically critical or important priority and should be automated immediately.
- **Clarification scenarios** fill gaps discovered during implementation and are usually important priority.
- **Production scenarios** reflect real-world behavior and may reveal missing coverage at any priority level.
- **Incident scenarios** are almost always critical priority, as they represent proven failure paths.


## Scenario Priority

| Priority | Meaning | Automation Expectation |
|----------|---------|----------------------|
| Critical | Failure means the feature is broken or unsafe | Must be automated; blocks deployment |
| Important | Failure degrades the experience significantly | Should be automated; flags in review |
| Edge-case | Uncommon path; failure has limited impact | Automate when practical; manual validation acceptable |


## Building and Maintaining the Bank

### Initial Population (FRAME/EXPLORE)

Scenarios from the Intent Contract seed the bank. Every Intent Contract requires at least three scenarios (happy path, edge case, failure case). These become the initial entries.

During EXPLORE, additional scenarios emerge from technical spikes and architecture analysis. If a spike reveals that a feature interacts with an external service that has rate limits, a rate-limit scenario should enter the bank.

### Growth During BUILD

As agents and humans implement the feature, new scenarios surface:

- Code review comments that clarify expected behavior become clarification scenarios
- Edge cases discovered during testing become new entries
- Integration points that reveal unexpected state combinations generate new scenarios

Agents operating at P2+ proof tiers should check their work against the Scenario Bank before submitting for review. If an agent's implementation would break an existing scenario, that is a signal to pause and investigate.

### Updates During LEARN

Production data and incidents are the most valuable sources for Scenario Bank growth:

- Usage patterns that no scenario covers reveal gaps
- Incidents provide battle-tested failure scenarios
- Performance data may reveal scenarios for non-functional requirements

The LEARN phase should include explicit Scenario Bank review as a standard activity.


## Scenario Banks and Proof Tiers

Scenario Banks become mandatory at P2 (scenario-backed proof) and grow in importance through P4:

| Proof Tier | Scenario Bank Role |
|-----------|-------------------|
| P0-P1 | Optional (helpful but not required) |
| P2 | Required. Validation is driven by Scenario Bank content. |
| P3 | Required. Includes non-functional scenarios (load, security, failure injection). |
| P4 | Required. Production telemetry validates scenarios continuously. Spec drift detected against scenario expectations. |


## Scenario Banks and Runtime Governance

For live agent systems, Scenario Banks connect directly to runtime governance artifacts:

- **Trust Envelope categories** in scenarios verify that agent outputs stay within authorized boundaries
- **Escalation class** fields validate that the correct escalation path fires
- **State paths** verify that the Interaction State Model transitions are correct
- **Runtime checks** validate real-time behavior against expectations

See [Runtime Governance](runtime-governance.md) for details on Trust Envelopes, Escalation Contracts, and Interaction State Models.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Intent Contract scenarios seed the bank |
| [Constitution](constitution.md) | Constitution rules may generate required scenarios |
| [Proof Tiers](proof-tiers.md) | Scenario Banks required at P2+; scope expands through P4 |
| [Autonomy Tiers](autonomy-tiers.md) | Agents validate work against Scenario Bank at P2+ |
| [Risk Classification](risk-classification.md) | Higher risk requires more comprehensive scenario coverage |
| [Drift Detection](drift-detection.md) | Scenario Bank is a baseline for build-time and spec drift comparison |
| [Runtime Governance](runtime-governance.md) | Scenarios map to Trust Envelope, Escalation, and State Model artifacts |
| [Phases](phases.md) | Seeded in FRAME/EXPLORE, expanded in BUILD, validated in VALIDATE, updated in LEARN |


## Practical Guidance

**Every incident should produce a scenario.** This is the single most effective practice for improving Scenario Bank quality. If something went wrong in production, capture it as a scenario so it never happens undetected again.

**Link scenarios to test cases.** Each automated scenario should map to one or more test cases in your test suite. The scenario provides the "what and why." The test case provides the "how." Track this mapping explicitly.

**Review scenario coverage during VALIDATE.** Before shipping, verify that the Scenario Bank covers the Intent Contract's desired outcomes, constraints, and failure modes. Gaps in coverage are gaps in confidence.

**Do not let the bank go stale.** A Scenario Bank that was accurate six months ago but has not been updated since is a false sense of security. Include scenario review in your LEARN phase checklist.

**Use scenarios to onboard agents.** When an agent starts working on a feature, pointing it at the relevant Scenario Bank entries gives it immediate context about expected behavior, failure modes, and runtime constraints.

**Prioritize automation of critical scenarios.** Not every scenario needs to be automated immediately, but every critical-priority scenario should be. If a critical scenario is manual-only, it is a deployment risk.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Test-only thinking | Scenarios written as test cases, missing failure modes and signals | Use the full scenario structure including signals and runtime checks |
| Spec-only sourcing | All scenarios from FRAME, none from production or incidents | Actively add scenarios from production data and incident reviews |
| Orphaned scenarios | Scenarios exist but are not linked to tests or validation | Map every automated scenario to test cases; track automation status |
| Coverage theater | Large scenario count but shallow coverage of actual risk areas | Prioritize scenario depth for high-risk paths over breadth |
| Static bank | Bank not updated after BUILD or LEARN discoveries | Include Scenario Bank review in phase transition checklists |
