# INTENT Framework — Tools

Portable utilities for enforcing INTENT artifacts in any repository or CI system.

## `validate-intent-contract.py`

A single-file, framework-independent validator for Intent Contract YAML files. Copy it into any repo alongside `schemas/intent-contract.schema.yaml` and run it from a hook, a make target, or any CI system.

### Install

```bash
pip install pyyaml jsonschema
```

### Usage

```bash
python tools/validate-intent-contract.py path/to/intent-contract.yaml [more.yaml ...]
# Override the schema path:
python tools/validate-intent-contract.py --schema other/schema.yaml contract.yaml
```

Exit code `0` means every file passed. Exit code `1` means at least one file failed; all errors are printed before exit.

### Checks performed

| # | Check | Framework concept |
|---|---|---|
| 1 | **Schema validation** — required fields, types, enums | Source of truth: `templates/intent-contract-template.md` |
| 2 | **Tier logic — autonomy bounds** — `risk=High` allows only `A0/A1`; `risk=Medium` allows only `A0/A1/A2` | [Risk Classification](../docs/concepts/risk-classification.md), [Autonomy Tiers](../docs/concepts/autonomy-tiers.md) |
| 3 | **Tier logic — minimum proof** — `High≥P3`, `Medium≥P2`, `Low≥P1` | [Proof Tiers](../docs/concepts/proof-tiers.md) |
| 4 | **Scenario coverage** — at least 3 scenarios; at least one with `type: failure` | [Scenario Banks](../docs/concepts/scenario-banks.md) |
| 5 | **Runtime governance gating** — if `runtime_governance.required: Yes`, at least one of `trust_envelope_version` / `escalation_contract_version` / `interaction_state_model_version` must be a non-`N/A` value | [Runtime Governance](../docs/concepts/runtime-governance.md) |

Checks 1 and the schema piece of 2 come from JSON Schema. Checks 2–5 are enforced as cross-field rules in the script because JSON Schema cannot express them cleanly.

### Wiring into CI

The validator is intentionally CI-agnostic. A reference GitHub Actions adapter is provided at `.github/workflows/intent-contract-check.yml`. To adapt it to GitLab CI, CircleCI, Jenkins, or a pre-commit hook, the only requirements are:

1. A Python 3 environment with `pyyaml` and `jsonschema` installed.
2. A way to discover changed `intent-contract*.yaml` files (e.g. `git diff --name-only`).
3. Pipe those paths to the validator and fail the job on a non-zero exit.

See [`docs/reference-adapters/github-actions.md`](../docs/reference-adapters/github-actions.md) for the worked example.
