# Implementation Plan: Semantic Search across Internal Documentation

> **Branch:** 042-semantic-search | **Date:** 2026-04-03 | **Spec:** 042-semantic-search/intent-contract.md
> **INTENT Phase:** EXPLORE, Direction Check

---

## Governance Context

| Dimension | Value | Implication for this plan |
|---|---|---|
| **Risk tier** | Medium | Requires scenario-backed evidence. Access control logic is the highest-risk sub-component (treated as High within this plan). |
| **Proof tier target** | P2 | All 6 scenarios (S001-S006) must pass. Integration tests for all connectors. Load testing for latency SLO. |
| **Autonomy tier target (BUILD)** | A2 | Agent implements, human reviews before merge. Access control changes require A0 (human decision-maker). |

### Runtime governance context

| Dimension | Value | Implication for runtime behavior |
|---|---|---|
| **Runtime governance required** | Yes | Trust Envelope, Escalation Contract, and Interaction State Model must be versioned and deployed before launch. |
| **Trust Envelope version** | 1.0 | Generated answers bounded by citation requirement. Five output categories (TE-1 through TE-5) with strict confidence policies. |
| **Escalation Contract version** | 1.0 | E0/E1/E2/EX escalation paths. PagerDuty and Slack integration required. E2 triggers global answer generation shutdown. |
| **Interaction State Model version** | 1.0 | Six states (ST-1 through ST-6). Per-state output restrictions. Server-side state validation. |

### Constitution compliance checkpoint

- [x] Architecture principles respected (FastAPI, React, PostgreSQL + pgvector, Redis)
- [x] Security requirements respected (SSO, document-level ACLs, no PII in indexes)
- [x] Reliability standards achievable with this design (p95 < 2s, 99.9% uptime, degraded mode)
- [x] Agent boundaries respected (no access control modification, no restricted doc indexing without approval)
- [x] New dependencies listed for review (see below)
- [x] Runtime trigger condition evaluated and documented (runtime governance required)

## Technical Context

- **Runtime:** Python 3.12, FastAPI, uvicorn
- **Data layer:** PostgreSQL 16 with pgvector extension, Redis 7
- **Auth:** Company SSO (SAML 2.0) via existing auth gateway
- **External integrations:** Confluence REST API, GitHub REST API, Notion API, Google Docs API (read-only)
- **UI framework:** React 18 (TypeScript), Vite, internal component library
- **Testing stack:** pytest (unit + integration), Playwright (e2e), locust (load testing)

### New dependencies (human review required)

| Package | Purpose | Why this one | Risk |
|---|---|---|---|
| pgvector (PostgreSQL extension) | Vector similarity search | Native PostgreSQL extension. Avoids separate vector DB. Well-maintained, production-proven. | Low. Open-source, widely adopted. |
| sentence-transformers | Embedding generation | Supports multiple embedding models. Allows local or API-based generation. | Medium. Model selection affects quality and cost. |
| langchain (core only) | LLM orchestration for answer synthesis | Standardized interface for prompt management and retrieval-augmented generation. | Medium. Large dependency surface. Pin to specific version. |
| tiktoken | Token counting for context window management | Official OpenAI tokenizer. Fast and accurate. | Low. Lightweight, well-maintained. |
| redis-py | Redis client for caching | Standard Python Redis client. Already used elsewhere in the org. | Low. |
| httpx | Async HTTP client for connector API calls | Modern async HTTP client. Better connection pooling than requests. | Low. Well-maintained, widely adopted. |

## Directory Structure

```
src/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── search.py          # /api/search endpoint
│   │   │   ├── health.py          # /api/health endpoint
│   │   │   └── feedback.py        # /api/feedback endpoint
│   │   ├── middleware/
│   │   │   ├── auth.py            # SSO authentication middleware
│   │   │   └── rate_limit.py      # Rate limiting middleware
│   │   └── app.py                 # FastAPI application setup
│   ├── connectors/
│   │   ├── base.py                # Abstract connector interface
│   │   ├── confluence.py          # Confluence REST API connector
│   │   ├── github_wiki.py         # GitHub Wiki connector
│   │   ├── notion.py              # Notion API connector
│   │   └── google_docs.py         # Google Docs API connector
│   ├── pipeline/
│   │   ├── embeddings.py          # Embedding generation pipeline
│   │   ├── indexer.py             # Document indexing orchestrator
│   │   ├── chunker.py             # Document chunking logic
│   │   └── pii_filter.py          # PII detection and filtering
│   ├── search/
│   │   ├── query_parser.py        # Query parsing and embedding
│   │   ├── retriever.py           # Vector similarity retrieval
│   │   ├── ranker.py              # Result ranking and deduplication
│   │   ├── access_control.py      # Permission filtering
│   │   └── synthesizer.py         # Answer generation with citations
│   ├── governance/
│   │   ├── trust_envelope.py      # Runtime trust envelope enforcement
│   │   ├── state_machine.py       # Interaction state management
│   │   └── escalation.py          # Escalation trigger detection and routing
│   └── config/
│       ├── settings.py            # Application configuration
│       └── constants.py           # Shared constants
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.tsx       # Search input component
│   │   │   ├── AnswerPanel.tsx     # Synthesized answer display
│   │   │   ├── ResultsList.tsx     # Search results list
│   │   │   ├── CitationCard.tsx    # Source citation component
│   │   │   ├── ClarifyDialog.tsx   # Clarifying question dialog
│   │   │   ├── StatusBanner.tsx    # System status and error display
│   │   │   └── HumanHelpButton.tsx # "Talk to a human" button
│   │   ├── hooks/
│   │   │   ├── useSearch.ts        # Search API integration hook
│   │   │   └── useSessionState.ts  # Client-side state mirror
│   │   └── App.tsx
│   └── vite.config.ts
tests/
├── unit/
│   ├── test_query_parser.py
│   ├── test_chunker.py
│   ├── test_ranker.py
│   ├── test_access_control.py
│   ├── test_pii_filter.py
│   └── test_trust_envelope.py
├── integration/
│   ├── test_confluence_connector.py
│   ├── test_github_connector.py
│   ├── test_notion_connector.py
│   ├── test_google_docs_connector.py
│   ├── test_search_pipeline.py
│   └── test_escalation_paths.py
├── e2e/
│   ├── test_happy_path_search.py      # S001
│   ├── test_no_results.py             # S002
│   ├── test_ambiguous_query.py        # S003
│   ├── test_access_control.py         # S004
│   ├── test_degraded_mode.py          # S005
│   └── test_multi_source_synthesis.py # S006
└── load/
    └── locustfile.py                  # Load testing (50 concurrent users)
```

## Data Model

### PostgreSQL Tables

**documents** - Metadata for indexed documents.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | Auto-generated |
| source_system | VARCHAR(50) | confluence, github_wiki, notion, google_docs |
| source_id | VARCHAR(255) | ID in the source system |
| title | VARCHAR(500) | Document title |
| url | TEXT | Direct link to the source document |
| last_synced_at | TIMESTAMP | Last successful sync time |
| last_modified_at | TIMESTAMP | Last modification in source system |
| access_control_metadata | JSONB | Serialized permission info from source system |

**document_chunks** - Chunked content with embeddings.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | Auto-generated |
| document_id | UUID (FK) | References documents.id |
| chunk_index | INTEGER | Position within the document |
| content | TEXT | Chunk text content (PII-filtered) |
| embedding | vector(1536) | pgvector embedding column |
| token_count | INTEGER | Token count for context window budgeting |

**search_sessions** - Audit log of search interactions.

| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | Session identifier |
| user_id | VARCHAR(255) | SSO user identifier |
| query_text | TEXT | Original search query |
| state_path | JSONB | Array of states traversed |
| escalation_class | VARCHAR(10) | E0, E1, E2, or EX |
| created_at | TIMESTAMP | Session start |
| completed_at | TIMESTAMP | Session end |

### Redis Keys

- `session:{session_id}` - Session state (JSON, 30-min TTL)
- `cache:query:{query_hash}` - Cached search results (JSON, 15-min TTL)
- `rate_limit:user:{user_id}` - Rate limit counter (sliding window)
- `connector_health:{connector_name}` - Connector health status (60s TTL)

## API Design

### POST /api/search

Submit a search query. Returns search results and a synthesized answer.

**Request:**
```json
{
  "query": "How do I set up local development for the payments service?",
  "session_id": "optional-existing-session-id",
  "clarification_context": null
}
```

**Response (success):**
```json
{
  "session_id": "uuid",
  "state": "ST-3",
  "answer": {
    "text": "To set up local development...",
    "confidence": 0.87,
    "citations": [
      {"index": 1, "title": "Payments Setup Guide", "source": "confluence", "url": "https://...", "last_updated": "2026-03-15"}
    ]
  },
  "results": [
    {"title": "...", "source": "confluence", "snippet": "...", "url": "...", "relevance": 0.92}
  ],
  "clarification": null,
  "status": {"degraded_sources": [], "message": null}
}
```

**Response (clarification needed):**
```json
{
  "session_id": "uuid",
  "state": "ST-4",
  "answer": null,
  "results": [],
  "clarification": {
    "question": "I found documentation about 'service mesh' for several projects. Which are you looking for?",
    "options": ["Project Atlas", "Project Nova", "Project Beacon"]
  },
  "status": {"degraded_sources": [], "message": null}
}
```

**Error responses:** 401 (unauthenticated), 429 (rate limited), 500 (internal error), 503 (all connectors down).

### POST /api/feedback

Submit relevance feedback for a search result.

**Request:**
```json
{
  "session_id": "uuid",
  "rating": "positive",
  "comment": "optional free-text"
}
```

### GET /api/health

Returns system health including per-connector status. Used by monitoring and the frontend status indicator.

## Component / Service Architecture

The system has three main data flow paths:

**Indexing pipeline (async, runs on schedule):**
Connectors pull documents from source APIs. Documents are chunked, PII-filtered, embedded, and stored in PostgreSQL with pgvector. Access control metadata is synced from source systems.

**Search request flow (synchronous, user-facing):**
User query arrives at the FastAPI search endpoint. Auth middleware validates SSO token. Rate limiter checks usage. Query parser generates an embedding. Retriever performs pgvector similarity search. Access control filter removes unauthorized results. Ranker scores and deduplicates. Synthesizer generates an answer with citations via LLM. Trust envelope validator checks the answer before returning it. State machine tracks the interaction lifecycle.

**Governance layer (cross-cutting):**
Trust envelope enforcement validates all outputs before they reach the user. State machine enforces per-state output restrictions. Escalation triggers monitor for E1/E2 conditions. All transitions emit OpenTelemetry spans.

## Implementation Sequence

### Phase 1: Foundation

**Deliverables:**
- Abstract connector interface (`connectors/base.py`)
- Confluence connector (first connector, proves the pattern)
- Document chunking logic with configurable chunk size
- PII detection filter (regex-based for v1, ML-based in future)
- Embedding generation pipeline (sentence-transformers)
- PostgreSQL schema (documents, document_chunks tables)
- pgvector setup and basic similarity search
- Integration test for Confluence connector

**Dependencies:** PostgreSQL with pgvector provisioned. Confluence API credentials available in staging. Embedding model selected (open question, use text-embedding-3-small as default).

**Verification:**
- Confluence connector integration test passes.
- Documents are chunked, embedded, and stored in pgvector.
- Basic similarity search returns relevant results for test queries.
- PII filter catches SSN, credit card, and email patterns in test data.

### Phase 2: Core Logic

**Deliverables:**
- Remaining connectors (GitHub Wiki, Notion, Google Docs)
- Query parser with embedding generation
- Vector similarity retriever with configurable thresholds
- Result ranker with deduplication
- Access control filtering (checks user permissions against source system ACLs)
- Answer synthesizer with citation generation (LLM-based)
- FastAPI search endpoint (`/api/search`)
- SSO auth middleware
- Rate limiting middleware
- Redis caching layer
- Integration tests for all connectors
- Unit tests for access control, ranking, and synthesis

**Dependencies:** Phase 1 complete. API credentials for GitHub, Notion, Google Docs. LLM API access (for answer synthesis). Redis provisioned.

**Verification:**
- All 4 connector integration tests pass.
- Access control filtering correctly blocks unauthorized documents (test matrix: allow, deny, mixed).
- Search endpoint returns relevant results with citations for test queries.
- Rate limiting enforced per user.
- p95 search latency < 2s under 10 concurrent users.

### Phase 3: User-facing / Runtime Integration

**Deliverables:**
- React search UI (SearchBar, AnswerPanel, ResultsList, CitationCard)
- Clarifying question dialog (ClarifyDialog)
- System status banner (StatusBanner)
- "Talk to a human" button and EX escalation flow (HumanHelpButton)
- Frontend search hook with session state management
- Governance runtime layer:
  - Trust envelope enforcement (`governance/trust_envelope.py`)
  - Interaction state machine (`governance/state_machine.py`)
  - Escalation trigger detection and routing (`governance/escalation.py`)
- Feedback endpoint (`/api/feedback`)
- Health endpoint (`/api/health`)
- Degraded mode UI (partial results with notice)
- Accessibility: WCAG 2.1 AA compliance, keyboard navigation, screen reader support

**Dependencies:** Phase 2 complete. Internal component library access. PagerDuty and Slack webhook configuration. Jira API access for EX ticket creation.

**Verification:**
- End-to-end happy path (S001) works in staging.
- Clarification flow (S003) works in staging.
- Degraded mode (S005) activated by simulating connector failure.
- "Talk to a human" creates a Jira ticket with search context.
- Trust envelope validator catches test violations (uncited answer, restricted content).
- State machine enforces per-state output restrictions.
- Accessibility audit passes WCAG 2.1 AA.

### Phase 4: Validation and Hardening

**Deliverables:**
- Full Scenario Bank execution (S001 through S006, all e2e tests)
- Load testing (50 concurrent users, p95 < 2s)
- Escalation path testing (simulated E1, E2, EX in staging)
- Trust envelope violation detection verification
- Constitution drift check (verify all architecture, security, reliability requirements)
- Runtime governance verification:
  - Trust envelope compliance rate measured
  - Escalation path success rate measured
  - State violation rate measured
  - Missed/false escalation rates measured
- Security review of access control implementation
- PII filter effectiveness audit
- Production monitoring dashboards (OpenTelemetry, Grafana)
- Runbook for on-call engineers

**Dependencies:** Phase 3 complete. Security team availability for review. Load testing environment provisioned.

**Verification:**
- All 6 scenarios pass end-to-end.
- Load test confirms p95 < 2s at 50 concurrent users.
- Trust envelope violation rate < 0.1% in staging.
- All escalation paths (E1, E2, EX) verified end-to-end.
- State violation rate < 0.1% in staging.
- Security review complete with no blocking findings.
- Constitution compliance confirmed (no drift from declared architecture, security, or reliability requirements).

## Drift Detection Checkpoints

| After Phase | Check | Method | Blocks next phase? |
|---|---|---|---|
| Phase 1 | Schema aligns with declared data model | Validator compares migration output to plan | Yes |
| Phase 1 | Connector interface matches declared contract | Interface test + review | Yes |
| Phase 2 | API behavior aligns with declared endpoints | Contract tests against /api/search spec | Yes |
| Phase 2 | Access control logic matches security requirements | Test matrix review + security spot-check | Yes |
| Phase 3 | Scenarios and state paths are implemented | Scenario walk-through + state machine tests | Yes |
| Phase 3 | Trust envelope categories enforced per state | Trust envelope integration tests | Yes |
| Phase 4 | Scenario Bank full pass | Automated e2e tests (S001-S006) | Yes |
| Phase 4 | Constitution compliance | Architecture, security, reliability analysis + review | Yes |
| Phase 4 | Dependency drift from plan | Diff of installed packages vs. declared dependencies | Yes |

### Runtime governance checkpoints

| Check | Method | Required threshold |
|---|---|---|
| Trust Envelope compliance | Automated classifier + 5% weekly sampling review | Violation rate < 0.1% |
| Escalation path success | Simulated E1/E2/EX walkthroughs in staging | 100% of paths reach resolution |
| Missed/false escalation rate | Scenario replay + manual review of edge cases | Missed < 0.5%, false < 5% |
| State violation rate | State-path assertions on all e2e test runs | < 0.1% |

## Contribution Map

| File/Directory | Author | Review Required |
|---|---|---|
| src/backend/connectors/ | Agent (A2) | Human review before merge |
| src/backend/search/access_control.py | Human (A0) | Human implements, peer review |
| src/backend/search/ (other files) | Agent (A2) | Human review before merge |
| src/backend/pipeline/pii_filter.py | Human (A0) | Human implements, security review |
| src/backend/governance/ | Agent (A2) | Human review before merge, security spot-check |
| src/backend/api/middleware/auth.py | Human (A0) | Human implements, security review |
| src/backend/api/ (other files) | Agent (A2) | Human review before merge |
| src/frontend/ | Agent (A2) | Human review before merge |
| tests/ | Agent (A2) | Human review before merge |

## Open Technical Decisions

- [ ] **Embedding model selection:** text-embedding-3-small (OpenAI, $0.02/1M tokens) vs. BGE-large (open-source, self-hosted). Decision needed before Phase 1. Default to text-embedding-3-small for faster iteration.
- [ ] **Chunk size and overlap:** 512 tokens with 50-token overlap as starting point. May need tuning based on retrieval quality in Phase 2.
- [ ] **Re-sync frequency:** Hourly full sync vs. webhook-based incremental updates. Hourly for v1, webhooks for v2.
- [ ] **Duplicate document handling:** Deduplicate at index time (by content hash) or at query time (by URL). Recommend index-time deduplication for simplicity.

---

> **Direction Check:** Before `/speckit.tasks`, verify this plan has no constitution violations,
> no unjustified complexity, realistic sequencing, and complete runtime governance coverage.
