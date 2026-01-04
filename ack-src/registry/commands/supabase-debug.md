---
doc_id: "cmd-002"
slug: "supabase-debug"
title: "Supabase Debug Command"
type: "command"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["agent-002", "skill-002", "tool-002"]
triggers:
  - /supabase-debug
  - supabase query failing
  - supabase auth not working
  - RLS blocking
  - permission denied supabase
---

# Supabase Debug Command

Diagnose and fix Supabase database, auth, and RLS issues.

## Workflow

1. **Identify** failure type (RLS, auth, query, Edge Function)
2. **Gather** schema and policy information via MCP
3. **Test** with service_role to isolate RLS issues
4. **Analyze** against known patterns
5. **Fix** with specific SQL or code changes
6. **Verify** fix with test query

## Execution Steps

### Step 1: Identify Failure Type
- "permission denied" → RLS issue
- "JWT expired" / "not authenticated" → Auth issue
- "column does not exist" → Schema issue
- "function error" → Edge Function issue

### Step 2: Gather Context via MCP
```sql
-- Check table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'TABLE_NAME';

-- Check RLS status
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Check policies
SELECT * FROM pg_policies 
WHERE tablename = 'TABLE_NAME';
```

### Step 3: Test with Service Role
If query works with service_role but not anon/authenticated:
- RLS policy is blocking
- Check `USING` clause
- Check `WITH CHECK` clause

### Step 4: Common Fixes

**RLS policy missing:**
```sql
CREATE POLICY "Users can view own data" ON table_name
  FOR SELECT USING (auth.uid() = user_id);
```

**Auth not passing through:**
```typescript
const supabase = createServerClient(url, key, { cookies })
```

### Step 5: Verify
```sql
SELECT * FROM table_name LIMIT 1;
```

## Output Format

```markdown
## Supabase Debug Report

**Issue Type:** {RLS|Auth|Query|Function}
**Table/Function:** {name}

### Analysis
{what's happening and why}

### Root Cause
{specific policy/code causing issue}

### Fix Applied
```sql
{SQL or code change}
```

### Verification
{confirmation query works}
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
