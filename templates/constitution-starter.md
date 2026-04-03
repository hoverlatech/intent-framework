# Project Constitution

> **Version:** 1.0 | **Last amended:** [DATE] | **INTENT Framework:** v0.5
>
> This is the supreme governing document for this project. Every AI agent interaction -
> specification, planning, implementation, and runtime behavior - MUST read and comply with
> this constitution. Violations block progress. Amendments require the process in Section 10.
>
> This template extends Spec Kit's default constitution with INTENT Framework governance
> sections. Fill in each section with your project's non-negotiable principles.

---

## 1. Architecture Principles

> Define allowed and forbidden technologies, patterns, and structural decisions.

- [e.g., Next.js App Router only. Pages Router is forbidden.]
- [e.g., All API routes validate input via shared schema contracts.]
- [e.g., Database access only through approved data access layer.]
- [e.g., No server-side mutable state outside approved persistence layers.]
- [e.g., New feature flags required for user-facing behavior changes.]

## 2. Security Requirements

> Non-negotiable security constraints. These override convenience and speed.

- [e.g., All endpoints require authenticated identity and authorization checks.]
- [e.g., PII is encrypted at rest and access is least privilege.]
- [e.g., No secrets in client-side code or logs.]
- [e.g., Public endpoints must enforce rate limiting and abuse controls.]
- [e.g., All external integrations require explicit threat review.]

## 3. Reliability Standards

> Performance, uptime, and resilience requirements.

- [e.g., User-facing APIs meet p95 latency and availability SLOs.]
- [e.g., Mutations are idempotent and retry-safe.]
- [e.g., All user-facing flows include clear error and recovery states.]
- [e.g., Breaking schema changes are forbidden without migration plan.]

## 4. Testing Standards

> Minimum testing requirements for all new code.

- [e.g., New APIs require integration tests.]
- [e.g., New UI flows require interaction coverage for primary paths.]
- [e.g., Regression coverage cannot decrease on merge.]
- [e.g., High-risk changes include failure-mode testing.]

## 5. Agent Boundaries

> What AI agents are forbidden from doing without human approval.

- [e.g., Agents must NOT modify auth or identity configuration without explicit approval.]
- [e.g., Agents must NOT alter production deployment policy without explicit approval.]
- [e.g., Agents must NOT modify migration files without explicit approval.]
- [e.g., Agents must NOT install dependencies without listed rationale and review.]
- [e.g., Agents must NOT access production secrets or production data directly.]

## 6. Risk Classification

> Define what makes a change High, Medium, or Low risk.

| Risk Tier | Criteria | Examples |
|---|---|---|
| **High** | [Touches auth, payments, PII, infrastructure, safety systems] | [OAuth flow, billing, escalation logic] |
| **Medium** | [User-facing features, API contract changes, schema updates] | [New endpoint, dashboard workflow] |
| **Low** | [Content, styling, docs, internal tooling] | [Copy update, UI polish] |

## 7. Proof Tier Thresholds

> What evidence is required at each proof level.

| Proof Tier | Name | Required Evidence | Minimum for Risk Tier |
|---|---|---|---|
| **P0** | Ad hoc | Informal check only | Low-risk internal tools only |
| **P1** | Repeatable | Basic automated checks + manual walkthrough | Low |
| **P2** | Scenario-backed | Scenario Bank pass evidence | Medium |
| **P3** | Risk-calibrated | P2 + load/security/failure-mode verification | High |
| **P4** | Closed-loop | P3 + production telemetry validates intent continuously | Critical systems |

## 8. Autonomy Policy

> What agents are allowed to do at each autonomy level.

| Autonomy Tier | Name | Agent Authority | Human Role | Applicable When |
|---|---|---|---|---|
| **A0** | Suggest | Agent proposes; humans execute | Decision-maker | High-risk or novel changes |
| **A1** | Draft | Agent drafts; humans edit | Author/editor | New artifacts and early framing |
| **A2** | Implement | Agent implements; humans review before merge | Reviewer | Default medium-risk delivery |
| **A3** | Operate | Agent executes with exception-focused review | Auditor | Low-risk, proven domains |
| **A4** | Execute | Agent merges/deploys under strict gates | Monitor | Mature low-risk domains only |

### Escalation rules

- Constitution violation -> automatic escalation to A0.
- New dependency or new architecture pattern -> A0 minimum.
- Agent confidence below project threshold -> escalate one tier.
- [Add project-specific escalation rules.]

## 9. Runtime Governance Requirements (for agent-facing systems)

> Required when an AI system operates live in customer-facing or safety-critical contexts.

### Trigger condition

Runtime governance artifacts are REQUIRED if the system's live outputs or actions can affect
users, operations, compliance, safety, or business outcomes without guaranteed human review.

### Required artifacts

- **Trust Envelope (required):** Positive boundary of authorized runtime outputs/actions.
- **Escalation Contract (required):** All paths from agent-handled to human-involved.
- **Interaction State Model (required):** Valid runtime states, transitions, and per-state permissions.

### Runtime enforcement rules

- No live deployment without versioned Trust Envelope, Escalation Contract, and Interaction State Model.
- Runtime authority is bounded by the Trust Envelope, not by BUILD autonomy tier alone.
- Escalation paths must be tested for each escalation class before release.
- Scenario Bank must map to interaction state paths for runtime coverage.

### Runtime evidence expectations

- Unsafe-answer rate (trust envelope violations per interaction)
- False-escalation and missed-escalation rates
- State violation rate (unauthorized output for current interaction state)
- Escalation success rate and fallback success rate

## 10. Amendment Process

> How this constitution is modified. Changes here affect all future development.

1. **Proposal:** Any team member may propose an amendment with rationale.
2. **Impact assessment:** Evaluate effects on active Intent Contracts and runtime artifacts.
3. **Review:** [e.g., maintainer approval / team vote / tech lead sign-off].
4. **Documentation:** Record date, rationale, changes, compatibility impact.
5. **Communication:** Re-initialize active agents after constitution changes.
6. **Versioning:** Increment constitution version with each amendment.

### Amendment log

| Version | Date | Change | Rationale | Approved by |
|---|---|---|---|---|
| 1.0 | [DATE] | Initial constitution | Project kickoff | [name] |
