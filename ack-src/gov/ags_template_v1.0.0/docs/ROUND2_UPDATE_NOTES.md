---
type: release_notes
description: "Round2 Update Notes"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: gov-051
slug: round2-update-notes
title: "Round 2 Update Notes"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

## Purpose

Capture what changed for the **Round 2 external review** so reviewers can focus on what’s new.

---

## What changed since last review

1. **Enforcement added:** `scripts/validate_ags.py`
   - Validates frontmatter presence and required keys
   - Enforces `doc_id` uniqueness
   - Validates `depends_on` references
   - Auto-generates `artifacts/ARTIFACT_REGISTRY.json`

2. **Registry policy clarified:** Registry is now **derived**, not manually edited.

3. **Solo-dev path clarified:** governance can be run locally; PR workflow is recommended but not required for a solo dev.

4. **Backlog enriched:** added break-glass, ID allocation, metrics, agent identity.

---

## How to run

From package root:

```bash
python3 scripts/validate_ags.py --write-registry
```

Use `--strict` to treat warnings as errors (future use).

---

## Reviewer focus

- Is the enforcement script minimal but sufficient?
- Are the required frontmatter keys reasonable?
- Should the script validate additional constraints now, or later?