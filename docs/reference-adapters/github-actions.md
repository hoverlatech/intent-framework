# Reference Adapter: GitHub Actions

> **INTENT Framework v0.5** | Reference Adapter
>
> The GitHub Actions workflow at [`.github/workflows/intent-contract-check.yml`](../../.github/workflows/intent-contract-check.yml) is **one** implementation of the portable validator at [`tools/validate-intent-contract.py`](../../tools/validate-intent-contract.py). The validator is the contract; this workflow is just a thin shell around it. Teams on other CI systems can adapt the same pattern in a few lines.

---

## What it does

On every pull request that touches an `intent-contract*.yaml` file, the schema, or the validator itself:

1. Checks out the repo with full history.
2. Installs Python 3.11 and the validator's two dependencies (`pyyaml`, `jsonschema`).
3. Diffs against the PR base branch to find the contract files that changed.
4. Runs `tools/validate-intent-contract.py` over those files.
5. Fails the job if any file fails schema validation or any cross-field rule (tier logic, scenario coverage, runtime governance gating).

If a PR changes no contracts, the job exits cleanly with a "nothing to do" message. The check is therefore safe to mark as **required** in branch protection.

## How to copy it

1. Copy the validator and schema into your repo:
   - `tools/validate-intent-contract.py`
   - `schemas/intent-contract.schema.yaml`
2. Copy `.github/workflows/intent-contract-check.yml` into your repo at the same path.
3. Make sure your contract files are named `intent-contract*.yaml` (or update the `paths:` and `grep` patterns to match your convention).
4. In **Settings → Branches → Branch protection rules**, mark **Intent Contract Check** as a required status check.

That is the entire setup. The workflow has no secrets, no caching, and no external services.

## How to adapt it for other CI systems

The validator is intentionally CI-agnostic. Any system that can run Python and `git diff` can host the same check.

### GitLab CI

```yaml
intent-contract-check:
  image: python:3.11
  script:
    - pip install pyyaml jsonschema
    - git fetch origin "$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - CHANGED=$(git diff --name-only --diff-filter=AM
        "origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...HEAD"
        | grep -E '(^|/)intent-contract.*\.ya?ml$' || true)
    - if [ -n "$CHANGED" ]; then
        echo "$CHANGED" | xargs python tools/validate-intent-contract.py;
      fi
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### CircleCI

A single job that runs `pip install pyyaml jsonschema` and the same `git diff | xargs python tools/validate-intent-contract.py` shell command. CircleCI has no built-in PR base concept, so use the `CIRCLE_PR_BASE_BRANCH` environment variable or hardcode `main`.

### Jenkins

A `sh` step inside a multibranch pipeline. Use `git diff origin/${env.CHANGE_TARGET}...HEAD` to discover changed files and pipe them to the validator.

### Pre-commit hook

Install [`pre-commit`](https://pre-commit.com/) and add a local hook that runs the validator on staged contract files. This catches violations before a PR is even opened, but does not replace the CI gate — pre-commit hooks can be bypassed with `--no-verify`.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: intent-contract-validator
        name: Validate Intent Contracts
        entry: python tools/validate-intent-contract.py
        language: system
        files: '(^|/)intent-contract.*\.ya?ml$'
        pass_filenames: true
```

## Why the validator and the adapter are separate

The validator's portability is a deliberate design choice. CI systems come and go, and many teams use more than one. By keeping all the validation logic in a single Python file with two dependencies, INTENT lets the same rules run from a developer's laptop, a pre-commit hook, a PR check, and a nightly drift sweep without re-implementing anything.

If you build an adapter for a CI system that is not listed here, contributions back to the framework are welcome.
