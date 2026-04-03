# Interaction State Model: DocSearch Semantic Search Agent

> **Version:** 1.0 | **Date:** 2026-04-03 | **Owner:** Search Platform Team
> **Intent Contract:** 042-semantic-search/intent-contract.md
>
> Interaction State Model defines valid runtime states, transitions, and per-state permissions.

---

## 1. Scope

- **Interaction type:** Web-based search chat (query/response with optional follow-up)
- **System boundary:** Governs the lifecycle of a single search session from query submission through answer delivery, follow-up, and resolution. A session starts when the user submits a query and ends when the user starts a new query, closes the search panel, or the session times out (30 minutes of inactivity).
- **Assumptions:** User is authenticated via SSO before any state transition occurs. Session state is stored in Redis with a 30-minute TTL. The frontend maintains a local state mirror for responsiveness.

## 2. State Definitions

| State ID | Name | Entry condition | Allowed Trust Envelope categories | Required data before exit | Exit conditions |
|---|---|---|---|---|---|
| ST-1 | Idle/Ready | Session initialized, or previous interaction completed | TE-5 (status messages only, e.g., "Ready to search") | None | User submits a search query |
| ST-2 | Query Processing | User submits a query or refines after clarification | TE-5 (processing indicator: "Searching...") | Parsed query, retrieved document chunks, access-filtered results | Processing completes (results found or no results), timeout (15s), or system error |
| ST-3 | Answer Generation | Query processing completes with results above relevance threshold | TE-1 (search results), TE-2 (generated answer), TE-3 (citations) | Generated answer with citations, or "no results" determination | Answer displayed to user, generation failure, or timeout (10s) |
| ST-4 | Follow-up | System asks a clarifying question (ambiguous query) or user asks a follow-up question | TE-4 (clarifying questions), TE-1 (partial results preview) | User response to clarification, or follow-up query text | User responds to clarification, user submits new query, or clarification timeout (60s) |
| ST-5 | Error Recovery | System error, connector failure, or timeout during ST-2 or ST-3 | TE-5 (error messages), TE-1 (partial results if available) | Error classification, fallback determination | Fallback response delivered, or escalation triggered |
| ST-6 | Escalated | E1, E2, or EX escalation triggered from any state | TE-5 (escalation status messages only) | Escalation class, trigger details, context snapshot | Human responder resolves, user cancels (EX only), or session timeout |

## 3. Transition Rules

| From state | Trigger | To state | Guard condition | Notes |
|---|---|---|---|---|
| ST-1 | User submits search query | ST-2 | Query is non-empty after trimming. Max query length 500 characters. | Log query submission event. Start processing timer. |
| ST-2 | Processing completes with results | ST-3 | At least 1 result above relevance threshold (0.65 cosine similarity) after access control filtering. | Pass filtered results to answer generation. |
| ST-2 | Processing completes, no results | ST-3 | Zero results above threshold after access control filtering. | ST-3 generates the "no results" response (still goes through answer generation state for consistent flow). |
| ST-2 | Ambiguity detected | ST-4 | 3+ distinct topic clusters with top results within 0.05 cosine similarity of each other. | System formulates a clarifying question. Max 5 options presented. |
| ST-2 | Processing timeout (15s) | ST-5 | Processing exceeds 15-second wall clock time. | Cancel in-flight connector requests. Collect any partial results. |
| ST-2 | Connector error (partial) | ST-5 | 1-3 connectors fail but at least 1 succeeds. | Mark failed connectors as degraded. Proceed with partial results. |
| ST-2 | All connectors fail | ST-5 | All 4 connectors return errors or timeout. | No results available. Error recovery determines fallback. |
| ST-3 | Answer displayed to user | ST-1 | Generated answer passes trust envelope validation (citations present, no disallowed content). | Log answer delivery. Return to idle for next query. |
| ST-3 | Answer generation fails | ST-5 | LLM call fails, or generated answer fails trust envelope validation. | Fall back to displaying raw search results without synthesis. |
| ST-3 | Answer generation timeout (10s) | ST-5 | Generation exceeds 10-second wall clock time. | Cancel LLM call. Fall back to raw results. |
| ST-4 | User selects clarification option | ST-2 | User selects one of the presented options. | Re-run query processing with the clarification context applied as a filter. |
| ST-4 | User submits new query instead | ST-2 | User types a new query rather than selecting a clarification option. | Treat as a fresh search. Discard clarification context. |
| ST-4 | Clarification timeout (60s) | ST-3 | User does not respond within 60 seconds. | Proceed with best-effort answer using the original query results. Log timeout. |
| ST-4 | Second clarification needed | ST-4 | After one clarification round, results are still ambiguous. | Maximum 2 clarification rounds. If still ambiguous after 2, proceed to ST-3 with grouped results. |
| ST-5 | Fallback response delivered | ST-1 | Degraded results or error message successfully shown to user. | Log error recovery outcome. Return to idle. |
| ST-5 | E1 escalation triggered | ST-6 | Error condition meets E1 criteria (all connectors down, repeated failures). | Initiate E1 protocol. |
| ST-5 | E2 escalation triggered | ST-6 | Error condition meets E2 criteria (access control failure, PII detected). | Initiate E2 protocol. Halt all output immediately. |
| ST-6 | Human resolves issue | ST-1 | Responder marks the escalation resolved. | Notify user that normal service is restored. Reset session state. |
| ST-6 | User cancels (EX only) | ST-1 | User clicks "Cancel" on the human help request. EX class only. | Close the help request ticket. Return to idle. |
| ST-6 | Session timeout (30 min) | Session ends | No activity for 30 minutes. | Clean up session state in Redis. If E2 active, escalation continues independently. |
| Any | User clicks "Talk to a human" | ST-6 | User initiates EX escalation from any state. | Capture current state context. Initiate EX protocol. |
| Any | E2 condition detected | ST-6 | PII or access control violation detected in any state. | Immediate override. Halt current output. Initiate E2 protocol. |

## 4. Escalation Overrides

| Condition | Forced state | Escalation class | Immediate action |
|---|---|---|---|
| PII detected in search results or generated answer | ST-6 | E2 | Halt output. Block result display. Trigger incident response. Preserve evidence. |
| Access control filter failure confirmed | ST-6 | E2 | Halt output. Block result display. Disable answer generation until resolved. |
| All source connectors unavailable for > 5 minutes | ST-6 | E1 | Display maintenance message. Alert on-call. Switch to cached results only (if available). |
| User requests human help | ST-6 | EX | Capture search context. Create help ticket. Inform user of expected response time. |
| 3+ trust envelope violations in 1 hour for same user | ST-6 | E1 | Disable answer generation for the affected user session. Alert on-call for investigation. |

## 5. Scenario Mapping

| Scenario ID | Expected state path | Escalation class |
|---|---|---|
| S001 | ST-1, ST-2, ST-3, ST-1 | E0 |
| S002 | ST-1, ST-2, ST-3, ST-1 | E0 |
| S003 | ST-1, ST-2, ST-4, ST-2, ST-3, ST-1 | E0 |
| S004 | ST-1, ST-2, ST-3, ST-1 | E0 (access control works correctly, no escalation needed) |
| S005 | ST-1, ST-2, ST-5, ST-3, ST-1 | E0 (degraded but functional) |
| S006 | ST-1, ST-2, ST-3, ST-1 | E0 |

Note: S004 escalates to E2 only if access control filtering fails (the failure mode). The happy path for S004 is E0 because the filter works correctly.

## 6. Runtime Validation

| Metric | Definition | Threshold | Owner |
|---|---|---|---|
| State violation rate | Output produced that is not authorized for the active state (e.g., answer generation output during ST-1) | < 0.1% of interactions | Search Platform Team |
| Invalid transition rate | State transition attempted that is not listed in the transition rules | < 0.05% of interactions | Search Platform Team |
| ST-2 processing latency | Time spent in Query Processing state | p95 < 2s | Search Platform Team |
| ST-3 generation latency | Time spent in Answer Generation state | p95 < 5s | Search Platform Team |
| ST-4 clarification rate | Percentage of queries entering the Follow-up state | < 20% of queries | Search Platform Team |
| ST-5 error recovery rate | Percentage of error recovery states that successfully deliver a fallback response | > 95% | Search Platform Team |
| ST-6 escalation resolution time | Time from escalation trigger to resolution | E1: < 1 hour, E2: < 30 min, EX: < 4 business hours | Search Platform Team / Security Team |

## 7. Prompt/Runtime Implementation Guidance

- Use per-state instruction blocks. Each state loads only its authorized Trust Envelope categories.
- ST-1 (Idle): Minimal prompt. Only TE-5 status messages are authorized. No answer generation capability loaded.
- ST-2 (Processing): Retrieval and ranking logic only. No LLM generation. Access control filtering runs here.
- ST-3 (Generation): LLM prompt loaded with strict citation requirements. System prompt includes: "Every factual claim must cite a source from the retrieved documents. Do not generate information not present in the provided context."
- ST-4 (Follow-up): Clarification question template loaded. Max 2 rounds enforced at the application layer, not just in the prompt.
- ST-5 (Recovery): Error message catalog loaded. No generation. Fallback logic determines which TE-1 results (if any) to display.
- ST-6 (Escalated): Only TE-5 escalation status messages. All other output categories disabled.
- Emit state transition events to the observability system (OpenTelemetry spans) for every transition.
- State transitions are validated server-side. The frontend reflects state but does not determine it.

## 8. Approval & Change Log

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| 1.0 | 2026-04-03 | Initial interaction state model | Feature launch preparation | Sarah Chen (Tech Lead) |
