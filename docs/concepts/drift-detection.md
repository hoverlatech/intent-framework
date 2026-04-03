# Drift Detection

## What It Is

Drift Detection is the mechanism that identifies when implementation, runtime behavior, or specifications diverge from the intended state. It operates at three levels: build-time, runtime, and spec drift. Together, these levels ensure that what you built, what is running, and what you documented stay aligned.

Drift is inevitable. Code evolves, production behavior shifts, and assumptions made during FRAME become outdated. Drift Detection does not prevent change. It makes change visible so teams can respond deliberately rather than discovering misalignment through incidents.


## Why It Exists

In traditional development, drift surfaces as bugs, outages, or audit findings. By that point, the gap between intent and reality is often large and expensive to close.

Agent-assisted development amplifies the drift risk. Agents generate code rapidly, potentially introducing subtle deviations from Intent Contract specifications that pass automated tests but violate the spirit of the design. Multiple agents working in parallel can create conflicting implementations that individually look correct but collectively diverge.

Drift Detection makes this class of problem detectable early. Build-time checks catch deviations before code merges. Runtime monitoring catches behavioral drift in production. Spec drift analysis catches when your documentation no longer matches reality.


## The Three Levels

### Level 1: Build-Time Drift

**What it checks:** CI validators verify that code changes conform to specifications, Constitution rules, and Intent Contract requirements.

**When it runs:** On every commit, pull request, and merge attempt.

**What happens on detection:** Violations block deployment. The change cannot proceed until the drift is resolved.

**Examples:**
- A new API endpoint missing required authentication (Constitution violation)
- Test coverage dropping below the threshold specified in the proof tier
- Code that contradicts the Intent Contract's stated constraints
- Scenario Bank test cases failing after implementation changes

**Implementation:** Build-time drift detection relies on your CI/CD pipeline. Typical checks include:

| Check Type | What It Validates |
|-----------|------------------|
| Constitution validators | Architecture rules, security requirements, coding standards |
| Proof tier gates | Test coverage, scenario coverage, non-functional test results |
| Intent Contract alignment | Declared constraints and non-goals are not violated |
| Scenario Bank regression | All existing scenarios still pass |

### Level 2: Runtime Drift

**What it checks:** Production behavior is continuously validated against the Trust Envelope, escalation paths, state transition rules, and expected performance characteristics.

**When it runs:** Continuously in production.

**What happens on detection:** Alerts fire. Depending on severity and configuration, the system may automatically restrict agent authority, trigger escalation, or halt specific operations.

**Examples:**
- A live agent producing outputs outside its Trust Envelope categories
- Response latency exceeding the quality bar defined in the Intent Contract
- Escalation paths not being followed when trigger conditions are met
- State transitions occurring that violate the Interaction State Model

**Implementation:** Runtime drift detection requires instrumentation aligned to your governance artifacts:

| Signal Source | What It Monitors |
|--------------|-----------------|
| Trust Envelope monitors | Output classification against authorized categories |
| Escalation tracking | Escalation trigger conditions vs. actual escalation rates |
| State model validators | State transitions against allowed transitions |
| Performance telemetry | Latency, error rates, throughput against quality bar |

### Level 3: Spec Drift

**What it checks:** Actual production telemetry is compared against the assumptions encoded in Intent Contracts and Scenario Banks.

**When it runs:** Periodically during the LEARN phase, or triggered by anomaly detection.

**What happens on detection:** Triggers a LEARN phase review. The team evaluates whether the spec needs updating, the implementation needs fixing, or both.

**Examples:**
- Users following a workflow path not covered by any scenario in the Scenario Bank
- Actual error rates significantly different (higher or lower) than expected
- Feature usage patterns that diverge from the user context assumptions in the Intent Contract
- Production load profiles that do not match the load test parameters used in P3 verification

**Implementation:** Spec drift detection compares production data against specification expectations:

| Comparison | What It Reveals |
|-----------|----------------|
| Usage patterns vs. scenarios | Missing or incorrect scenario coverage |
| Error distributions vs. failure modes | Undocumented failure paths |
| Performance profiles vs. quality bar | Unrealistic or outdated performance assumptions |
| User behavior vs. user context | Incorrect assumptions about how users interact |


## Drift Severity

Not all drift is equal. Classification helps teams prioritize responses:

| Severity | Criteria | Response |
|----------|----------|----------|
| Critical | Constitution violation or safety system deviation | Immediate action; may require rollback or agent authority restriction |
| High | Trust Envelope breach or escalation path failure | Urgent investigation; restrict affected operations |
| Medium | Performance degradation or scenario coverage gap | Scheduled investigation in next LEARN cycle |
| Low | Minor spec drift or documentation mismatch | Track for next LEARN review |


## Drift Detection Across Proof Tiers

The depth of drift detection scales with the proof tier:

| Proof Tier | Drift Detection Capabilities |
|-----------|----------------------------|
| P0 | None (ad hoc, no systematic detection) |
| P1 | Build-time only (CI validators, test regression) |
| P2 | Build-time + scenario regression (Scenario Bank validation) |
| P3 | Build-time + scenario regression + non-functional monitoring |
| P4 | All three levels (build-time + runtime + spec drift, closed-loop) |

P4 is the only tier with full closed-loop drift detection. If your system requires continuous validation of intent in production, P4 is the target.


## How It Relates to Other Concepts

| Concept | Relationship |
|---------|-------------|
| [Intent Contracts](intent-contracts.md) | Drift is measured against Intent Contract specifications |
| [Constitution](constitution.md) | Constitution violations are the highest-severity drift |
| [Proof Tiers](proof-tiers.md) | Proof tier determines drift detection depth |
| [Autonomy Tiers](autonomy-tiers.md) | Detected drift may trigger autonomy reduction |
| [Risk Classification](risk-classification.md) | Higher risk triggers stricter drift monitoring |
| [Scenario Banks](scenario-banks.md) | Scenario Bank is a primary baseline for drift comparison |
| [Runtime Governance](runtime-governance.md) | Trust Envelope, Escalation Contract, and State Model are runtime drift baselines |
| [Phases](phases.md) | Build-time in BUILD, runtime from SHIP onward, spec drift in LEARN |


## Practical Guidance

**Start with build-time drift detection.** If you have nothing else, add CI validators that check Constitution rules. This is the highest-value, lowest-effort starting point.

**Align monitoring to governance artifacts.** Your runtime drift detection should map directly to your Trust Envelope categories, escalation trigger conditions, and state transition rules. If you cannot monitor it, you cannot detect drift in it.

**Treat spec drift as a learning signal, not a failure.** Spec drift often means your assumptions were wrong, not that your code is broken. The correct response is usually to update the spec, not to "fix" the code to match outdated assumptions.

**Automate response to critical drift.** For Constitution violations and Trust Envelope breaches, automated responses (restricting agent authority, triggering escalation, alerting on-call) should not require human initiation. Speed matters for critical drift.

**Review drift patterns in LEARN.** Individual drift events are symptoms. Patterns across drift events reveal systemic issues. If the same type of spec drift keeps appearing, your FRAME process may need better assumption validation.


## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Alert fatigue | Too many low-severity drift alerts | Tune thresholds; aggregate related alerts |
| Detection without response | Drift detected but no one acts on it | Define response protocols per severity level |
| Build-time only | No runtime or spec drift monitoring | Add runtime monitoring for P3+; add spec drift analysis for P4 |
| Spec ossification | Treating all spec drift as bugs rather than learning opportunities | Distinguish between broken code and outdated specs |
| Manual-only detection | Relying on humans to notice drift | Automate detection at every level your proof tier supports |
