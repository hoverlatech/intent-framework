# Tool Integration Guide

> **INTENT Framework v0.5** | Guide
>
> INTENT is tool-agnostic. It works with any AI coding agent and any spec-driven
> development workflow. This guide explains the three-layer model, how Spec Kit
> integrates with INTENT phases, and how to configure your specific tools.

---

## The Three-Layer Model

INTENT operates across three distinct layers. Understanding them prevents confusion about what belongs where.

```
┌─────────────────────────────────────────────────┐
│  Layer 1: INTENT Framework                      │
│  (Operating Model / Governance)                 │
│  Roles, governance, autonomy scaling,           │
│  human-agent contracts                          │
├─────────────────────────────────────────────────┤
│  Layer 2: Spec-Driven Development               │
│  (Engineering Methodology)                      │
│  Spec-first workflows, generation,              │
│  validation, drift detection                    │
├─────────────────────────────────────────────────┤
│  Layer 3: Agent Tooling                         │
│  (Execution Runtime)                            │
│  Claude Code, Cursor, GitHub Copilot,           │
│  Microsoft Amplifier, OpenAI Codex              │
└─────────────────────────────────────────────────┘
```

| Layer | What It Owns | Examples |
|-------|-------------|----------|
| INTENT Framework | Team structure, roles, governance posture, autonomy budgets, contracts, scenarios | Constitution, Intent Contracts, Scenario Bank, Trust Envelope |
| Spec-Driven Development | Spec-first workflows driving generation, validation, and drift detection | GitHub Spec Kit, AWS Kiro, Tessl |
| Agent Tooling | Code generation, execution, tool-specific configuration | Claude Code, Cursor, GitHub Copilot, Microsoft Amplifier, OpenAI Codex |

**Key principle:** INTENT artifacts (contracts, constitution, scenarios) live in your project repo. Tool-specific configuration lives in tool-specific locations. The framework repo does not contain `.claude/`, `.cursorrules`, or `.github/copilot/` directories.

---

## Spec Kit Integration

INTENT's BUILD and VALIDATE phases run through Spec Kit. Here is the phase-to-command mapping.

| INTENT Phase | Spec Kit Command | Owner | Purpose |
|-------------|-----------------|-------|---------|
| Setup | `specify init` | Developer | Initialize Spec Kit in your project |
| FRAME | `/speckit.specify` | Intent Architect | Write the Intent Contract |
| EXPLORE | `/speckit.plan` | Agent (reviewed by team) | Generate implementation plan |
| BUILD | `/speckit.tasks`, `/speckit.implement` | Agent at assigned autonomy | Break down and execute work |
| VALIDATE | Scenario Bank + runtime checks | Quality Guardian | Verify outcomes match intent |
| SHIP | Standard CI/CD pipeline | Team | Deploy through existing infrastructure |
| LEARN | Monitoring feedback loop | Team + automation | Compare production to assumptions |

### How the Layers Connect

1. The **Intent Architect** writes an Intent Contract (Layer 1).
2. Spec Kit consumes the contract and drives agent execution (Layer 2).
3. The **agent tool** generates code based on the spec (Layer 3).
4. The **Quality Guardian** validates output against the Scenario Bank (Layer 1).
5. Drift detection runs at build-time and runtime (Layer 2).

The framework provides governance. Spec Kit provides workflow. The agent provides execution.

---

## The agent-instructions.md File

The `agent-instructions.md` file is the tool-agnostic source of truth for agent behavior in your project. It lives in your project repo and contains:

- Project context and architecture overview
- Constitution reference (or inline rules)
- Coding standards and conventions
- Security requirements
- Boundaries (what the agent should never do)

Every agent tool can consume this file, either natively or through tool-specific configuration that references it.

**Where to put it:** Project root or `.speckit/agent-instructions.md`.

**What goes in it vs. what goes in tool-specific config:**

| Content | Location | Reason |
|---------|----------|--------|
| Architecture principles | `agent-instructions.md` | Tool-agnostic, shared across all agents |
| Security requirements | `agent-instructions.md` | Tool-agnostic, non-negotiable |
| Coding conventions | `agent-instructions.md` | Tool-agnostic, project-level |
| Model preferences | Tool-specific config | Varies by tool |
| Key bindings, UI settings | Tool-specific config | Varies by tool |
| MCP server configuration | Tool-specific config | Varies by tool |

---

## Tool-Specific Configuration

### Claude Code

Claude Code reads instructions from `CLAUDE.md` files and the `.claude/` directory.

**Setup:**

1. Create a `CLAUDE.md` file in your project root.
2. Reference or include your `agent-instructions.md` content.
3. Add INTENT-specific instructions:

```markdown
# INTENT Framework Rules

- Read the Constitution before making changes: [path to constitution]
- Check the Scenario Bank before claiming a task is complete
- Do not modify files outside the scope defined in the Intent Contract
- Flag Constitution violations rather than working around them
```

**Configuration location:** `CLAUDE.md` (project root), `.claude/settings.json`

### Cursor

Cursor reads project rules from `.cursorrules` or `.cursor/rules/` directory.

**Setup:**

1. Create a `.cursorrules` file or add rule files to `.cursor/rules/`.
2. Reference your `agent-instructions.md` content.
3. Add INTENT governance rules.

```
# INTENT Framework Rules

Always read the Constitution before making architectural decisions.
Validate changes against the Scenario Bank before finalizing.
Report any drift from the Intent Contract constraints.
```

**Configuration location:** `.cursorrules` (project root), `.cursor/rules/`

### GitHub Copilot

GitHub Copilot reads instructions from `.github/copilot-instructions.md` and custom instructions in VS Code settings.

**Setup:**

1. Create `.github/copilot-instructions.md` in your repo.
2. Include your `agent-instructions.md` content.
3. Add INTENT-specific context about your project's governance requirements.

**Configuration location:** `.github/copilot-instructions.md`

### Other Agents (Amplifier, Codex, etc.)

The pattern is the same for any agent tool:

1. Find where the tool reads project-level instructions.
2. Reference or include your `agent-instructions.md` content.
3. Add INTENT governance rules (Constitution compliance, scenario validation, drift reporting).

---

## What Stays Outside the Framework Repo

The INTENT framework repository contains templates, documentation, and governance structures. It does not contain tool-specific configuration.

| Belongs in INTENT repo | Belongs in YOUR project repo |
|------------------------|------------------------------|
| Intent Contract template | Your project's Intent Contracts |
| Constitution starter | Your project's Constitution |
| Scenario template | Your project's Scenario Bank |
| Framework documentation | `.claude/`, `.cursorrules`, `.github/copilot-instructions.md` |
| Role definitions | `agent-instructions.md` with project-specific rules |

This separation keeps the framework tool-agnostic. You can switch from Cursor to Claude Code without changing any INTENT artifacts. Only the tool-specific configuration layer changes.

---

## Drift Detection Setup

Drift detection runs at Layer 2 (Spec-Driven Development) and feeds results back to Layer 1 (INTENT governance).

### Build-Time Detection (CI)

Add these checks to your CI pipeline:

1. **Constitution compliance:** Verify new code does not violate declared architecture principles.
2. **Contract alignment:** Check that implementation matches Intent Contract constraints.
3. **Scenario coverage:** Ensure every open Intent Contract has associated scenarios.

### Runtime Detection (Production)

For projects with live agent surfaces:

1. **Trust envelope monitoring:** Alert when agent behavior exceeds declared boundaries.
2. **State model validation:** Log interaction state transitions that do not match the model.
3. **Escalation tracking:** Measure escalation rates against expected baselines.

### Spec-Level Detection (Pre-Merge)

During the VALIDATE phase:

1. **Scenario pass evidence:** All scenarios for the relevant contract must pass.
2. **Risk-tier review:** High-risk changes require human sign-off, not just automated checks.
3. **Constitution diff:** Flag any changes to Constitution-protected areas for explicit review.

---

## Related Docs

- [Quickstart Guide](./quickstart.md)
- [Roles & Team Models](../reference/roles.md)
- [30/60/90 Rollout Plan](../reference/rollout-30-60-90.md)
