# Interaction State Model: [Agent / Feature Name]

> **Version:** [x.y] | **Date:** [DATE] | **Owner:** [team]
> **Intent Contract:** [path]
>
> Interaction State Model defines valid runtime states, transitions, and per-state permissions.

---

## 1. Scope

- **Interaction type:** [voice/chat/autonomous workflow]
- **System boundary:** [what this model governs]
- **Assumptions:** [runtime assumptions]

## 2. State Definitions

| State ID | Name | Entry condition | Allowed Trust Envelope categories | Required data before exit | Exit conditions |
|---|---|---|---|---|---|
| ST-1 | [State name] | [entry] | [TE categories] | [data] | [exit] |
| ST-2 | [State name] | [entry] | [TE categories] | [data] | [exit] |
| ST-3 | [State name] | [entry] | [TE categories] | [data] | [exit] |

## 3. Transition Rules

| From state | Trigger | To state | Guard condition | Notes |
|---|---|---|---|---|
| ST-1 | [trigger] | ST-2 | [guard] | [notes] |
| ST-2 | [trigger] | ST-3 | [guard] | [notes] |
| ST-2 | [interrupt] | ST-4 | [guard] | [interrupt handling] |

## 4. Escalation Overrides

| Condition | Forced state | Escalation class | Immediate action |
|---|---|---|---|
| [condition] | [state] | E1 | [action] |
| [condition] | [state] | E2 | [action] |

## 5. Scenario Mapping

| Scenario ID | Expected state path | Escalation class |
|---|---|---|
| S001 | [ST-1 -> ST-2 -> ST-3] | E0 |
| S002 | [path] | E0 |
| S003 | [path] | E1 |

## 6. Runtime Validation

| Metric | Definition | Threshold | Owner |
|---|---|---|---|
| State violation rate | Unauthorized output/action for active state | [threshold] | [owner] |
| Invalid transition rate | Transition not allowed by model | [threshold] | [owner] |
| State completion latency | Time spent in critical states | [threshold] | [owner] |

## 7. Prompt/Runtime Implementation Guidance

- Use per-state instruction blocks, not one monolithic prompt.
- Load only the allowed Trust Envelope categories for active state.
- Trigger escalation override immediately when guard conditions fail.
- Emit state transition events for observability and replay.

## 8. Approval & Change Log

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| [x.y] | [DATE] | [summary] | [reason] | [name] |
