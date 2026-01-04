---
type: release_notes
description: "Round3 Update Notes"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: gov-052
slug: round3-update-notes
title: "Round 3 Update Notes"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

## Purpose

Capture what changed based on Round 2 feedback (secondary review).

## Changes

1. Added **validation profiles**:
   - `--profile strict` (default): requires full schema
   - `--profile minimal`: requires core keys only; fills defaults for optional keys

2. Added **ID allocator helper**:
   - `--next-id <prefix>` prints next available ID, e.g. `gov-012`.

3. Added **git-derived change report**:
   - `--change-report` writes `artifacts/CHANGE_REPORT.md`.

4. Clarified: manual “Review & Change History” sections are optional and candidates for removal once change report or git log usage is standardized.
