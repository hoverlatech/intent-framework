# Escalation Contract: DocSearch Semantic Search Agent

> **Version:** 1.0 | **Date:** 2026-04-03 | **Owner:** Search Platform Team
> **Intent Contract:** 042-semantic-search/intent-contract.md
>
> Escalation Contract defines every path from agent-handled interaction to human involvement.

---

## 1. Scope

- **Applies to:** DocSearch web search interface (all user-facing search interactions)
- **Users affected:** All authenticated DocSearch users (~200 engineers)
- **Runtime systems involved:** PagerDuty (on-call alerting), Slack #docsearch-incidents channel, internal ticketing system (Jira)

## 2. Escalation Classes

| Class | Trigger type | Description | Priority |
|---|---|---|---|
| E0 | No escalation | Agent handles the interaction within the Trust Envelope. Normal search, answer generation, clarification flows. | Lowest |
| E1 | Urgent escalation | Potential risk or degraded experience. Includes: access violation attempt detected, repeated low-confidence answers, full search failure, connector outage affecting all sources. | High |
| E2 | Critical escalation | Safety or compliance incident. Includes: PII detected in search results, restricted content exposed to unauthorized user, security breach indicators. | Highest |
| EX | User-requested | User explicitly requests human help via "Talk to a human" button or types a request like "let me speak to someone." | Medium |

## 3. Protocol Per Class

### E0 - No Escalation

Normal operation. The agent handles the full interaction within Trust Envelope boundaries.

- Search results displayed (TE-1)
- Answers generated with citations (TE-2, TE-3)
- Clarifying questions asked when needed (TE-4, max 2)
- Error messages shown for expected failure states (TE-5)

No human involvement required.

### E1 - Urgent

**Triggers:**
- Access control filter detects an attempted bypass or inconsistency
- 3+ consecutive queries for a single user return confidence scores below 0.5
- All source connectors are simultaneously unavailable
- Answer generation fails 5+ times within a 10-minute window

**Protocol:**

1. **Detection:** System detects the E1 trigger condition via runtime monitoring.
2. **User communication:** Display message: "We have noticed an issue and are looking into it. You can continue searching, but results may be limited."
3. **Alert:** Send PagerDuty alert to on-call Search Platform engineer. Post to #docsearch-incidents Slack channel with trigger details.
4. **Fallback behavior:** Switch to degraded mode. Serve raw search results only (no answer generation). Disable clarification flow.
5. **Resolution:** On-call engineer acknowledges within timeout, investigates, and resolves. System returns to E0 when trigger condition clears.

- **Timeout to human acknowledgment:** 15 minutes
- **Max wait before fallback:** Fallback activates immediately upon E1 trigger. Human acknowledgment is for investigation, not for restoring service.

### E2 - Critical

**Triggers:**
- PII detected in any search result or generated answer (SSN patterns, credit card numbers, personal health information)
- Restricted document content confirmed exposed to an unauthorized user
- Security team reports a breach involving DocSearch data
- Access control system reports a permissions sync failure affecting result filtering

**Protocol:**

1. **Immediate stop:** Halt answer generation for the affected session. Do not display the compromised results.
2. **User communication:** Display message: "We encountered a security issue and have paused your search session. Our team has been notified and will follow up shortly."
3. **Critical alert:** Send PagerDuty P1 alert to on-call Security engineer AND Search Platform Tech Lead. Post to #docsearch-incidents and #security-incidents Slack channels.
4. **Evidence preservation:** Log the full request/response chain for the affected interaction. Preserve access control state snapshot.
5. **Incident logging:** Create Jira incident ticket automatically with severity "Critical," linked logs, and affected user information.
6. **Broader impact assessment:** If the trigger indicates a systemic issue (e.g., permissions sync failure), disable answer generation for all users until resolved.

- **Timeout to critical responder:** 5 minutes
- **Fallback path:** If no responder acknowledges within 5 minutes, automatically disable DocSearch answer generation globally and display maintenance message to all users. Page the secondary on-call and engineering manager.

### EX - User-Requested

**Triggers:**
- User clicks the "Talk to a human" button in the search interface
- User types a message like "help me find someone who knows about this," "I need to talk to an expert," or similar

**Protocol:**

1. **Acknowledgment:** Display message: "Got it. Let me connect you with someone who can help."
2. **Context collection:** Gather the user's search query, any clarification responses, and the most recent search results.
3. **Routing:** Create a Jira ticket in the Documentation Help queue with the collected context. Tag the relevant team based on the search topic (if identifiable).
4. **User communication:** Display message: "I have created a help request with your search context. A team member will follow up within 4 business hours. Your request ID is {ticket_id}."
5. **Continuation:** User can continue searching while awaiting human follow-up.

- **Timeout to human response:** 4 business hours
- **Fallback path:** If no response within 4 business hours, auto-escalate to the Documentation Team Lead and notify the user: "Your request is being escalated for faster attention."

## 4. User Communication

| Stage | User message template | Channel |
|---|---|---|
| E1 escalation started | "We have noticed an issue and are looking into it. You can continue searching, but results may be limited." | In-app banner |
| E1 waiting for resolution | "Our team is investigating. Basic search results are still available." | In-app banner |
| E1 resolved | "The issue has been resolved. Full search functionality is restored." | In-app banner (auto-dismiss after 30s) |
| E2 escalation started | "We encountered a security issue and have paused your search session. Our team has been notified and will follow up shortly." | In-app modal (blocks interaction) |
| E2 resolved (user-specific) | "The issue has been resolved. You can resume searching. If you have questions, contact security@company.com." | In-app modal + email |
| EX acknowledged | "Got it. Let me connect you with someone who can help." | In-app message |
| EX ticket created | "I have created a help request with your search context. A team member will follow up within 4 business hours. Your request ID is {ticket_id}." | In-app message |
| EX timeout/escalated | "Your request is being escalated for faster attention. We apologize for the delay." | In-app message + email |

## 5. Fallback Paths

| Failure condition | Fallback action | Owner |
|---|---|---|
| On-call engineer unavailable (E1) | Auto-page secondary on-call. If no response in 30 minutes, page Engineering Manager. | Search Platform Team |
| Security responder unavailable (E2) | Disable DocSearch answer generation globally. Page Engineering Director. | Security Team |
| PagerDuty system down | Send alerts via Slack bot and email fallback. | Platform Engineering |
| Jira unavailable (EX tickets) | Log ticket details to a fallback queue in PostgreSQL. Retry ticket creation every 5 minutes. Notify user that help request was received. | Search Platform Team |
| Slack unavailable | Rely on PagerDuty and email. Log a note that Slack notification was skipped. | Search Platform Team |

## 6. Evidence Capture

| Event | Required fields | Retention | Audit owner |
|---|---|---|---|
| Escalation trigger | Trigger type, timestamp, user ID, query text, escalation class, session ID | 1 year | Search Platform Team |
| Handoff success/failure | Escalation class, time to acknowledgment, responder ID, resolution action | 1 year | Search Platform Team |
| Timeout/fallback activation | Escalation class, timeout duration, fallback action taken, affected users | 1 year | Search Platform Team |
| E2 incident details | Full request/response chain, access control state, affected documents, PII scan results | 3 years (compliance) | Security Team |
| EX user request | Query context, search results shown, user feedback, ticket ID, resolution time | 1 year | Documentation Team |

## 7. Failure Modes

| Failure mode | Severity | Detection | Mitigation |
|---|---|---|---|
| Missed escalation (should have been E1/E2 but was not triggered) | Critical | Post-hoc audit of trust envelope violations that did not generate alerts. Weekly review of low-confidence answer logs. | Improve trigger sensitivity. Add redundant detection paths. Review threshold settings. |
| False escalation (E1/E2 triggered unnecessarily) | Medium | Track escalation rate vs. confirmed incidents. Alert if false-positive rate exceeds 5%. | Tune trigger thresholds. Add confirmation step for borderline cases. |
| Incomplete handoff (escalation triggered but context not delivered to responder) | High | Monitor ticket creation success rate. Alert if context attachment fails. | Retry context delivery. Fall back to minimal ticket with session ID for manual lookup. |
| Escalation storm (many E1/E2 triggers in rapid succession) | High | Rate limiting on escalation triggers. Alert if > 10 escalations in 5 minutes. | Deduplicate triggers. Batch into single incident. Page senior on-call directly. |

## 8. Priority Matrix

| If multiple triggers apply | Winning class | Rule |
|---|---|---|
| E2 + EX | E2 | Safety and compliance always take priority over user-requested handoff. |
| E1 + EX | EX | User-requested handoff is honored alongside the E1 investigation. Both proceed in parallel. |
| Multiple E1 triggers | Single E1 | Deduplicate into one incident. Include all trigger details in the alert. |
| E1 + E2 | E2 | Critical always supersedes urgent. E1 investigation folds into the E2 incident. |

## 9. Validation Checklist

- [ ] E0 normal flow verified end-to-end (S001, S002, S003, S006)
- [ ] E1 escalation triggered and resolved in staging (simulated connector outage, low-confidence cascade)
- [ ] E2 escalation triggered and resolved in staging (simulated PII detection, simulated access control failure)
- [ ] EX user-requested handoff creates ticket with full context
- [ ] Timeout behavior verified for E1 (15 min), E2 (5 min), EX (4 business hours)
- [ ] Fallback behavior verified for each failure condition
- [ ] Evidence logging verified for all escalation events
- [ ] User communication templates approved by UX and Legal
- [ ] PagerDuty routing rules configured and tested
- [ ] Slack channel integrations verified

## 10. Approval & Change Log

| Version | Date | Change | Reason | Approved by |
|---|---|---|---|---|
| 1.0 | 2026-04-03 | Initial escalation contract | Feature launch preparation | Sarah Chen (Tech Lead), James Park (Security Lead) |
