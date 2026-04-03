# Quickstart: Your First INTENT Project

> **INTENT Framework v0.5** | Guide
>
> This guide walks you through setting up INTENT on a real project, from installation
> to your first validated feature. Expect 30-60 minutes for initial setup, then
> ongoing use per feature.

---

## Prerequisites

- A Git repository for your project
- [GitHub Spec Kit](https://github.com/github/spec-kit) installed (INTENT's BUILD and VALIDATE phases run through Spec Kit)
- An AI coding agent (Claude Code, Cursor, GitHub Copilot, or similar)
- Familiarity with your project's architecture and constraints

---

## Step 1: Install Spec Kit

Spec Kit provides the spec-driven development workflow that INTENT builds on.

```bash
npm install -g @github/spec-kit
```

Initialize Spec Kit in your project:

```bash
cd your-project
specify init
```

This creates a `.speckit/` directory with default configuration.

---

## Step 2: Copy INTENT Templates

Clone or download the INTENT template pack into your project. The templates live in the `templates/` directory of this repository.

**Required templates:**

| Template | Purpose | Used By |
|----------|---------|---------|
| [`templates/intent-contract-template.md`](../../templates/intent-contract-template.md) | Define feature intent, outcomes, constraints | Intent Architect |
| [`templates/constitution-starter.md`](../../templates/constitution-starter.md) | Project-level invariants and rules | Systems Conductor |
| [`templates/scenarios-template.yaml`](../../templates/scenarios-template.yaml) | Structured validation scenarios | Quality Guardian |
| [`templates/plan-template-intent.md`](../../templates/plan-template-intent.md) | Implementation plan structure | Agent (reviewed) |
| [`templates/tasks-template-intent.md`](../../templates/tasks-template-intent.md) | Task breakdown structure | Agent |

**Optional templates (for agent-facing products):**

| Template | Purpose | Used By |
|----------|---------|---------|
| [`templates/trust-envelope-template.md`](../../templates/trust-envelope-template.md) | Agent autonomy boundaries | Experience Shaper |
| [`templates/escalation-contract-template.md`](../../templates/escalation-contract-template.md) | Human handoff rules | Experience Shaper |
| [`templates/interaction-state-model-template.md`](../../templates/interaction-state-model-template.md) | Valid interaction states | Experience Shaper |

Copy these into your project's spec directory or reference them directly.

---

## Step 3: Write Your Constitution

The Constitution is your project's supreme governing document. Every agent interaction must comply with it.

1. Copy `templates/constitution-starter.md` to your project (e.g., `.speckit/constitution.md` or `docs/constitution.md`).
2. Fill in the required sections:

**Minimum viable sections:**

- **Architecture Principles:** 3-5 rules about allowed technologies, patterns, and structural decisions.
- **Security Requirements:** Non-negotiable security constraints.
- **Agent Boundaries:** What agents can and cannot do in this project.
- **Amendment Process:** How the Constitution changes over time.

Do not overthink this. Start with rules you already follow but have never written down. You will refine the Constitution as you learn.

---

## Step 4: Build Your First Feature

INTENT follows six phases: FRAME, EXPLORE, BUILD, VALIDATE, SHIP, LEARN. Here is how they map to Spec Kit commands and your workflow.

### FRAME: Write the Intent Contract

Use `/speckit.specify` (or create manually from the template) to write your Intent Contract.

```
/speckit.specify
```

Fill in:

- **Problem Statement:** What problem are you solving and for whom?
- **Desired Outcomes:** Measurable success criteria (2-3 outcomes).
- **Constraints:** What must be true? What is out of scope?
- **Proof Plan:** What evidence proves the intent was met?
- **Risk Classification:** High, Medium, or Low for this feature.

**Quality check:** Can someone who has not seen the code explain what this feature should do and how you will know it works? If yes, the contract is good enough.

### EXPLORE: Generate the Plan

Use `/speckit.plan` to have the agent generate an implementation plan.

```
/speckit.plan
```

Review the plan against your Constitution. Check for:

- Architecture principle violations
- Missing constraint handling
- Unreasonable scope or complexity
- Security requirement gaps

The agent proposes. You review and approve. Do not skip this review.

### BUILD: Execute Tasks

Use `/speckit.tasks` to break the plan into tasks, then `/speckit.implement` to execute.

```
/speckit.tasks
/speckit.implement
```

The agent executes at the autonomy level appropriate for your risk classification:

| Risk Tier | Agent Behavior |
|-----------|----------------|
| Low | Agent implements end-to-end, you review the result |
| Medium | Agent implements, you review before merge |
| High | Agent proposes each step, you approve before it executes |

### VALIDATE: Run Scenarios

Before merging, validate against your Scenario Bank.

1. **Walk scenarios:** Run each scenario from `templates/scenarios-template.yaml` against the implementation.
2. **Check Constitution drift:** Verify the implementation does not violate any Constitution rules.
3. **Verify trust envelope compliance:** If this feature involves agent-facing behavior, confirm it stays within the Trust Envelope.

All scenarios must pass at their required proof tier before the feature can proceed.

### SHIP: Merge and Deploy

Use your standard CI/CD pipeline. INTENT does not prescribe deployment tooling.

Before merging, confirm:

- [ ] All scenarios pass
- [ ] No Constitution violations detected
- [ ] Risk-appropriate review completed
- [ ] Drift detection checks pass in CI

### LEARN: Review and Feed Back

After the feature is live, compare production behavior against your Intent Contract assumptions.

- Did the desired outcomes materialize?
- Were the constraints sufficient?
- What scenarios were missing?
- What should change in the Constitution?

Feed findings back into the Scenario Bank and Constitution for the next feature.

---

## What You Should Have After This Guide

| Artifact | Location |
|----------|----------|
| Constitution | Your project's spec directory |
| First Intent Contract | Per feature, in spec directory |
| Scenario Bank | Per contract, YAML files |
| Implementation plan | Generated by Spec Kit |
| Passing scenario evidence | CI artifacts or PR description |

---

## Next Steps

- Read [Roles & Team Models](../reference/roles.md) to assign INTENT roles on your team.
- Read [Tool Integration](./tool-integration.md) to configure your specific AI coding agent.
- Review the [30/60/90 Rollout Plan](../reference/rollout-30-60-90.md) for a structured adoption path.
