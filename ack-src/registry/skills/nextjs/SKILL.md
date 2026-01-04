---
type: skill
description: "Next.js 14+ App Router patterns and procedures"
version: 1.0.0
updated: "2026-01-04T09:26:12"
name: nextjs
---

# Next.js Skill

Procedural knowledge for Next.js 14+ App Router development.

## Quick Reference

### Project Commands
```bash
npx create-next-app@latest      # New project
npm run dev                      # Development server
npm run build                    # Production build
npm run start                    # Production server
npm run lint                     # Lint check
```

### File Naming Conventions
| File | Purpose |
|------|---------|
| `page.tsx` | Route UI (makes folder a route) |
| `layout.tsx` | Shared wrapper (persists across navigations) |
| `loading.tsx` | Loading state (Suspense boundary) |
| `error.tsx` | Error state (Error boundary) |
| `not-found.tsx` | 404 state |
| `route.ts` | API endpoint |
| `template.tsx` | Re-renders on navigation (unlike layout) |
| `default.tsx` | Parallel route fallback |

## App Router Structure

### Basic Routes
```
app/
├── page.tsx                 # → /
├── about/page.tsx           # → /about
├── blog/
│   ├── page.tsx             # → /blog
│   └── [slug]/page.tsx      # → /blog/:slug
└── api/
    └── users/route.ts       # → /api/users
```

### Route Groups (Organization Only)
```
app/
├── (marketing)/
│   ├── about/page.tsx       # → /about
│   └── contact/page.tsx     # → /contact
└── (dashboard)/
    ├── layout.tsx           # Dashboard-specific layout
    └── settings/page.tsx    # → /settings
```

### Parallel Routes
```
app/
├── @modal/
│   └── login/page.tsx       # Renders in modal slot
├── layout.tsx               # Receives modal as prop
└── page.tsx
```

## Data Fetching Patterns

### Pattern 1: Server Component Fetch
```typescript
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Cache 1 hour
  })
  return res.json()
}

export default async function PostsPage() {
  const posts = await getPosts()
  return <PostList posts={posts} />
}
```

### Pattern 2: Server Action (Mutations)
```typescript
// app/posts/actions.ts
"use server"

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  
  // Insert to database
  await db.posts.create({ data: { title } })
  
  revalidatePath('/posts')
  redirect('/posts')
}

// Usage in component:
<form action={createPost}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

### Pattern 3: Route Handler (API)
```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const posts = await db.posts.findMany()
  return NextResponse.json(posts)
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.posts.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

### Pattern 4: Client-side with React Query
```typescript
// components/posts.tsx
"use client"

import { useQuery } from '@tanstack/react-query'

export function Posts() {
  const { data, isLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(r => r.json())
  })
  
  if (isLoading) return <div>Loading...</div>
  return <PostList posts={data} />
}
```

## Caching Strategies

### Static (Default)
```typescript
// Cached at build time, never revalidates
fetch('https://api.example.com/data')
```

### Time-based Revalidation
```typescript
// Revalidate every hour
fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
})
```

### On-demand Revalidation
```typescript
// In Server Action or Route Handler
import { revalidatePath, revalidateTag } from 'next/cache'

revalidatePath('/posts')           // Revalidate specific path
revalidateTag('posts')             // Revalidate by tag
```

### No Cache
```typescript
// Always fetch fresh
fetch('https://api.example.com/data', {
  cache: 'no-store'
})
```

## Metadata

### Static Metadata
```typescript
// app/about/page.tsx
export const metadata = {
  title: 'About Us',
  description: 'Learn about our company'
}
```

### Dynamic Metadata
```typescript
// app/posts/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt
  }
}
```

## Common Middleware Patterns

### Auth Middleware
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')
  
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*']
}
```

## Decision Trees

### Server vs Client Component
```
Does component need...
├── useState/useEffect/useContext → Client ("use client")
├── onClick/onChange handlers → Client
├── Browser APIs (window, localStorage) → Client
├── Direct database access → Server (default)
├── Fetch without user interaction → Server
└── Access to request headers/cookies → Server
```

### Data Fetching Choice
```
What type of data operation?
├── Read on page load → Server Component fetch
├── Read with user interaction → Client fetch or Server Action
├── Create/Update/Delete → Server Action
├── Need JSON API for external → Route Handler
└── Real-time updates → Client with subscription
```

### Caching Strategy
```
How fresh does data need to be?
├── Static forever → Default (no options)
├── Fresh within X seconds → next: { revalidate: X }
├── Always fresh → cache: 'no-store'
├── Fresh after mutation → revalidatePath/revalidateTag
└── User-specific → cache: 'no-store' + cookies()
```

## Environment Variables

```bash
# .env.local
# Public (exposed to browser)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Private (server only)
SUPABASE_SERVICE_ROLE_KEY=eyJ...
DATABASE_URL=postgresql://...
```

Access:
- Server: `process.env.DATABASE_URL`
- Client: `process.env.NEXT_PUBLIC_SUPABASE_URL`

## Build Optimization

### Analyze Bundle
```bash
npm install @next/bundle-analyzer
# Add to next.config.js, then:
ANALYZE=true npm run build
```

### Common Build Errors
```
Dynamic server usage → Add export const dynamic = 'force-dynamic'
Missing generateStaticParams → Add function for static paths
Hydration mismatch → Check for browser-only code in Server Component
```
