---
type: domain
description: "Next.js Domain Package"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Next.js Domain Package

**Purpose:** App Router development, data fetching, server/client components, deployment

## Components

### Agent: `nextjs-expert`
Senior Next.js specialist. App Router architecture, Server Components, data fetching patterns, caching, deployment optimization.

**Invoked when:** Building pages, choosing data fetching strategy, debugging hydration, optimizing builds.

### Skill: `nextjs/SKILL.md`
Procedural knowledge:
- File naming conventions (page.tsx, layout.tsx, etc.)
- Server vs Client component decision tree
- Data fetching patterns (Server Component, Server Actions, Route Handlers)
- Caching strategies
- Middleware patterns
- Build optimization

### Tool: `nextjs-cli.md`
- **CLI:** `next` via npm scripts — No MCP available. Use `npm run dev/build/start`.
- **Scripts:** Build analysis, lint checks.

### Command: `nextjs-debug`
Trigger: `/nextjs-debug` or "next build failing"

Workflow:
1. Identify error type (hydration, build, runtime)
2. Check for Server/Client component misuse
3. Verify data fetching patterns
4. Run `npm run build` to surface errors
5. Apply fix
6. Verify build succeeds

## Quick Start

```bash
# In your project
ln -s ~/code/tools/claude-registry/agents/nextjs-expert.md .claude/agents/
ln -s ~/code/tools/claude-registry/commands/nextjs-debug.md .claude/commands/

# No MCP needed — uses file operations and npm scripts
```

## Documentation Sources
- https://nextjs.org/docs
- https://nextjs.org/docs/app
- https://nextjs.org/docs/app/building-your-application/data-fetching
- https://nextjs.org/docs/app/building-your-application/caching

Use Context7 MCP for up-to-date Next.js documentation:
```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio", 
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

## When to Use
- Build pages and routes
- Choose data fetching strategy
- Debug hydration mismatches
- Fix "use client" errors
- Optimize caching
- Set up middleware
- Configure for deployment
