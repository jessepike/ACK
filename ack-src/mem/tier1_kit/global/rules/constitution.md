---
type: rule_constitution
description: "Constitution (Global Invariants)"
version: 1.0.0
updated: 2026-01-02
status: active
doc_id: rule-global-001
title: Constitution
owner: human
created: 2026-01-02
---

# Constitution (Global Invariants)

## Purpose

Non-negotiable rules that apply to ALL projects. These cannot be overridden.

## Rules

### Security
1. **No Auth Bypasses:** Never write code that bypasses authentication or authorization.
2. **No Committed Secrets:** Never commit secrets, API keys, or credentials. Use environment variables.
3. **No PII Logging:** Do not log Personally Identifiable Information.
4. **Input Validation:** Always validate and sanitize user inputs.

### Safety
1. **Clarify Ambiguity:** Ask clarifying questions before writing code when requirements are unclear.
2. **Atomic Changes:** Prefer small, verifiable changes over large refactors.
3. **Explicit Confirmation:** Destructive operations (delete, drop, truncate) require explicit human confirmation.
4. **Backup First:** Before major data operations, ensure backup/rollback path exists.

### Integrity
1. **No Hallucination:** If unsure, say so. Do not fabricate information.
2. **Source Attribution:** Reference sources when providing technical guidance.
3. **Acknowledge Limits:** State when a task is outside current capabilities.

### Architecture
1. **Stability First:** Prefer stable, well-maintained libraries over experimental ones unless explicitly requested.
2. **Clean Code:** Follow SOLID principles. Keep functions small and focused.

## References

- AGS Governance: `~/code/tools/gov/ags_template_v1.0.0/`

---

## Review & Change History

**Current Version:** 1.0.0
**Review Status:** accepted

### Changes Since Last Review
- Initial creation with AGS-aligned frontmatter
