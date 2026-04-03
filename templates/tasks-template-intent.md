# Task Breakdown: [Feature Name]

> **Branch:** [###-feature-name] | **Date:** [DATE]
> **Input:** Plan from `/specs/[###-feature-name]/plan.md`
> **Prerequisites:** plan.md, intent-contract.md, scenarios.yaml
> **INTENT Phase:** BUILD
>
> This template extends Spec Kit's `tasks-template.md` with INTENT v0.5 governance markers.

---

## Governance Summary

- **Risk tier:** [from spec]
- **Autonomy tier (BUILD):** [from spec]
- **Proof tier:** [from spec]
- **Runtime governance required:** [Yes / No]
- **Trust Envelope version:** [version / N/A]
- **Escalation Contract version:** [version / N/A]
- **Interaction State Model version:** [version / N/A]

### Task execution rules

- [e.g., A2: Agent executes tasks, human reviews each phase checkpoint.]
- [e.g., Tasks marked 🔒 require human approval before proceeding.]
- [e.g., Agent must not touch constitution-forbidden files without escalation.]
- [e.g., Runtime-governance checks are mandatory before SHIP when runtime is in scope.]

## Markers

- `[P]` - Parallelizable within phase
- `[S]` - Sequential dependency
- `🔒` - Human gate required
- `[US#]` - Scenario mapping to Scenario Bank IDs
- `[RG]` - Runtime governance task (Trust Envelope/Escalation/State Model)

## Phase 1: Foundation

- [ ] **Task 1.1** `[S]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S001]
- [ ] **Task 1.2** `[S]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S001, S002]
- [ ] 🔒 **Phase 1 checkpoint** - Human verifies foundation and constitution compliance

## Phase 2: Core Logic

- [ ] **Task 2.1** `[P]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S001, S002]
- [ ] **Task 2.2** `[P]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S001, S003]
- [ ] **Task 2.3** `[S]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S003]
- [ ] 🔒 **Phase 2 checkpoint** - Human verifies contracts and tests

## Phase 3: User-facing / Runtime Behavior

- [ ] **Task 3.1** `[P]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S001]
- [ ] **Task 3.2** `[P]` - [Description] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S002, S003]
- [ ] **Task 3.3** `[S]` - [Error/recovery behavior] `[file paths]`
  - Proof: [verification]
  - Scenarios: [S003]
- [ ] **Task 3.4** `[S][RG]` - Validate state-path and trust-envelope wiring
  - Proof: [runtime checks configured]
  - Scenarios: [S001, S002, S003]
- [ ] 🔒 **Phase 3 checkpoint** - Human verifies UX and runtime safety behavior

## Phase 4: Integration & Validation

- [ ] **Task 4.1** `[S]` - Run full test suite
  - Proof: no regressions
- [ ] **Task 4.2** `[S]` - Run Scenario Bank validation
  - Proof: scenario results documented
- [ ] **Task 4.3** `[S]` - Constitution drift check
  - Proof: no forbidden changes
- [ ] **Task 4.4** `[S]` - Generate contribution map
  - Proof: files categorized agent/human/both
- [ ] **Task 4.5** `[S][RG]` - Runtime governance verification
  - Proof: trust-envelope violations, escalation quality, and state violations meet thresholds
- [ ] 🔒 **Phase 4 checkpoint (VALIDATE gate)** - Human verifies:
  - [ ] Scenario Bank pass evidence is complete
  - [ ] Constitution compliance is confirmed
  - [ ] Runtime governance metrics meet thresholds (if required)
  - [ ] Contribution map reviewed
  - [ ] Proof Report drafted for PR

---

## Proof Report Template

```markdown
## Proof Report - [Feature Name]

**Intent Contract:** .specify/specs/[###-feature-name]/intent-contract.md
**Risk tier:** [value]
**Proof tier achieved:** [P0/P1/P2/P3/P4]
**Autonomy tier used (BUILD):** [A0/A1/A2/A3/A4]
**Runtime governance required:** [Yes/No]

### Scenario Results
| ID | Scenario | Result | Method | Notes |
|---|---|---|---|---|
| S001 | [name] | ✅/❌ | automated/manual | [notes] |
| S002 | [name] | ✅/❌ | automated/manual | [notes] |
| S003 | [name] | ✅/❌ | automated/manual | [notes] |

### Runtime Governance Evidence (if required)
| Metric | Result | Threshold | Status |
|---|---|---|---|
| Unsafe-answer rate | [value] | [target] | ✅/❌ |
| False-escalation rate | [value] | [target] | ✅/❌ |
| Missed-escalation rate | [value] | [target] | ✅/❌ |
| State violation rate | [value] | [target] | ✅/❌ |
| Escalation success rate | [value] | [target] | ✅/❌ |

### Constitution Compliance
- [ ] No architecture violations
- [ ] No security violations
- [ ] No unauthorized dependencies
- [ ] No forbidden file modifications
- [ ] Performance targets met

### Contribution Map Summary
- Agent-generated files: [count]
- Human-authored files: [count]
- Joint-authored files: [count]
- Files requiring focused review: [list]
```
