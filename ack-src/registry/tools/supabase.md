---
type: tool
description: "Supabase Tool Spec"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Supabase Tool Spec

## MCP Server (Preferred)

type: mcp
name: supabase-mcp
url: https://mcp.supabase.com/mcp

### Configuration
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

### Capabilities via MCP
- Query database (SELECT)
- Inspect schema
- List tables and columns
- View RLS policies
- Execute SQL (with appropriate permissions)

### Authentication
OAuth flow — Claude will prompt to connect your Supabase account on first use.

---

## CLI (For Migrations & Local Dev)

type: cli
name: supabase-cli
binary: supabase
install: npm install -g supabase
docs: https://supabase.com/docs/guides/cli

### Authentication
```bash
supabase login           # Browser OAuth
supabase link --project-ref <ref>  # Link to project
```

### When to Use CLI vs MCP

| Task | Use |
|------|-----|
| Query data | MCP |
| Inspect schema | MCP |
| Create migration | CLI |
| Push migrations | CLI |
| Local development | CLI |
| Edge Functions | CLI |
| Generate types | CLI |

### Core Commands
```bash
supabase start              # Start local stack
supabase stop               # Stop local stack
supabase db push            # Apply migrations
supabase db pull            # Pull remote changes
supabase gen types typescript  # Generate TS types
supabase functions serve    # Run functions locally
supabase functions deploy   # Deploy function
```

### Environment Variables (CLI)
```bash
SUPABASE_ACCESS_TOKEN       # From supabase login
SUPABASE_DB_PASSWORD        # Database password
```

### Exit Codes
- `0` - Success
- `1` - General error
- `2` - Auth required
