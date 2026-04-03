# Runtime Governance

## What It Is

Runtime Governance is the set of artifacts and mechanisms that control live agent behavior in production. While most INTENT Framework concepts focus on the development lifecycle (how you build software), Runtime Governance focuses on what happens after deployment: how agents behave, what they are authorized to do, when they escalate to humans, and what states they can occupy.

Runtime Governance consists of three artifacts that operate in a defined hierarchy:

1. **Trust Envelope** (what the agent is authorized to do)
2. **Escalation Contract** (how and when work moves to humans)
3. **Interaction State Model** (what states the agent can be in and how it transitions between them)

All three operate under the [Constitution](constitution.md), which sits at the top of the governance stack.


## Why It Exists

A deployed agent is fundamentally different from a code-generating agent during BUILD. During BUILD, agents produce artifacts that humans review before they reach users. In production, agents interact with users and systems directly. The feedback loop is tighter, the stakes are higher, and the need for guardrails is immediate.

Runtime Governance exists because "test it thoroughly and deploy it" is insufficient for live agent systems. Production environments surface situations that testing cannot fully anticipate. Runtime Governance provides the structure for agents to handle those situations safely, escalating when they encounter uncertainty rather than guessing.

**Trigger condition:** Runtime Governance artifacts are required whenever a system's live outputs or actions can affect users, operations, compliance, safety, or business outcomes without guaranteed human review of every interaction.


## The Governance Stack

The four layers of the governance stack form a strict hierarchy. Each layer must conform to the layer above it.

```
Constitution (non-negotiable rules)
    Trust Envelope (authorized boundaries)
        Escalation Contract (paths to humans)
            Interaction State Model (valid states and transitions)
```

A Trust Envelope cannot authorize outputs that the Constitution prohibits. An Escalation Contract cannot skip escalation for Constitution violations. The Interaction State Model cannot define states that violate Trust Envelope boundaries.


## Trust Envelope

### What It Is

The Trust Envelope defines the positive authorization boundary for a live agent: what the agent IS authorized to output or do. Anything not explicitly within the envelope is unauthorized by default.

### Structure

A Trust Envelope contains:

| Component | Purpose |
|-----------|---------|
| Authorized output categories | Named categories of outputs the agent can produce (e.g., "product information," "account status," "troubleshooting guidance") |
| Boundaries per category | Constraints on each category (e.g., "product information must reference only the current catalog") |
| Examples per category | Concrete examples of valid and invalid outputs |
| Confidence levels | How much variation the agent is allowed |
| Violation severity | Impact classification for boundary breaches |
| Detection methods | How violations are identified |

### Confidence Levels

Each output category has an assigned confidence level that determines how much latitude the agent has:

| Level | Name | Agent Behavior |
|-------|------|---------------|
| Scripted | Fixed output | Agent uses exact, pre-defined responses with no variation |
| Templated | Constrained variation | Agent fills in templates with validated data |
| Generated | Bounded generation | Agent generates responses within defined boundaries |

Higher confidence levels (generated) require stronger proof foundations and more sophisticated monitoring. Scripted outputs are the safest but least flexible.

### Violation Severity

When the agent produces output outside the Trust Envelope, the severity determines the response:

| Severity | Response |
|----------|----------|
| Critical | Immediate halt or fallback; escalate to human |
| High | Restrict agent to scripted responses; alert operations |
| Medium | Log and flag for review; continue with reduced authority |
| Low | Log for LEARN phase analysis |


## Escalation Contract

### What It Is

The Escalation Contract maps every path from agent-handled interaction to human involvement. It ensures that there is always a defined route to human help, with clear protocols for each type of escalation.

### Escalation Classes

| Class | Name | Trigger | Response Time |
|-------|------|---------|---------------|
| E0 | No escalation | Agent handles fully within Trust Envelope | N/A |
| E1 | Urgent | Time-sensitive issue requiring human judgment | Defined SLA |
| E2 | Critical | Safety, compliance, or high-impact issue | Immediate |
| EX | User-requested | User explicitly asks for a human | Defined SLA |

### Structure

An Escalation Contract defines:

| Component | Purpose |
|-----------|---------|
| Escalation classes | Classification of escalation types with triggers |
| Step-by-step protocols | What happens at each stage of escalation |
| Timeouts and fallbacks | What happens if escalation does not resolve within expected time |
| User communication templates | What the user sees during escalation per stage |
| Evidence capture requirements | What data must be preserved for the human receiving the escalation |

### Key Principle

Every interaction path must have a defined escalation route. If there is a situation where the agent is stuck and no escalation path exists, the Escalation Contract is incomplete. The "EX" class (user-requested escalation) is the universal fallback: users can always request a human.


## Interaction State Model

### What It Is

The Interaction State Model defines the valid runtime states an agent can occupy, the transitions between them, and the permissions and constraints that apply in each state.

### State Definition

Each state includes:

| Component | Purpose |
|-----------|---------|
| Entry conditions | What must be true for the agent to enter this state |
| Allowed Trust Envelope categories | Which output categories are valid in this state |
| Required data before exit | What information must be collected before leaving |
| Exit conditions | What must be true to transition out |

### Transitions

State transitions follow defined rules:

- **Guard conditions** that must be satisfied before a transition occurs
- **Escalation overrides** that force state changes regardless of normal transition logic (e.g., a Constitution violation forces a transition to an escalation state)
- **Scenario mapping** that links expected state paths to Scenario Bank entries

### Why States Matter

Without a defined state model, agents can drift into undefined situations. A customer support agent might attempt to process a refund while still in an "information gathering" state, missing required verification steps. The Interaction State Model prevents this by making state transitions explicit and enforced.


## Runtime Governance and Risk

Risk classification directly affects how strict Runtime Governance artifacts need to be:

| Risk Level | Trust Envelope | Escalation | State Model |
|-----------|---------------|------------|-------------|
| High | Narrow boundaries, mostly scripted/templated | Low escalation thresholds, fast response | Few states, strict transitions |
| Medium | Defined categories with bounded generation | Explicit triggers, standard SLAs | Moderate complexity, clear guard conditions |
| Low + strong proof | Broader categories, more generated output | Exception-based escalation | Flexible transitions within validated patterns |


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Runtime Governance Context section references these artifacts |
| [Constitution](constitution.md) | Top of governance stack; all runtime artifacts must conform |
| [Proof Tiers](proof-tiers.md) | P4 validates runtime governance through production telemetry |
| [Autonomy Tiers](autonomy-tiers.md) | Runtime autonomy bounded by Trust Envelope |
| [Risk Classification](risk-classification.md) | Risk determines strictness of all three artifacts |
| [Scenario Banks](scenario-banks.md) | Scenarios map to state paths, escalation classes, and Trust Envelope categories |
| [Drift Detection](drift-detection.md) | Runtime drift checks validate against all three artifacts |
| [Phases](phases.md) | Defined in FRAME/EXPLORE, built in BUILD, validated in VALIDATE, monitored from SHIP onward |


## Practical Guidance

**Start with the Trust Envelope.** Of the three artifacts, the Trust Envelope has the highest immediate impact. Defining what the agent is authorized to do (and, by exclusion, what it is not) prevents the most common class of runtime failures.

**Make escalation paths concrete.** Abstract escalation policies ("escalate when appropriate") fail in practice. Define specific triggers, specific protocols, and specific communication templates. Agents need unambiguous instructions for when and how to involve humans.

**Test your state model with Scenario Bank entries.** Every scenario that involves a live agent should map to an expected state path. If a scenario's state path is not valid according to the Interaction State Model, either the scenario or the model needs updating.

**Monitor Trust Envelope boundaries, not just violations.** Track how close agents get to boundaries, not just when they cross them. If outputs frequently cluster near a boundary, either the boundary is too narrow or the agent needs better guidance.

**Plan for graceful degradation.** When escalation fails (no human available, system overloaded), what happens? The Escalation Contract should define fallback behavior for every escalation class. "Try again later" is sometimes the right answer, but it needs to be an explicit choice.

**Review runtime governance in LEARN.** Production data reveals whether Trust Envelope boundaries are calibrated correctly, whether escalation triggers fire at the right thresholds, and whether the state model covers actual interaction patterns.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Envelope-less deployment | Live agent with no defined Trust Envelope | Define authorized categories before deployment |
| Missing escalation paths | Some interaction paths have no route to humans | Audit all paths; ensure EX (user-requested) is always available |
| Undefined states | Agent operates in situations not covered by the state model | Expand state model based on production observation |
| Over-scripted envelope | Everything is scripted; agent provides no value | Identify safe categories for templated or generated output |
| Escalation dead ends | Escalation triggered but no one responds | Define timeouts and fallback behavior for every class |
| Static governance | Runtime artifacts never updated after initial deployment | Include runtime governance review in LEARN phase |


## Template Reference

See `templates/trust-envelope.md`, `templates/escalation-contract.md`, and `templates/interaction-state-model.md` for starter templates with inline guidance.
