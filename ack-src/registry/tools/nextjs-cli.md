# Next.js Tool Spec

type: cli
name: next-cli
binary: next (via npx or npm scripts)
install: Included with create-next-app
docs: https://nextjs.org/docs

## No MCP Server

Next.js doesn't have an MCP server. Use CLI via Bash and file operations.

## Commands

### Development
```bash
npm run dev                  # Start dev server (port 3000)
npm run dev -- -p 3001       # Custom port
```

### Production
```bash
npm run build                # Build for production
npm run start                # Start production server
```

### Utilities
```bash
npm run lint                 # ESLint check
npx next info                # Environment info for debugging
```

## Create New Project
```bash
npx create-next-app@latest my-app
# Options: TypeScript, ESLint, Tailwind, src/ directory, App Router
```

## Environment

Next.js auto-loads:
- `.env` - All environments
- `.env.local` - Local overrides (gitignored)
- `.env.development` - Dev only
- `.env.production` - Prod only

## Key Files

| File | Purpose |
|------|---------|
| `next.config.js` | Framework configuration |
| `middleware.ts` | Edge middleware |
| `tsconfig.json` | TypeScript config |
| `.env.local` | Environment variables |

## Exit Codes
- `0` - Success
- `1` - Build/lint error

## Notes

- Dev server supports Fast Refresh (hot reload)
- Build output in `.next/` directory
- Static export: `output: 'export'` in next.config.js
