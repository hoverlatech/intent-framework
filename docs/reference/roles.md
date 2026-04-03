# Roles & Team Models

> **INTENT Framework v0.5** | Reference
>
> Four roles govern every INTENT project. The roles exist whether you have one person or fifty.
> What changes is how you assign them.

---

## The Four Roles

### Intent Architect

The Intent Architect owns the "what" and "why." They write Intent Contracts, define constraints, and design the proof plan that determines when a feature is actually done.

**Responsibilities:**

- Write and maintain Intent Contracts (replacing user stories)
- Define measurable outcomes and success criteria
- Set constraints and non-goals
- Design the proof plan: what evidence proves the intent was met
- Own the FRAME phase, drive EXPLORE

**When this role matters most:** Early in a feature lifecycle. If the contract is wrong, everything downstream is wasted work.

### Systems Conductor

The Systems Conductor owns architecture decisions, system reliability, and the context layers that agents need to do their work correctly.

**Responsibilities:**

- Maintain the project Constitution (architecture principles, security requirements, agent boundaries)
- Define and enforce context layers (what information agents receive at each phase)
- Own system-level reliability: performance budgets, failure modes, integration boundaries
- Review agent-generated plans for architectural compliance
- Own BUILD phase oversight

**When this role matters most:** During BUILD and VALIDATE. The Conductor prevents architectural drift before it becomes technical debt.

### Experience Shaper

The Experience Shaper owns interaction quality and usability. In agent-facing products, they own the Trust Envelope, Escalation Contract, and Interaction State Model.

**Responsibilities:**

- Define interaction quality standards (response time, tone, error handling)
- Author and maintain the Trust Envelope (what agents can and cannot do autonomously)
- Design escalation paths (when and how agents hand off to humans)
- Build the Interaction State Model (valid states, transitions, edge cases)
- Validate usability evidence during VALIDATE phase

**When this role matters most:** Any project with user-facing agent behavior. Without this role, agents may be technically correct but unusable.

### Quality Guardian

The Quality Guardian owns the Scenario Bank, risk tiers, and autonomy policy. They decide how much freedom agents get and hold the evidence that justifies it.

**Responsibilities:**

- Build and maintain the Scenario Bank (structured scenarios per contract)
- Assign risk tiers (High / Medium / Low) to features and agent actions
- Define and calibrate autonomy budgets (how much agents can do without human review)
- Monitor scenario health: pass rates, coverage gaps, flaky scenarios
- Own VALIDATE phase, drive LEARN phase reviews

**When this role matters most:** Continuously. Scenario health degrades over time. Autonomy budgets need recalibration as evidence accumulates.

---

## Team Models

INTENT scales across three team structures. Pick the one that matches your team size and project complexity.

### Solo Director

| Attribute | Detail |
|-----------|--------|
| Team size | 1 person |
| Role assignment | One person fills all four roles |
| Best for | Prototypes, side projects, solo practitioners, early-stage startups |

The Solo Director cycles through each role as needed. During FRAME, you are the Intent Architect. During BUILD, you shift to Systems Conductor. During VALIDATE, you become the Quality Guardian.

**Practical guidance:**

- Use the templates to enforce role discipline. Without them, it is easy to skip the Quality Guardian work when you are eager to ship.
- Time-box each role. Spend explicit time on scenario writing and Constitution review rather than treating them as afterthoughts.
- The biggest risk is skipping VALIDATE because you "already know it works." Write the scenarios anyway.

### Thin Team (2-4 people)

| Attribute | Detail |
|-----------|--------|
| Team size | 2-4 people |
| Role assignment | Each person covers 1-2 roles |
| Best for | Product teams, feature squads, small engineering teams |

This is the most common model. Clear ownership with minimal coordination overhead.

**Typical assignments:**

| People | Suggested Split |
|--------|----------------|
| 2 | Person A: Intent Architect + Experience Shaper. Person B: Systems Conductor + Quality Guardian. |
| 3 | Person A: Intent Architect. Person B: Systems Conductor + Experience Shaper. Person C: Quality Guardian. |
| 4 | One person per role. |

**Practical guidance:**

- Make role assignments explicit. Write them in your project README or Constitution.
- The Intent Architect and Quality Guardian pairing matters most. If one person writes contracts and a different person writes scenarios, you get better coverage.
- Avoid giving one person both Intent Architect and Quality Guardian. The contract author should not be the only person validating it.

### Swarm

| Attribute | Detail |
|-----------|--------|
| Team size | 5+ people |
| Role assignment | Multiple people share roles |
| Best for | Complex systems, platform teams, organizations scaling INTENT across projects |

In the Swarm model, roles become teams. You might have two Intent Architects (one per domain area), a Systems Conductor with a deputy, and a Quality Guardian team that maintains the Scenario Bank.

**Practical guidance:**

- Establish coordination protocols. When multiple people share a role, define who has final say on conflicts.
- Use the Constitution as the single source of truth. With more people, implicit norms break down faster.
- Assign a "role lead" for each shared role to prevent diffusion of responsibility.
- Run weekly role syncs: each role lead reports on their domain (contract health, architecture drift, scenario coverage, interaction quality).

---

## Choosing Your Model

| Signal | Recommended Model |
|--------|-------------------|
| Solo developer or prototype | Solo Director |
| Product team building features | Thin Team |
| Multiple teams, shared platform, or org-wide rollout | Swarm |
| Transitioning from Scrum | Start with Thin Team, map existing roles to INTENT roles |

You can evolve between models. Most teams start as Solo Director or Thin Team and move to Swarm as the project grows and more people need to participate in governance decisions.

---

## Related Templates

- [`templates/intent-contract-template.md`](../../templates/intent-contract-template.md) (Intent Architect)
- [`templates/constitution-starter.md`](../../templates/constitution-starter.md) (Systems Conductor)
- [`templates/trust-envelope-template.md`](../../templates/trust-envelope-template.md) (Experience Shaper)
- [`templates/scenarios-template.yaml`](../../templates/scenarios-template.yaml) (Quality Guardian)
- [`templates/escalation-contract-template.md`](../../templates/escalation-contract-template.md) (Experience Shaper)
- [`templates/interaction-state-model-template.md`](../../templates/interaction-state-model-template.md) (Experience Shaper)
