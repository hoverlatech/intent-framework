# Project Constitution

> **Version:** 1.0 | **Last amended:** 2026-04-03 | **INTENT Framework:** v0.5
>
> This is the supreme governing document for the DocSearch project. Every AI agent interaction,
> specification, planning, implementation, and runtime behavior, MUST read and comply with
> this constitution. Violations block progress. Amendments require the process in Section 10.

---

## 1. Architecture Principles

- Python FastAPI backend. No alternative web frameworks without amendment.
- React (TypeScript) frontend with Vite build toolchain.
- PostgreSQL with pgvector extension for vector storage and similarity search. No separate vector database.
- Redis for query result caching and rate limiting. No in-process caching for shared state.
- All API routes validate input via Pydantic schema contracts.
- Document connectors are isolated modules with a shared interface. Each source system (Confluence, GitHub Wiki, Notion, Google Docs) has its own connector.
- Embedding generation runs as an async pipeline, not inline with search requests.
- No server-side mutable state outside PostgreSQL and Redis.
- Feature flags required for all user-facing behavior changes.

## 2. Security Requirements

- All endpoints require SSO authentication. No anonymous access.
- Document-level access controls are inherited from source systems. DocSearch never grants broader access than the source.
- No PII is stored in search indexes or embedding vectors. PII detection runs as a pipeline filter.
- No secrets in client-side code, logs, or error messages.
- All external integrations (Confluence API, GitHub API, Notion API, Google Docs API) require explicit threat review before activation.
- API rate limiting enforced per user: 60 queries/minute, 500 queries/hour.
- All search queries and results are logged for audit, but logs exclude document content from restricted sources.

## 3. Reliability Standards

- Search API p95 latency < 2 seconds.
- Search API availability: 99.9% uptime (measured monthly).
- Embedding pipeline tolerates individual connector failures without blocking other sources.
- All mutations to the search index are idempotent and retry-safe.
- All user-facing flows include clear error states and recovery paths.
- Degraded mode: if a source connector is unavailable, search proceeds with available sources and displays a notice.

## 4. Testing Standards

- Integration tests required for every document connector (Confluence, GitHub Wiki, Notion, Google Docs).
- End-to-end tests required for all search flows defined in the Scenario Bank.
- Unit tests required for embedding generation, query parsing, and access control filtering.
- Regression coverage cannot decrease on merge.
- Failure-mode tests required for connector outages and degraded search.
- Runtime governance scenarios (trust envelope violations, escalation paths) must have automated test coverage.

## 5. Agent Boundaries

- Agents must NOT modify access control configurations in any source system.
- Agents must NOT index documents marked as restricted without explicit human approval.
- Agents must NOT alter production deployment configuration without explicit approval.
- Agents must NOT install dependencies without listed rationale and review.
- Agents must NOT access production secrets or production user data directly.
- Agents must NOT generate answers that include content from documents the requesting user cannot access.
- Agents must NOT provide legal, HR, or compliance advice regardless of document content.

## 6. Risk Classification

| Risk Tier | Criteria | Examples |
|---|---|---|
| **High** | Touches authentication, access controls, PII handling, or security boundaries | SSO integration, access control filtering, PII detection pipeline |
| **Medium** | User-facing features, API contract changes, search ranking logic, new connectors | Search endpoint, answer generation, new source connector |
| **Low** | Content updates, styling, documentation, internal tooling, logging changes | UI polish, copy updates, log format changes |

## 7. Proof Tier Thresholds

| Proof Tier | Name | Required Evidence | Minimum for Risk Tier |
|---|---|---|---|
| **P0** | Ad hoc | Informal check only | Low-risk internal tools only |
| **P1** | Repeatable | Basic automated checks + manual walkthrough | Low |
| **P2** | Scenario-backed | Scenario Bank pass evidence + connector integration tests | Medium |
| **P3** | Risk-calibrated | P2 + load testing, security review, failure-mode verification | High |
| **P4** | Closed-loop | P3 + production telemetry validates intent continuously | Critical systems |

## 8. Autonomy Policy

| Autonomy Tier | Name | Agent Authority | Human Role | Applicable When |
|---|---|---|---|---|
| **A0** | Suggest | Agent proposes; humans execute | Decision-maker | High-risk or novel changes (auth, access controls) |
| **A1** | Draft | Agent drafts; humans edit | Author/editor | New artifacts and early framing |
| **A2** | Implement | Agent implements; humans review before merge | Reviewer | Default for medium-risk delivery (search features, connectors) |
| **A3** | Operate | Agent executes with exception-focused review | Auditor | Low-risk proven domains (styling, docs) |
| **A4** | Execute | Agent merges/deploys under strict gates | Monitor | Not applicable for this project |

### Escalation rules

- Constitution violation: automatic escalation to A0.
- New dependency or new architecture pattern: A0 minimum.
- Agent confidence below 0.7: escalate one tier.
- Any change touching access control logic: A0, no exceptions.
- Any change to PII detection or filtering: A0, no exceptions.
- New source connector integration: A1 minimum (draft, human edits).

## 9. Runtime Governance Requirements (for agent-facing systems)

> DocSearch operates as a live AI search agent that generates synthesized answers from
> internal documentation. Its outputs directly affect engineers making technical decisions.
> Runtime governance is required.

### Trigger condition

Runtime governance artifacts are REQUIRED because DocSearch's live outputs (search results,
synthesized answers, source citations) directly affect users without guaranteed human review
of every response.

### Required artifacts

- **Trust Envelope (required):** Defines authorized output categories for search results, generated answers, citations, clarifying questions, and error messages.
- **Escalation Contract (required):** Covers access violation detection, PII exposure risk, low-confidence answers, and user-requested human handoff.
- **Interaction State Model (required):** Defines search interaction lifecycle from idle through query processing, answer generation, follow-up, error recovery, and escalation.

### Runtime enforcement rules

- No live deployment without versioned Trust Envelope, Escalation Contract, and Interaction State Model.
- Runtime authority is bounded by the Trust Envelope, not by BUILD autonomy tier alone.
- Escalation paths must be tested for each escalation class (E0, E1, E2, EX) before release.
- Scenario Bank must map to interaction state paths for runtime coverage.

### Runtime evidence expectations

| Metric | Threshold | Owner |
|---|---|---|
| Unsafe-answer rate (trust envelope violations per interaction) | < 0.1% | Search Platform Team |
| False-escalation rate | < 5% | Search Platform Team |
| Missed-escalation rate | < 0.5% | Search Platform Team |
| State violation rate (unauthorized output for current state) | < 0.1% | Search Platform Team |
| Escalation success rate | > 99% | Search Platform Team |
| Fallback success rate | > 95% | Search Platform Team |

## 10. Amendment Process

1. **Proposal:** Any team member may propose an amendment with rationale.
2. **Impact assessment:** Evaluate effects on active Intent Contracts and runtime artifacts.
3. **Review:** Requires Search Platform Tech Lead sign-off plus one additional reviewer.
4. **Documentation:** Record date, rationale, changes, and compatibility impact.
5. **Communication:** Re-initialize active agents after constitution changes.
6. **Versioning:** Increment constitution version with each amendment.

### Amendment log

| Version | Date | Change | Rationale | Approved by |
|---|---|---|---|---|
| 1.0 | 2026-04-03 | Initial constitution | Project kickoff | Sarah Chen (Tech Lead) |
