---
doc_id: "gov-090"
slug: "ci-example-github-actions"
title: "CI Example: GitHub Actions"
type: "runbook"
tier: "tier2"
authority: "guidance"
status: "draft"
version: "0.1.0"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
review_status: "draft"
depends_on: ["gov-001"]
---

## GitHub Actions (example)

Create `.github/workflows/ags-validate.yml`:

```yaml
name: AGS Validate
on:
  pull_request:
  push:
    branches: [ main ]
jobs:
  ags:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml
      - run: python3 scripts/validate_ags.py --profile strict --check-registry --check-drift
```

Notes:
- Keep this advisory until you standardize CI across repos.
