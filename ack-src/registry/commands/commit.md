---
type: command
description: "Commit Command"
version: 0.1.0
updated: 2026-01-01
status: review
depends_on: "["prompt-001"]"
doc_id: cmd-004
slug: commit
title: "Commit Command"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
triggers: 
notes: "May overlap with Claude Code built-in. Pending review."
---

# Commit Command

Generate a conventional commit message for staged changes.

## Workflow

1. Check staged changes exist
2. Analyze diff
3. Apply commit-message prompt template
4. Output formatted message
5. Optionally execute commit

## Execution

```bash
# Step 1: Verify staged changes
git diff --staged --stat

# Step 2: Get detailed diff
git diff --staged
```

## Apply Prompt

Reference: `prompts/commit-message.md`

Analyze the diff and generate message following:
- Conventional Commits format
- Imperative mood
- ≤50 char subject line

## Output Format

```
<type>(<scope>): <subject>

<body if needed>

<footer if needed>
```

Then ask: "Ready to commit with this message? (y/n)"

If yes:
```bash
git commit -m "<generated message>"
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
- Marked for review: may overlap with Claude Code built-in
