# INTENT Framework

A governance operating model for AI-native product development.

INTENT provides the missing governance layer for teams where AI agents do the execution. It defines how decisions get made, what evidence is required, how much autonomy agents receive, and how live AI systems stay within bounds. INTENT sits above your engineering methodology and above your agent tooling.

## The Three-Layer Model

INTENT operates as the top layer in a three-layer stack:

| Layer | Purpose | Examples |
|-------|---------|----------|
| **Operating Model** (INTENT) | Governance, roles, autonomy scaling, human-agent contracts | Constitution, Intent Contracts, Proof Tiers |
| **Engineering Methodology** | Spec-first workflows driving generation, validation, drift detection | GitHub Spec Kit, AWS Kiro, Tessl |
| **Execution Runtime** | Agent tooling that does the work, bounded by governance constraints | Claude Code, Cursor, GitHub Copilot, Codex |

INTENT is tool-agnostic. It composes with any spec-driven methodology and any AI coding tool. The governance layer defines the rules. The engineering layer enforces them. The execution layer operates within them.

## Core Concepts

### Constitution

The supreme governing document for a project. It defines non-negotiable principles across architecture, security, reliability, testing, and agent boundaries. Every AI agent interaction must comply. Changes require a formal amendment process.

See [docs/concepts/constitution.md](docs/concepts/constitution.md) | Template: [templates/constitution-starter.md](templates/constitution-starter.md)

### Intent Contracts

Intent Contracts replace user stories with outcome-centric specifications. Each contract captures the problem, desired outcomes, constraints, non-goals, scenarios, and a proof plan that assigns risk, proof, and autonomy tiers. They define *what* and *why*, not *how*.

See [docs/concepts/intent-contracts.md](docs/concepts/intent-contracts.md) | Template: [templates/intent-contract-template.md](templates/intent-contract-template.md)

### Proof Tiers

Proof tiers define how much evidence is required before a change ships. Higher risk demands higher proof.

| Tier | Name | What It Means |
|------|------|---------------|
| P0 | Ad hoc | Informal checks only. No structured evidence. |
| P1 | Repeatable | Basic automated checks plus manual walkthrough. |
| P2 | Scenario-backed | Scenario Bank pass evidence required. |
| P3 | Risk-calibrated | P2 plus load, security, and failure-mode verification. |
| P4 | Closed-loop | P3 plus production telemetry validates intent continuously. |

The **Spec Continuum** describes how the relationship between specs and code evolves:
- **P0-P1 (Spec-guided):** Code is the source of truth. Specs guide but do not govern.
- **P2-P3 (Spec-anchored):** Specs and code co-evolve. Drift detection enforces alignment.
- **P4 (Spec-as-source):** Specs govern. Code is generated output.

See [docs/concepts/proof-tiers.md](docs/concepts/proof-tiers.md)

### Autonomy Tiers

Autonomy tiers define how much freedom AI agents have during BUILD and what role humans play.

| Tier | Name | Agent Authority | Human Role |
|------|------|----------------|------------|
| A0 | Suggest | Proposes; humans execute | Decision-maker |
| A1 | Draft | Drafts; humans edit | Author/editor |
| A2 | Implement | Implements; humans review before merge | Reviewer |
| A3 | Operate | Executes with exception-focused review | Auditor |
| A4 | Execute | Merges and deploys under strict gates | Monitor |

**P1 x A2** is the most common pairing: agents implement, humans review, with basic automated checks as the proof floor.

See [docs/concepts/autonomy-tiers.md](docs/concepts/autonomy-tiers.md)

### Phases

INTENT uses a continuous, proof-gated flow rather than time-boxed sprints:

**FRAME** > **EXPLORE** > **BUILD** > **VALIDATE** > **SHIP** > **LEARN**

| Phase | Purpose | Key Output |
|-------|---------|------------|
| FRAME | Define outcomes, constraints, proof expectations | Intent Contract |
| EXPLORE | Investigate approaches, plan implementation | Implementation Plan |
| BUILD | Execute the plan under governance constraints | Working code + proof artifacts |
| VALIDATE | Verify behavior against Scenario Bank and constitution | Proof Report |
| SHIP | Release through standard CI/CD | Production deployment |
| LEARN | Compare production telemetry against intent assumptions | Updated scenarios, recalibrated tiers |

An optional **DISCOVER** phase precedes FRAME for research and problem validation.

See [docs/concepts/phases.md](docs/concepts/phases.md)

### Risk Classification

Every change is classified as High, Medium, or Low risk. Risk tier determines minimum proof and maximum autonomy.

| Risk Tier | Criteria | Minimum Proof | Maximum Autonomy |
|-----------|----------|---------------|------------------|
| High | Auth, payments, PII, infrastructure, safety | P3 | A0-A1 |
| Medium | User-facing features, API changes, schema updates | P2 | A2 |
| Low | Content, styling, docs, internal tooling | P1 | A3-A4 |

See [docs/concepts/risk-classification.md](docs/concepts/risk-classification.md)

### Drift Detection

INTENT detects drift at three levels:

1. **Build-time:** CI validators check spec conformance. Violations block deployment.
2. **Runtime:** Production behavior is continuously validated against Trust Envelope, escalation paths, and state rules. Deviations trigger alerts.
3. **Spec drift:** Actual telemetry is compared against Intent Contract assumptions. Divergence triggers a LEARN phase review.

See [docs/concepts/drift-detection.md](docs/concepts/drift-detection.md)

### Scenario Banks

The Scenario Bank is the holdout set used during VALIDATE to prove behavior aligns with intent. Each scenario captures preconditions, steps, expected outcomes, failure modes, and runtime signals. Scenarios accumulate over time as the project matures, with new scenarios added from production incidents and edge cases discovered during LEARN.

See [docs/concepts/scenario-banks.md](docs/concepts/scenario-banks.md) | Template: [templates/scenarios-template.yaml](templates/scenarios-template.yaml)

### Runtime Governance

For systems where AI operates live (customer-facing agents, autonomous workflows, safety-critical surfaces), INTENT adds three runtime artifacts that form a governance stack:

**Constitution** (non-negotiables) > **Trust Envelope** > **Escalation Contract** > **Interaction State Model**

| Artifact | Purpose |
|----------|---------|
| **Trust Envelope** | Defines the positive boundary: what the agent is authorized to output or do. Categorizes outputs with confidence levels (scripted, templated, generated) and violation severity. |
| **Escalation Contract** | Maps every path from agent-handled interaction to human involvement. Defines escalation classes (E0 through E2, plus user-requested), protocols, timeouts, and fallbacks. |
| **Interaction State Model** | Defines valid runtime states, transitions, and per-state permissions. Each state specifies which Trust Envelope categories are active and what data is required before exit. |

Runtime governance is required when the system's live outputs or actions can affect users, operations, compliance, safety, or business outcomes without guaranteed human review.

See [docs/concepts/runtime-governance.md](docs/concepts/runtime-governance.md) | Templates: [templates/trust-envelope-template.md](templates/trust-envelope-template.md), [templates/escalation-contract-template.md](templates/escalation-contract-template.md), [templates/interaction-state-model-template.md](templates/interaction-state-model-template.md)

## Roles

INTENT defines four roles. On small teams, one person may fill multiple roles.

| Role | Owns |
|------|------|
| **Intent Architect** | Outcomes, constraints, proof plan. Writes Intent Contracts, sets risk and proof tiers. |
| **Systems Conductor** | Architecture, reliability, context layers. Maintains the Constitution and technical guardrails. |
| **Experience Shaper** | Interaction quality and usability evidence. Owns Trust Envelopes and user-facing behavior. |
| **Quality Guardian** | Scenario health, risk tiers, autonomy policy. Runs validation and calibrates governance. |

Three team models: **Solo Director** (one person, all roles), **Thin Team** (2-4 people, 1-2 roles each), **Swarm** (larger teams with shared roles).

See [docs/reference/roles.md](docs/reference/roles.md)

## Getting Started

The fastest path to using INTENT:

1. Read the [Quickstart Guide](docs/guides/quickstart.md)
2. Copy the [templates](templates/) into your project
3. Write your first [Constitution](templates/constitution-starter.md) and [Intent Contract](templates/intent-contract-template.md)
4. Review the [worked example](examples/sample-project/) to see how all the pieces fit together

For a gradual adoption path, see the [30/60/90 Rollout Plan](docs/reference/rollout-30-60-90.md).

## Spec Kit Integration

INTENT's BUILD and VALIDATE phases run through [GitHub Spec Kit](https://github.com/github/spec-kit), a spec-driven development tool that transforms specifications into working code.

| Phase | Spec Kit Command | INTENT Role |
|-------|-----------------|-------------|
| Frame | `/speckit.specify` | Intent Architect |
| Explore | `/speckit.plan` | Agent (reviewed) |
| Build | `/speckit.tasks`, `/speckit.implement` | Agent at assigned autonomy |
| Validate | Scenario Bank + runtime checks | Quality Guardian |

See [docs/guides/tool-integration.md](docs/guides/tool-integration.md) for details on using INTENT with Spec Kit, Claude Code, Cursor, and other tools.

## Repo Structure

```
intent-framework/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── docs/
│   ├── concepts/          # Core framework concepts
│   │   ├── intent-contracts.md
│   │   ├── constitution.md
│   │   ├── proof-tiers.md
│   │   ├── autonomy-tiers.md
│   │   ├── phases.md
│   │   ├── risk-classification.md
│   │   ├── drift-detection.md
│   │   ├── scenario-banks.md
│   │   └── runtime-governance.md
│   ├── guides/            # How-to guides
│   │   ├── quickstart.md
│   │   └── tool-integration.md
│   └── reference/         # Reference material
│       ├── roles.md
│       ├── intent-vs-scrum.md
│       └── rollout-30-60-90.md
├── templates/             # Ready-to-use templates
│   ├── intent-contract-template.md
│   ├── constitution-starter.md
│   ├── scenarios-template.yaml
│   ├── plan-template-intent.md
│   ├── tasks-template-intent.md
│   ├── trust-envelope-template.md
│   ├── escalation-contract-template.md
│   └── interaction-state-model-template.md
└── examples/              # Worked example
    └── sample-project/    # "DocSearch" - AI-powered doc search
        ├── constitution.md
        ├── intent-contract.md
        ├── scenarios.yaml
        ├── trust-envelope.md
        ├── escalation-contract.md
        ├── interaction-state-model.md
        └── plan.md
```

## Background

INTENT was developed by Nick Polyan at [Hoverla Tech](https://hoverlatech.com) as an implementable framework for evidence-driven delivery when AI does the execution. It addresses the governance gap that emerges when agent-generated code outpaces traditional review and QA processes. The framework is used on real projects and continues to evolve based on production experience.

## Influences

INTENT was shaped by ideas from Dan Shapiro's Five Levels maturity model, StrongDM's Software Factory principles, Nate B. Jones's work on specification bottlenecks and intent-driven writing, and GitHub's Spec Kit methodology. The framework builds on these foundations while adding organizational governance, proof tiers, and autonomy scaling.

## Acknowledgments

Built with AI-assisted development using Claude Code.

## License

MIT. See [LICENSE](LICENSE).
