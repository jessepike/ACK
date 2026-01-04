---
doc_id: "cmd-007"
slug: "review"
title: "Review Command"
type: "command"
tier: "tier2"
status: "deprecated"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["prompt-003"]
triggers:
  - /review
deprecation_note: "DEPRECATED - Use built-in /review command instead. Claude Code has native code review."
---

# Review Command (DEPRECATED)

> **Note:** This command is deprecated. Use the built-in `/review` command instead.
> Claude Code has native code review functionality.

This command was originally created to perform systematic code review.
The built-in `/review` command provides this functionality natively.

## Migration

Instead of using this custom command, use:
```
/review
```

The prompt template in `prompts/code-review.md` can still be referenced
for manual review guidance if needed.

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
- Marked deprecated: overlaps with Claude Code built-in /review
