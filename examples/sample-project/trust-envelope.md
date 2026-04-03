# Trust Envelope: DocSearch Semantic Search Agent

> **Version:** 1.0 | **Date:** 2026-04-03 | **Owner:** Search Platform Team
> **Intent Contract:** 042-semantic-search/intent-contract.md
>
> Trust Envelope defines the positive runtime boundary: what the DocSearch agent is authorized to output or do.

---

## 1. Scope

- **Agent surface:** Web chat interface (search bar with answer panel)
- **User groups:** Authenticated engineers, engineering managers, and technical writers (~200 users)
- **Runtime context:** Production internal tool, accessed via company SSO
- **Out of scope:** API-only consumers (future), Slack bot integration (future), admin configuration interface

## 2. Authorized Output Categories

| Category ID | Name | Description | Allowed examples | Explicit boundary |
|---|---|---|---|---|
| TE-1 | Search results display | Display ranked list of matching documents with title, source system, snippet, and relevance indicator | "Found 12 results across Confluence and Notion. Top result: 'Payments Service Setup Guide' (Confluence)" | Must not display results from documents the user cannot access. Must not fabricate document titles or snippets. |
| TE-2 | Answer generation | Generate a synthesized natural language answer from retrieved document chunks | "To set up local development for the payments service, first clone the repo and run the setup script [1]. Then configure your local database using the migration tool [2]." | Every factual claim must have a source citation. Must not generate answers when no relevant results exist. Must not provide information beyond what the source documents contain. |
| TE-3 | Source citations | Display structured citations linking to original documents | "[1] Payments Setup Guide, Confluence, last updated 2026-03-15. [Link]" | Must link to the actual source document. Must include source system, document title, and last-updated date. Must not fabricate citation metadata. |
| TE-4 | Clarifying questions | Ask the user to disambiguate when the query matches multiple distinct contexts | "I found documentation about 'service mesh' for several projects: Project Atlas, Project Nova, Project Beacon. Which are you looking for?" | Maximum 2 follow-up clarifying questions per search session. Questions must present concrete options, not open-ended prompts. Must not ask for information unrelated to the search query. |
| TE-5 | Error and status messages | Display system status, degradation notices, and error messages | "Some sources are temporarily unavailable. Results may be incomplete." / "No matching documentation found. Try different search terms." | Must not expose internal system details, stack traces, or infrastructure information. Must always provide a constructive next step. |

## 3. Confidence Policy

| Category ID | Confidence level | Runtime flexibility | Notes |
|---|---|---|---|
| TE-1 | scripted | Fixed output format. Result cards follow a strict template: title, source, snippet, link. | No variation in structure. Content varies based on retrieved documents. |
| TE-2 | bounded generation | Generated text, constrained by source material and citation requirement. | LLM generates the answer, but every claim must trace to a retrieved chunk. Confidence score displayed when below 0.7. |
| TE-3 | templated | Constrained variation. Citation format is fixed; content fields populated from document metadata. | Template: "[N] {title}, {source_system}, last updated {date}. [Link]" |
| TE-4 | templated | Constrained variation. Question structure is fixed; options populated from query analysis. | Template: "I found documentation about '{topic}' for several {context_type}: {option_list}. Which are you looking for?" Max 5 options. |
| TE-5 | scripted | Fixed messages from an approved message catalog. | All error and status messages are pre-written and code-reviewed. No dynamic generation. |

## 4. Disallowed Output Classes

- **Document modification:** The agent must never create, edit, delete, or move documents in any source system.
- **Restricted content sharing:** The agent must never display, summarize, quote, or reference content from documents the requesting user cannot access in the source system.
- **Uncited answers:** The agent must never provide factual answers without at least one source citation.
- **Legal or HR advice:** The agent must never interpret, advise on, or provide guidance about legal, HR, or compliance matters, even if the source documents contain such content.
- **Personal opinions or recommendations:** The agent must never express preferences, opinions, or recommendations beyond what the source documents state.
- **Access control modification:** The agent must never modify, suggest modifications to, or provide instructions for changing document access controls.
- **Cross-user data sharing:** The agent must never reference one user's search history, queries, or results in another user's session.
- **External data:** The agent must never include information from outside the indexed documentation sources.

## 5. Violation Severity

| Severity | Definition | Example | Required response |
|---|---|---|---|
| Critical | Access control breach or PII exposure | Restricted document content shown to unauthorized user. PII appears in search results. | Immediate E2 escalation. Block further output. Trigger incident response. Preserve evidence. |
| High | Significant trust boundary breach | Answer generated without any citations. Answer contradicts source material without flagging the contradiction. | E1 escalation. Block the specific answer. Log for review. Serve fallback (raw results). |
| Medium | Boundary drift, minor policy miss | Clarifying question asked a third time (exceeding max 2). Answer includes hedging language not in source docs. | Log the violation. Apply correction. Monitor for pattern. |
| Low | Style or format deviation | Citation missing the last-updated date. Error message slightly different from catalog. | Log. Fix in next release. No runtime intervention needed. |

## 6. Detection & Monitoring

| Signal | Detection method | Alert threshold | Owner |
|---|---|---|---|
| Trust envelope violation rate | Automated classifier scanning all generated answers against citation and access control rules | > 0.1% of interactions | Search Platform Team |
| Unsafe-answer rate | Post-hoc sampling review (5% weekly) plus automated hallucination detector | > 0.1% of answers | Search Platform Team |
| Uncited-claim rate | Automated check: every sentence in generated answer must map to a retrieved chunk | > 1% of answers | Search Platform Team |
| Access control filter failure | Audit log comparison: documents in results vs. user permissions | Any single occurrence | Security Team |
| Disallowed category output | Keyword and intent classifier on all agent outputs | Any single occurrence | Search Platform Team |

## 7. Escalation Integration

- **Escalation Contract version:** 1.0
- **When envelope violations escalate automatically:**
  - Any Critical severity violation triggers E2 immediately.
  - Any High severity violation triggers E1.
  - 3+ Medium severity violations within a 1-hour window for a single user triggers E1.
- **Fallback behavior before human takeover:** Display raw search results (TE-1 only, no generated answers) with a message: "We are showing basic search results while we resolve an issue. A team member has been notified."

## 8. Scenario & State Mapping

| Scenario ID | State path | Allowed categories |
|---|---|---|
| S001 | ST-1, ST-2, ST-3, ST-1 | TE-1, TE-2, TE-3 |
| S002 | ST-1, ST-2, ST-3, ST-1 | TE-1, TE-5 |
| S003 | ST-1, ST-2, ST-4, ST-2, ST-3, ST-1 | TE-1, TE-2, TE-3, TE-4 |
| S004 | ST-1, ST-2, ST-3, ST-1 | TE-1, TE-5 |
| S005 | ST-1, ST-2, ST-5, ST-3, ST-1 | TE-1, TE-2, TE-3, TE-5 |
| S006 | ST-1, ST-2, ST-3, ST-1 | TE-1, TE-2, TE-3 |

## 9. Approval & Change Log

- **Approved by:** Sarah Chen (Tech Lead), James Park (Security Lead)
- **Approval date:** 2026-04-03
- **Review cadence:** Monthly, or immediately upon any Critical/High violation

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| 1.0 | 2026-04-03 | Initial trust envelope | Feature launch preparation | Sarah Chen, James Park |
