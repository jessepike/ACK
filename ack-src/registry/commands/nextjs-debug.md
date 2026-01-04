---
type: command
description: "Next.js Debug Command"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: "["agent-003", "skill-003", "tool-003"]"
doc_id: cmd-003
slug: nextjs-debug
title: "Next.js Debug Command"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
triggers: 
---

# Next.js Debug Command

Diagnose and fix Next.js App Router issues.

## Workflow

1. **Identify** error type (build, hydration, runtime, routing)
2. **Run** build to surface all errors
3. **Analyze** error messages and component structure
4. **Fix** with correct Server/Client patterns
5. **Verify** build succeeds

## Execution Steps

### Step 1: Run Build
```bash
npm run build 2>&1 | head -100
```

### Step 2: Identify Error Type

**"useState/useEffect can only be used in Client Components"**
→ Add "use client" directive

**"Hydration failed because..."**
→ Server/client HTML mismatch. Check:
- Browser-only APIs (window, localStorage)
- Date/time differences
- Random values

**"Dynamic server usage"**
→ Add `export const dynamic = 'force-dynamic'`

**"generateStaticParams is required"**
→ Add static params function

### Step 3: Common Fixes

**Client Component needed:**
```typescript
"use client"
import { useState } from 'react'
```

**Hydration fix:**
```typescript
"use client"
import { useState, useEffect } from 'react'

export function BrowserOnly() {
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  if (!mounted) return null
  return <div>{window.location.href}</div>
}
```

### Step 4: Verify
```bash
npm run build
npm run dev  # Check console for hydration warnings
```

## Output Format

```markdown
## Next.js Debug Report

**Error Type:** {Build|Hydration|Runtime|Routing}
**File:** {path}

### Error Message
```
{exact error}
```

### Analysis
{why this is happening}

### Fix Applied
```typescript
{code change}
```

### Verification
{build succeeds, no console errors}
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
