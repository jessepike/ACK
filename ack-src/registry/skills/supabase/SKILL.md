---
name: supabase
description: Supabase database, auth, and Edge Functions procedures
version: 1.0.0
---

# Supabase Skill

Procedural knowledge for Supabase development and operations.

## Prerequisites

- Supabase CLI: `npm install -g supabase`
- Project linked: `supabase link --project-ref <ref>`
- Or use Supabase MCP (preferred): Add to `.mcp.json`

## MCP vs CLI

**Use MCP when available** (query data, inspect schema):
```json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp"
    }
  }
}
```

**Use CLI for** (local dev, migrations, Edge Functions):
```bash
supabase start          # Local dev environment
supabase db push        # Push migrations
supabase functions serve # Local Edge Functions
```

## Quick Reference

### Database Commands
```bash
supabase db diff                    # Show pending changes
supabase db push                    # Apply migrations to remote
supabase db pull                    # Pull remote schema
supabase db dump --schema-only      # Export schema
supabase migration new <name>       # Create migration file
```

### Auth Commands
```bash
supabase auth list-users            # List users (requires service key)
```

### Edge Functions
```bash
supabase functions new <name>       # Create function
supabase functions serve            # Run locally
supabase functions deploy <name>    # Deploy to production
supabase functions logs <name>      # View logs
```

## Database Patterns

### Migration File Structure
```
supabase/
├── config.toml
├── migrations/
│   ├── 20240101000000_create_users.sql
│   └── 20240102000000_add_items.sql
└── functions/
    └── my-function/
        └── index.ts
```

### Safe Migration Template
```sql
-- supabase/migrations/YYYYMMDDHHMMSS_description.sql

-- Up migration
CREATE TABLE IF NOT EXISTS items (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS
ALTER TABLE items ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users manage own items" ON items
  FOR ALL USING (auth.uid() = user_id);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_items_user_id ON items(user_id);
```

## Auth Patterns

### Client Setup (Next.js)
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Server Setup (Next.js App Router)
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          )
        },
      },
    }
  )
}
```

### Protected Route Check
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const supabase = createServerClient(/* ... */)
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  return response
}
```

## RLS Decision Tree

```
Need to protect data?
├── Yes → Enable RLS: ALTER TABLE x ENABLE ROW LEVEL SECURITY
│   ├── User owns data? → USING (auth.uid() = user_id)
│   ├── Role-based? → USING (auth.jwt()->>'role' = 'admin')
│   ├── Public read? → FOR SELECT USING (true)
│   └── Service only? → No policy (only service_role can access)
└── No → Leave RLS disabled (not recommended for user data)
```

## Debugging Decision Tree

```
Query returning empty/forbidden?
├── Check RLS: SELECT * FROM items; -- as service_role
│   ├── Data exists? → RLS policy blocking, check auth.uid()
│   └── No data? → Insert issue, check WITH CHECK clause
├── Check auth: SELECT auth.uid(); -- should return UUID
│   ├── Returns null? → User not authenticated
│   └── Returns UUID? → Policy condition not matching
└── Check policy: SELECT * FROM pg_policies WHERE tablename = 'items';

Edge Function failing?
├── 500 error → Check function logs: supabase functions logs <name>
├── CORS error → Add headers in response
├── Auth error → Verify SUPABASE_SERVICE_ROLE_KEY in env
└── Timeout → Function >60s, optimize or split

Realtime not updating?
├── Table replication enabled? → Check Replication settings in dashboard
├── RLS blocking? → Realtime respects RLS policies
└── Client subscription correct? → .on('postgres_changes', ...)
```

## Environment Variables

Required in `.env.local`:
```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # Server-only, never expose
```
