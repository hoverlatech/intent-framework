# Do I Need INTENT?

> **INTENT Framework v0.5** | Guide
>
> A 5-question decision tree to figure out which INTENT artifacts you actually need. Skip the rest until you do.

---

## The 5 questions

Answer yes/no. Tally your answers.

| # | Question | If Yes |
|---|---|---|
| 1 | Do AI agents write or modify production code in your repo? | Adopt the **always-required** set. |
| 2 | Does the change you are about to ship touch auth, payments, PII, infrastructure, or anything that wakes someone at 2am if it breaks? | Adopt the **always-required** set. Plan for P3 proof. |
| 3 | Do live AI outputs reach end users (customers, operators, regulators) without guaranteed human review of every action? | Add the **live-agents-only** set. |
| 4 | Are multiple agents — or multiple humans driving agents — making changes in parallel against the same codebase? | Adopt the **always-required** set. You will need shared rules to avoid drift. |
| 5 | Do you owe evidence to a customer, auditor, or regulator that the system behaves as specified? | Adopt the **always-required** set, plus a Proof Report per release. |

If you answered **no to all five**, you do not need INTENT yet. Bookmark this page; come back when one of them flips.

---

## What to adopt

### Always-required (any "yes" to questions 1, 2, 4, or 5)

| Artifact | Purpose | Template |
|---|---|---|
| **Constitution** | Project-level non-negotiables agents must obey | [`templates/constitution-starter.md`](../../templates/constitution-starter.md) |
| **Intent Contract** | One per medium+ risk change. Defines outcomes, constraints, scenarios, proof plan | [`templates/intent-contract-template.md`](../../templates/intent-contract-template.md) |
| **Scenario Bank** | The holdout cases that prove a change works | [`templates/scenarios-template.yaml`](../../templates/scenarios-template.yaml) |
| **Proof Report** | Evidence that the Scenario Bank passed at the target proof tier | Generated per release |

### Live-agents-only (yes to question 3)

| Artifact | Purpose | Template |
|---|---|---|
| **Trust Envelope** | What the live agent is authorized to output or do | [`templates/trust-envelope-template.md`](../../templates/trust-envelope-template.md) |
| **Escalation Contract** | Every path from agent-handled to human-handled | [`templates/escalation-contract-template.md`](../../templates/escalation-contract-template.md) |
| **Interaction State Model** | Valid runtime states, transitions, and per-state permissions | [`templates/interaction-state-model-template.md`](../../templates/interaction-state-model-template.md) |

If you do not have live agents in production, **skip the live-agents-only set entirely.** Adopting them prematurely is the most common reason teams bounce off INTENT.

---

## What's next

- New to the framework? Go to the [Quickstart](./quickstart.md) for a Day 1–30 path.
- Wiring this into CI? Start with the [GitHub Actions reference adapter](../reference-adapters/github-actions.md).
- Already running INTENT and wondering where the gaps are? Read [Drift Detection](../concepts/drift-detection.md).
