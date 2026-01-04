---
type: prompt
description: "Error Diagnosis Prompt"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: prompt-004
slug: error-diagnosis
title: "Error Diagnosis Prompt"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

# Error Diagnosis Prompt

Structured approach to diagnosing and resolving errors.

## Diagnosis Framework

### 1. Capture
```
Error Type: [Runtime | Build | Type | Network | Auth | Database]
Error Message: [Exact message]
Stack Trace: [First 10 lines]
Context: [What user was doing]
Reproducible: [Always | Sometimes | Once]
```

### 2. Categorize

| Error Pattern | Likely Cause | First Check |
|---------------|--------------|-------------|
| `undefined is not a function` | Wrong import, typo | Import statements |
| `Cannot read property of null` | Missing null check | Data flow |
| `ECONNREFUSED` | Service down | Service status |
| `401 Unauthorized` | Auth token issue | Token validity |
| `403 Forbidden` | Permission issue | RLS/RBAC policies |
| `404 Not Found` | Wrong URL/route | Route definition |
| `500 Internal Server Error` | Server crash | Server logs |
| `Hydration mismatch` | Server/client diff | Dynamic content |

### 3. Isolate

1. **Reproduce** — Can you trigger it consistently?
2. **Minimize** — What's the smallest code that fails?
3. **Bisect** — When did it start? (`git bisect`)
4. **Compare** — Does it work in other environments?

### 4. Hypothesize

Form 2-3 hypotheses ranked by likelihood:
```
H1 (70%): [Most likely cause]
H2 (20%): [Second possibility]
H3 (10%): [Long shot]
```

### 5. Test

For each hypothesis:
```
Test: [What to check]
Expected if true: [What you'd see]
Actual: [What you saw]
Result: [Confirmed | Ruled out]
```

### 6. Fix

```
Root Cause: [What actually caused it]
Fix: [What was changed]
Verification: [How you confirmed it's fixed]
Prevention: [How to prevent recurrence]
```

## Output Format

```markdown
## Error Diagnosis

**Error:** [Brief description]
**Type:** [Category]

### Symptoms
[What's happening]

### Investigation
1. [Step taken] → [Finding]
2. [Step taken] → [Finding]

### Root Cause
[Explanation of why this happened]

### Fix
```[language]
[Code change]
```

### Verification
[How fix was confirmed]
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
