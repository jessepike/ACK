---
doc_id: "prompt-002"
slug: "pr-description"
title: "PR Description Prompt"
type: "prompt"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: []
---

# PR Description Prompt

Generate a clear, reviewable pull request description.

## Format

```markdown
## Summary
[One paragraph explaining what this PR does]

## Changes
- [Bullet list of specific changes]

## Testing
- [ ] [How to test this]

## Screenshots
[If UI changes]

## Related
- Closes #XX
- Related to #YY
```

## Rules

1. Summary should be understandable without reading code
2. Changes list is exhaustive but concise
3. Testing instructions are reproducible
4. Link all related issues

## Examples

### Feature PR
```markdown
## Summary
Adds user profile page with editable fields for name, bio, and avatar.

## Changes
- Add `/profile` route with profile form component
- Create `updateProfile` server action
- Add avatar upload to Supabase Storage
- Add form validation with Zod

## Testing
- [ ] Navigate to /profile when logged in
- [ ] Update each field and verify save
- [ ] Upload new avatar and verify display

## Related
- Closes #34
```

### Bug Fix PR
```markdown
## Summary
Fixes race condition where user could submit form twice.

## Changes
- Add loading state to disable submit button
- Add optimistic locking on server

## Testing
- [ ] Click submit rapidly - should only create one record

## Related
- Fixes #89
```

## Instructions for Claude

1. Review all changes: `git diff main...HEAD`
2. Identify the type (feature, fix, refactor, etc.)
3. Write summary explaining value/purpose
4. List all meaningful changes
5. Determine testing approach
6. Find related issues from branch name/commits

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
