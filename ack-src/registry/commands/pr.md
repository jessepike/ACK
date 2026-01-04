---
type: command
description: "PR Command"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: "["prompt-002"]"
doc_id: cmd-005
slug: pr
title: "PR Command"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
triggers: 
---

# PR Command

Generate a pull request description for current branch.

## Workflow

1. Get branch info and commits
2. Analyze all changes vs main
3. Apply pr-description prompt template
4. Output formatted PR description

## Execution

```bash
git branch --show-current
git log main..HEAD --oneline
git diff main...HEAD --stat
```

## Apply Prompt

Reference: `prompts/pr-description.md`

## Output Format

```markdown
## Summary
[Generated summary]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] [Test step 1]

## Related
- Closes #XX
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
