# Dependencies: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "environment"
---

## Core Dependencies

<!-- 
Primary packages required for MVP:
- Framework dependencies
- UI libraries
- Database clients
- AI SDKs
-->

### Framework & Runtime

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| next | ^14.2.0 | React framework, routing, SSR | ~500KB | MIT |
| react | ^18.2.0 | UI library | ~130KB | MIT |
| react-dom | ^18.2.0 | React DOM rendering | ~130KB | MIT |
| typescript | ^5.3.0 | Type safety | Dev only | Apache-2.0 |


### Editor & Rich Text

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| @tiptap/react | ^2.1.0 | React wrapper for editor | ~50KB | MIT |
| @tiptap/starter-kit | ^2.1.0 | Basic editor extensions | ~100KB | MIT |
| @tiptap/extension-placeholder | ^2.1.0 | Placeholder text | ~5KB | MIT |
| @tiptap/extension-character-count | ^2.1.0 | Character counting | ~5KB | MIT |


### Database & Backend

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| @supabase/supabase-js | ^2.38.0 | Supabase client | ~150KB | MIT |
| @supabase/auth-helpers-nextjs | ^0.8.0 | Next.js auth helpers | ~20KB | MIT |


### AI & Agents

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| @anthropic-ai/sdk | ^0.10.0 | Claude API client | ~80KB | MIT |


### Styling & UI

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| tailwindcss | ^3.4.0 | CSS framework | Dev only | MIT |
| @tailwindcss/forms | ^0.5.7 | Form styling | Dev only | MIT |
| lucide-react | ^0.303.0 | Icon library | ~20KB | ISC |


### Utilities

| Package | Version | Purpose | Size | License |
|---------|---------|---------|------|---------|
| zod | ^3.22.0 | Schema validation | ~60KB | MIT |
| date-fns | ^3.0.0 | Date utilities | ~20KB | MIT |
| clsx | ^2.1.0 | Class name merging | ~1KB | MIT |



## Development Dependencies

<!-- 
Dev-only packages:
- Testing
- Linting
- Type checking
- Build tools
-->

### Code Quality

| Package | Version | Purpose |
|---------|---------|---------|
| eslint | ^8.56.0 | Linting |
| eslint-config-next | ^14.2.0 | Next.js ESLint config |
| @typescript-eslint/parser | ^6.19.0 | TypeScript ESLint parser |
| prettier | ^3.2.0 | Code formatting |
| prettier-plugin-tailwindcss | ^0.5.11 | Tailwind class sorting |


### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| @testing-library/react | ^14.1.0 | React testing |
| @testing-library/jest-dom | ^6.1.0 | Jest DOM matchers |
| jest | ^29.7.0 | Test runner |
| @types/jest | ^29.5.0 | Jest TypeScript types |


### Type Definitions

| Package | Version | Purpose |
|---------|---------|---------|
| @types/node | ^20.11.0 | Node.js types |
| @types/react | ^18.2.0 | React types |
| @types/react-dom | ^18.2.0 | React DOM types |



## Installation Commands

<!-- 
Step-by-step installation:
-->

### Initial Setup

```bash
# Create Next.js app (if not already done)
npx create-next-app@latest ack-mvp --typescript --tailwind --app

cd ack-mvp
```

### Core Packages

```bash
# Supabase
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs

# Tiptap
npm install @tiptap/react @tiptap/starter-kit \
  @tiptap/extension-placeholder \
  @tiptap/extension-character-count

# Anthropic
npm install @anthropic-ai/sdk

# UI & Utilities
npm install lucide-react zod date-fns clsx
```

### Development Tools

```bash
# Testing
npm install --save-dev @testing-library/react \
  @testing-library/jest-dom \
  jest @types/jest

# Code quality
npm install --save-dev prettier \
  prettier-plugin-tailwindcss
```



## Dependency Justification

<!-- 
Why each major dependency was chosen:
-->

### Next.js
**Why:**
- Server-side rendering for better SEO
- Built-in API routes
- Excellent TypeScript support
- App Router for modern patterns
- Easy Vercel deployment

**Alternatives considered:**
- Vite + React Router: More lightweight but need separate backend
- Remix: Great but less mature ecosystem


### Tiptap
**Why:**
- Built on ProseMirror (battle-tested)
- Extensible (custom nodes for sections)
- React-first API
- Markdown support
- Collaborative editing ready

**Alternatives considered:**
- Lexical: Too new, less stable
- Slate: Good but more complex
- ProseMirror direct: Too low-level


### Supabase
**Why:**
- PostgreSQL + real-time + auth + storage in one
- Row Level Security for multi-tenancy
- Vector support (pgvector) for future RAG
- Excellent TypeScript support
- Free tier generous

**Alternatives considered:**
- Firebase: NoSQL doesn't fit relational data model
- Custom PostgreSQL + separate services: More complex
- MongoDB: Poor fit for structured data


### Anthropic SDK
**Why:**
- Official SDK
- TypeScript support
- Streaming responses
- Tool/function calling

**Alternatives considered:**
- Direct HTTP: More complex, no types
- LangChain: Too heavy for our needs



## Version Management

<!-- 
How to manage dependency versions:
-->

### Versioning Strategy

**Lock exact versions for:**
- Core framework (Next.js, React)
- Database client (Supabase)
- Editor (Tiptap)

**Allow minor updates for:**
- UI utilities
- Icons
- Date libraries

**package.json convention:**
```json
{
  "dependencies": {
    "next": "14.2.0",          // Exact version (no ^)
    "@tiptap/react": "^2.1.0", // Allow patch updates
    "lucide-react": "^0.303.0" // Allow minor updates
  }
}
```


### Update Policy

**Check for updates:**
```bash
# Check outdated packages
npm outdated

# Update specific package
npm update [package-name]

# Update all (be careful)
npm update
```

**Testing before major updates:**
1. Read changelog
2. Test in dev
3. Run full test suite
4. Check bundle size impact



## Bundle Size Optimization

<!-- 
Keeping bundle small:
-->

### Bundle Analysis

```bash
# Analyze bundle
npm run build
# Check .next/analyze output
```

### Tree Shaking

**Ensure proper imports:**
```typescript
// ✓ Good - tree-shakeable
import { Button } from 'lucide-react';

// ✗ Bad - imports everything
import * as Icons from 'lucide-react';
```

### Code Splitting

**Dynamic imports for heavy components:**
```typescript
// Lazy load editor
const TiptapEditor = dynamic(() => import('@/components/editor/tiptap'), {
  ssr: false,
  loading: () => <EditorSkeleton />
});
```


### Target Bundle Sizes

| Route | Target | Current | Status |
|-------|--------|---------|--------|
| Home | < 100KB | | |
| Editor | < 300KB | | |
| Chat | < 200KB | | |



## Security Considerations

<!-- 
Dependency security:
-->

### Audit Commands

```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities (auto)
npm audit fix

# Fix with breaking changes
npm audit fix --force
```

### Regular Checks

**Schedule:**
- Weekly: `npm audit`
- Monthly: `npm outdated`
- Quarterly: Major version reviews


### Known Vulnerabilities

**Currently tracking:**
- [ ] None


### Dependency Policies

**Avoid:**
- Packages with critical vulnerabilities
- Unmaintained packages (>1 year no updates)
- Packages with unclear licenses
- Very large packages (>1MB) unless essential



## Alternative Implementations

<!-- 
If we need to replace dependencies:
-->

### Replacement Options

**If Tiptap doesn't work:**
- Plan B: Lexical (Meta)
- Plan C: ProseMirror direct
- Migration effort: ~2 weeks

**If Supabase doesn't scale:**
- Plan B: Self-hosted PostgreSQL + separate auth
- Migration: ~4 weeks
- Cost: Higher

**If Anthropic API is unavailable:**
- Plan B: OpenAI GPT-4
- Plan C: Open-source model (Llama)
- Code changes: Minimal (abstracted agent layer)



---

## Installation Checklist

### Pre-Installation
- [ ] Node.js 18+ installed
- [ ] npm or yarn installed
- [ ] Git installed

### Core Installation
- [ ] Created Next.js project
- [ ] Installed Supabase client
- [ ] Installed Tiptap packages
- [ ] Installed Anthropic SDK
- [ ] Installed UI dependencies

### Configuration
- [ ] Configured TypeScript
- [ ] Configured Tailwind
- [ ] Configured ESLint
- [ ] Configured Prettier

### Verification
- [ ] `npm run dev` works
- [ ] `npm run build` succeeds
- [ ] `npm run type-check` passes
- [ ] `npm run lint` passes

### Documentation
- [ ] Updated README with dependencies
- [ ] Documented required environment variables
- [ ] Created .env.example


---

**Next steps:** See `scaffolding.md` for initial code setup
