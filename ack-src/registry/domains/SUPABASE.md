# Supabase Domain Package

**Purpose:** Database design, auth, RLS, Edge Functions, real-time

## Components

### Agent: `supabase-expert`
Senior Supabase specialist. Database design, Row Level Security, Auth flows, Edge Functions, real-time subscriptions.

**Invoked when:** Designing schema, setting up auth, writing RLS policies, debugging queries, creating Edge Functions.

### Skill: `supabase/SKILL.md`
Procedural knowledge:
- MCP vs CLI decision guide
- RLS policy patterns and decision tree
- Auth setup (Next.js SSR, client, server)
- Migration file templates
- Edge Function patterns
- Debugging decision tree

### Tool: `supabase.md`
- **MCP Server:** `https://mcp.supabase.com/mcp` — Primary. Query data, inspect schema, run SQL.
- **CLI:** `supabase` — For migrations, local dev, Edge Functions, type generation.
- **Scripts:** Migration generators if needed.

### Command: `supabase-debug`
Trigger: `/supabase-debug` or "supabase query failing"

Workflow:
1. Check MCP connection
2. Identify failure type (RLS, auth, query, function)
3. Inspect relevant schema/policies
4. Test query with service_role to bypass RLS
5. Apply fix
6. Verify with test query

## Quick Start

```bash
# In your project
ln -s ~/code/tools/claude-registry/agents/supabase-expert.md .claude/agents/
ln -s ~/code/tools/claude-registry/commands/supabase-debug.md .claude/commands/

# Add to .mcp.json
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp"
    }
  }
}
```

## Documentation Sources
- https://supabase.com/docs
- https://supabase.com/docs/guides/auth
- https://supabase.com/docs/guides/database
- https://supabase.com/docs/guides/functions
- https://supabase.com/docs/reference/javascript

## When to Use
- Design database schema
- Write RLS policies
- Set up authentication
- Create Edge Functions
- Debug query permissions
- Set up real-time subscriptions
- Generate TypeScript types
