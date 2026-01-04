---
doc_id: "spec-001"
slug: "tier1-markdown-schema"
title: "Tier 1 Markdown Schema"
type: "schema"
tier: "tier1"
status: "active"
authority: "binding"
version: "0.2.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["gov-011"]
---

# Tier 1 Markdown schema (exact)

Tier 1 Markdown docs are *human-first* but *machine-governed* via YAML frontmatter and a required bottom “Review & Change History” section.

Store Tier 1 docs in `/docs/*.md` (or your preferred structure).

---

## Tier 1 frontmatter (required fields)

```yaml
doc_id: "arch-001"                 # required; unique; stable
slug: "system-architecture"        # required; stable human reference
title: "System Architecture"       # required

status: "active"                   # required; draft|review|active|deprecated

version: "0.2.0"                   # required; document meaning version (semver recommended)
review_status: "reviewed"          # required; draft|reviewed|accepted

created: "2026-01-01"              # required; YYYY-MM-DD
updated: "2026-01-01"              # required; YYYY-MM-DD

owner: "human"                     # required; simple start: human|agent|team:<name>
depends_on: []                     # required; list of doc_ids this depends on (can be empty)
```

---

## Tier 1 frontmatter (optional fields)

Add these later (backlog), not day one:

```yaml
supersedes: []                     # doc_id(s) replaced by this doc
related: []                        # doc_id(s) related but not dependencies
tags: []                           # retrieval tags
change_log_ref: "adr_index"        # pointer to decision log (doc_id or slug)
```

---

## Required body structure (progressive disclosure spine)

Tier 1 docs must include these top-level headings in this order:

```markdown
## Purpose
## Scope
## Constraints
## System overview
## Key decisions (links to ADRs)
## Interfaces & dependencies
## Invariants (what must remain true)
## Open questions
```

Types may extend this with additional required sections, but Tier 1 keeps the same spine.

---

## Required bottom section (Tier 1)

Tier 1 docs must end with:

```markdown
---

## Review & Change History

**Current Version:** 0.2.0  
**Review Status:** reviewed

### Changes Since Last Review
- (none)
```

This keeps change/authority metadata out of the main narrative and supports progressive disclosure.

---

## Example: complete Tier 1 doc header

```markdown
---
doc_id: "arch-001"
slug: "system-architecture"
title: "System Architecture"
status: "active"
version: "0.2.0"
review_status: "reviewed"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["brief-001", "sec-001"]
---

## Purpose
...
```

---

## References

- Document versioning policy: `GOVERNANCE_DOCUMENT_VERSIONING.md`
