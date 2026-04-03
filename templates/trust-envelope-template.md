# Trust Envelope: [Agent / Feature Name]

> **Version:** [x.y] | **Date:** [DATE] | **Owner:** [team]
> **Intent Contract:** [path]
>
> Trust Envelope defines the positive runtime boundary: what the live agent is authorized to output or do.

---

## 1. Scope

- **Agent surface:** [voice/chat/automation]
- **User groups:** [who receives outputs]
- **Runtime context:** [production, support calls, transaction assistant, etc.]
- **Out of scope:** [what this envelope does not cover]

## 2. Authorized Output Categories

| Category ID | Name | Description | Allowed examples | Explicit boundary |
|---|---|---|---|---|
| TE-1 | [Category] | [What is allowed] | [examples] | [where it must stop] |
| TE-2 | [Category] | [What is allowed] | [examples] | [where it must stop] |
| TE-3 | [Category] | [What is allowed] | [examples] | [where it must stop] |

## 3. Confidence Policy

| Category ID | Confidence level | Runtime flexibility | Notes |
|---|---|---|---|
| TE-1 | scripted | fixed output | [notes] |
| TE-2 | templated | constrained variation | [notes] |
| TE-3 | generated | bounded generation | [notes] |

## 4. Disallowed Output Classes

- [Class 1 - explicitly forbidden output/action]
- [Class 2]
- [Class 3]

## 5. Violation Severity

| Severity | Definition | Example | Required response |
|---|---|---|---|
| Critical | Safety/compliance breach | [example] | Immediate escalation + incident |
| High | Significant policy breach | [example] | Escalation + block further output |
| Medium | Boundary drift | [example] | Log + correction + monitor |
| Low | Minor style/policy miss | [example] | Log + tune |

## 6. Detection & Monitoring

| Signal | Detection method | Alert threshold | Owner |
|---|---|---|---|
| Trust-envelope violation rate | [classifier/review] | [threshold] | [team] |
| Unsafe-answer rate | [method] | [threshold] | [team] |
| Category mismatch rate | [method] | [threshold] | [team] |

## 7. Escalation Integration

- **Escalation Contract version:** [version]
- **When envelope violations escalate automatically:** [rules]
- **Fallback behavior before human takeover:** [behavior]

## 8. Scenario & State Mapping

| Scenario ID | State path | Allowed categories |
|---|---|---|
| S001 | [states] | [TE categories] |
| S002 | [states] | [TE categories] |

## 9. Approval & Change Log

- **Approved by:** [name/role]
- **Approval date:** [DATE]
- **Review cadence:** [e.g., monthly]

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| [x.y] | [DATE] | [summary] | [reason] | [name] |
