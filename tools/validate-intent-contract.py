#!/usr/bin/env python3
# INTENT Framework v0.5 — portable Intent Contract validator.
# Copy this into any repo. No framework-specific runtime dependencies.
#
# Usage:
#   python validate-intent-contract.py path/to/intent-contract.yaml [more.yaml ...]
#
# Dependencies:
#   pip install pyyaml jsonschema
#
# Behavior:
#   - Loads schemas/intent-contract.schema.yaml relative to this script
#     (override with --schema PATH).
#   - Validates each input file against the schema.
#   - Enforces additional cross-field rules that JSON Schema cannot express:
#       1. Tier logic: risk tier bounds proof tier and autonomy tier.
#       2. Scenario coverage: >=3 scenarios, >=1 of type 'failure'.
#       3. Runtime governance gating: if required, at least one runtime
#          artifact version must be a real (non-N/A) value.
#   - Exit 0 on full pass, 1 on any failure. All errors for all files
#     are printed before exit so CI surfaces every problem at once.

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, List, Tuple

try:
    import yaml
except ImportError:
    sys.stderr.write("error: pyyaml is required (pip install pyyaml)\n")
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    sys.stderr.write("error: jsonschema is required (pip install jsonschema)\n")
    sys.exit(2)


# Tier ordering for the risk -> minimum proof rule.
PROOF_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}

# Risk tier rules. Mirrors docs/concepts/risk-classification.md.
MAX_AUTONOMY_BY_RISK = {
    "High": {"A0", "A1"},
    "Medium": {"A0", "A1", "A2"},
    "Low": {"A0", "A1", "A2", "A3", "A4"},
}
MIN_PROOF_BY_RISK = {"High": "P3", "Medium": "P2", "Low": "P1"}


def load_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def schema_errors(contract: Any, schema: Any) -> List[str]:
    validator = jsonschema.Draft202012Validator(schema)
    out = []
    for err in sorted(validator.iter_errors(contract), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        out.append(f"schema: {loc}: {err.message}")
    return out


def cross_field_errors(contract: Any) -> List[str]:
    """Rules JSON Schema cannot express cleanly."""
    errs: List[str] = []
    if not isinstance(contract, dict):
        return ["root: contract must be a mapping"]

    # Rule 1: tier logic.
    proof = contract.get("proof_plan") or {}
    risk = proof.get("risk_tier")
    autonomy = proof.get("autonomy_tier")
    proof_tier = proof.get("proof_tier")

    if risk in MAX_AUTONOMY_BY_RISK and autonomy:
        allowed = MAX_AUTONOMY_BY_RISK[risk]
        if autonomy not in allowed:
            errs.append(
                f"tier: risk_tier={risk} forbids autonomy_tier={autonomy} "
                f"(allowed: {sorted(allowed)})"
            )

    if risk in MIN_PROOF_BY_RISK and proof_tier in PROOF_ORDER:
        min_required = MIN_PROOF_BY_RISK[risk]
        if PROOF_ORDER[proof_tier] < PROOF_ORDER[min_required]:
            errs.append(
                f"tier: risk_tier={risk} requires proof_tier>={min_required}, "
                f"got {proof_tier}"
            )

    # Rule 2: scenario coverage.
    scenarios = contract.get("scenarios") or []
    if isinstance(scenarios, list):
        if len(scenarios) < 3:
            errs.append(f"scenarios: need at least 3, got {len(scenarios)}")
        if not any(isinstance(s, dict) and s.get("type") == "failure" for s in scenarios):
            errs.append("scenarios: at least one scenario must have type='failure'")

    # Rule 3: runtime governance gating.
    rg = contract.get("runtime_governance") or {}
    if rg.get("required") == "Yes":
        version_fields = (
            "trust_envelope_version",
            "escalation_contract_version",
            "interaction_state_model_version",
        )
        present = [
            f for f in version_fields
            if rg.get(f) and str(rg.get(f)).strip().upper() != "N/A"
        ]
        if not present:
            errs.append(
                "runtime_governance: required=Yes but no runtime artifact "
                "version is set (need at least one of "
                "trust_envelope_version / escalation_contract_version / "
                "interaction_state_model_version)"
            )

    return errs


def validate_file(path: str, schema: Any) -> Tuple[bool, List[str]]:
    try:
        contract = load_yaml(path)
    except Exception as exc:
        return False, [f"parse: {exc}"]
    errs = schema_errors(contract, schema) + cross_field_errors(contract)
    return (not errs), errs


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    default_schema = os.path.normpath(
        os.path.join(here, "..", "schemas", "intent-contract.schema.yaml")
    )

    ap = argparse.ArgumentParser(description="Validate INTENT Intent Contract YAML files.")
    ap.add_argument("files", nargs="+", help="One or more contract YAML files.")
    ap.add_argument("--schema", default=default_schema,
                    help=f"Path to schema file (default: {default_schema})")
    args = ap.parse_args()

    try:
        schema = load_yaml(args.schema)
    except FileNotFoundError:
        sys.stderr.write(f"error: schema not found at {args.schema}\n")
        return 2

    overall_ok = True
    for path in args.files:
        ok, errs = validate_file(path, schema)
        if ok:
            print(f"PASS  {path}")
        else:
            overall_ok = False
            print(f"FAIL  {path}")
            for e in errs:
                print(f"  - {e}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
