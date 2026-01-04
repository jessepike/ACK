---
doc_id: "review-mem-synthesis-001"
title: "Tier-1 Kit Review Synthesis"
type: "research_note"
status: "active"
version: "1.0.0"
owner: "human"
created: "2026-01-02"
updated: "2026-01-02"
---

# Tier-1 Memory Kit Review Synthesis

**Reviews:** Gemini, ChatGPT  
**Date:** 2026-01-02  
**Verdict:** Has Potential But Flawed (unanimous)

---

## Critical Issues (Both Agree)

### 1. Frontmatter Over-Engineering

**Problem:** Schema duplicates Git functionality, creates maintenance burden.

**Flagged fields to remove:**
- `version` — Git hash is better
- `created` — Git history handles this
- `updated` — Git history (won't drift)
- `owner` — Git blame handles this
- `status` — Git branches (draft = branch, active = main)
- `doc_id` — Filename is sufficient
- `review_status` — "Merged to main" = accepted

**Keep:**
- `title` — Human-readable
- `type` — Categorization (constitution vs preference)
- `paths` — Conditional loading (when implemented)

**Action:** Dramatically simplify required frontmatter.

---

### 2. Conflict Resolution Undefined

**Problem:** No policy for when rules conflict across levels.

**Example:** Global `preferences.md` says "use Python" but Project `stack.md` says "this is Node.js repo."

**Current spec implies:** Global > Project priority — which is WRONG for preferences.

**Proposed fix:**
- **Constitution (Global):** NEVER override — hard invariants
- **Preferences (Global):** Project CAN override — soft defaults
- Add explicit override mechanism or priority field

**Action:** Define two classes of global rules (Strong/Weak) with explicit override semantics.

---

### 3. Token Budget Math Doesn't Add Up

**Problem:** Spec says ~20k target but components sum to ~8k.

**What spec says:**
- Global: ~2,000 tokens
- Project: ~5,000 tokens
- Local: ~1,000 tokens
- **Total: ~8,000** (not 20k)

**Additional concern:** If rules/*.md all auto-load and a project has many rule files, budget explodes silently.

**Action:** 
- Clarify what the remaining ~12k is for (conversation? file reads?)
- Add token measurement tooling
- Define overflow handling

---

### 4. "Agent via hooks" is Magic

**Problem:** Spec claims agents update CLAUDE.md "via hooks" but defines no such hooks.

**Reality:** This requires external MCP server or custom scripts — not native Claude Code.

**Action:** Either:
- Remove the claim, OR
- Explicitly define the hook mechanism required

---

### 5. No Enforcement Mechanisms

**Problem:** Governance rules exist but nothing enforces them.

**Concerns:**
- Line limits (200) — no validator
- Token budgets — no measurement
- Frontmatter — no linter
- Version increments — honor system

**Action:** Define validation tooling (extend `validate_ags.py` or new script).

---

### 6. Global Sync Strategy Missing

**Problem:** `~/.claude` is "global" only to one machine.

**Use cases unaddressed:**
- Multiple machines (laptop + desktop)
- Team-shared global standards
- Backup/recovery

**Action:** Recommend dotfiles approach (private Git repo for `~/.claude`).

---

## Important Issues (One or Both Flag)

### 7. Load Order Needs Verification

**Problem:** Spec claims "official" load order but provides no citation or test plan.

**Risk:** If Claude Code changes behavior, entire priority model breaks.

**Action:** Add verification test and Claude Code version compatibility note.

---

### 8. Line Limit is Arbitrary

**Problem:** "200 lines hard ceiling" forces awkward file splits.

**Suggestion:** Change to soft target (200) with hard warning (500).

**Action:** Relax to guideline, not hard rule.

---

### 9. "Changes Since Last Review" is Lossy

**Problem:** Section gets cleared after each review — loses history.

**Alternative:** Git commit history IS the change history.

**Action:** Consider removing this section entirely if frontmatter is simplified.

---

### 10. Project CLAUDE.md Policy Inconsistent

**Problem:** Spec says "agent can update CLAUDE.md, no approval needed" but also "project rules must commit to git."

**Conflict:** Is CLAUDE.md exempt from review? If so, audit trail breaks.

**Action:** Clarify: either all project memory requires PR, or explain auditability for auto-updates.

---

## Recommendations by Priority

### Must Fix (Blockers)

| Issue | Fix |
|-------|-----|
| Frontmatter bloat | Reduce to: `title`, `type`, `paths` (optional) |
| Conflict resolution | Define Strong (constitution) vs Weak (preferences) override rules |
| "Agent via hooks" | Remove claim or define mechanism |

### Should Fix (Important)

| Issue | Fix |
|-------|-----|
| Token budget math | Clarify total and add measurement tooling |
| Global sync | Add dotfiles recommendation |
| Load order | Add verification test and version note |
| Enforcement | Define validation script requirements |

### Could Fix (Nice to Have)

| Issue | Fix |
|-------|-----|
| Line limit | Soften to guideline |
| Review section | Consider removal if using Git-only tracking |
| Priority field | Add optional `priority: critical|normal` |

---

## Revised Frontmatter Schema

**Minimal (recommended):**
```yaml
---
title: "Constitution"
type: "rule_constitution"
---
```

**Extended (when needed):**
```yaml
---
title: "API Rules"
type: "rule_stack"
paths: "src/api/**/*.ts"
priority: "critical"
---
```

**Rationale:** Git provides `created`, `updated`, `owner`, version history. Don't duplicate.

---

## Revised Override Model

```
┌─────────────────────────────────────────────────────────┐
│ Global Constitution (rule_constitution)                 │
│ NEVER OVERRIDABLE — Hard invariants                     │
│ Examples: No auth bypass, no committed secrets          │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Cannot override
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Global Preferences (rule_preferences, rule_workflow)    │
│ PROJECT CAN OVERRIDE — Soft defaults                    │
│ Examples: "Prefer Python" → Project says "Use Node"     │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Overrides
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Project Rules (rule_architecture, rule_stack, etc.)     │
│ Specific to this repo                                   │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Overrides
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Local (CLAUDE.local.md)                                 │
│ Personal, ephemeral, not tracked                        │
└─────────────────────────────────────────────────────────┘
```

---

## Questions to Resolve

1. **Do we keep ANY frontmatter beyond title/type?** Or go pure Git-based?
2. **How strict on Constitution vs Preferences?** Explicit tag, or just convention?
3. **Validation tooling:** Extend AGS validate script, or new dedicated tool?
4. **Agent CLAUDE.md updates:** Allow with auto-commit, or require human approval?

---

## Next Steps

1. **Decide** on frontmatter simplification level
2. **Update** TIER1_KIT_SPEC.md with fixes
3. **Optionally** re-run review on v2
4. **Implement** validation tooling

---

## Review & Change History

**Current Version:** 1.0.0
**Review Status:** accepted

### Changes Since Last Review
- Initial synthesis from Gemini and ChatGPT reviews
