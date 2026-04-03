# Escalation Contract: [Agent / Feature Name]

> **Version:** [x.y] | **Date:** [DATE] | **Owner:** [team]
> **Intent Contract:** [path]
>
> Escalation Contract defines every path from agent-handled interaction to human involvement.

---

## 1. Scope

- **Applies to:** [agent surfaces]
- **Users affected:** [audience]
- **Runtime systems involved:** [ticketing, paging, CRM, etc.]

## 2. Escalation Classes

| Class | Trigger type | Description | Priority |
|---|---|---|---|
| E0 | No escalation | Agent handles within Trust Envelope | Lowest |
| E1 | Urgent escalation | Potential risk or unresolved user need | High |
| E2 | Critical escalation | Safety/compliance/critical incident | Highest |
| EX | User-requested | User explicitly requests human handoff | [set] |

## 3. Protocol Per Class

### E1 - Urgent

1. [Trigger detection step]
2. [User communication step]
3. [Handoff action]
4. [Confirmation and close]

- **Timeout to human acknowledgment:** [time]
- **Max wait before fallback:** [time]

### E2 - Critical

1. [Immediate stop or guard action]
2. [Critical escalation signal]
3. [User safety communication]
4. [Incident logging]

- **Timeout to critical responder:** [time]
- **Fallback path:** [what happens if responder unavailable]

## 4. User Communication

| Stage | User message template | Channel |
|---|---|---|
| Escalation started | [template] | [voice/chat/email] |
| Waiting for human | [template] | [channel] |
| Escalation complete | [template] | [channel] |
| Escalation failed/fallback | [template] | [channel] |

## 5. Fallback Paths

| Failure condition | Fallback action | Owner |
|---|---|---|
| Human unavailable | [fallback] | [team] |
| Downstream system failure | [fallback] | [team] |
| Channel interruption | [fallback] | [team] |

## 6. Evidence Capture

| Event | Required fields | Retention | Audit owner |
|---|---|---|---|
| Escalation trigger | [fields] | [period] | [owner] |
| Handoff success/failure | [fields] | [period] | [owner] |
| Timeout/fallback | [fields] | [period] | [owner] |

## 7. Failure Modes

| Failure mode | Severity | Detection | Mitigation |
|---|---|---|---|
| Missed escalation | Critical | [method] | [action] |
| False escalation | Medium | [method] | [action] |
| Incomplete handoff | High | [method] | [action] |

## 8. Priority Matrix

| If multiple triggers apply | Winning class | Rule |
|---|---|---|
| E2 + EX | E2 | Safety/compliance first |
| E1 + EX | [set rule] | [rationale] |
| Multiple E1 triggers | [set rule] | [rationale] |

## 9. Validation Checklist

- [ ] Each escalation class tested end-to-end
- [ ] Timeout behavior verified
- [ ] Fallback behavior verified
- [ ] Evidence logging verified
- [ ] User communication content approved

## 10. Approval & Change Log

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| [x.y] | [DATE] | [summary] | [reason] | [name] |
