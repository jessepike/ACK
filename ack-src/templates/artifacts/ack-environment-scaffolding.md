# Code Scaffolding: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "environment"
---

## Overview

<!-- 
Initial code structure to implement:
- Base components
- Configuration files
- Utility functions
- Type definitions
-->

**Goal:** Create minimal scaffolding to:
1. Render 3-panel layout
2. Connect to Supabase
3. Configure Tiptap
4. Set up routing

**Not included:**
- Full functionality (Week 2)
- Agent integration (Week 3)
- Polish/styling (ongoing)



## Configuration Files

<!-- 
Framework and tool configuration:
-->

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Supabase images
  images: {
    domains: ['[your-project-id].supabase.co'],
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_APP_NAME: 'ACK',
  },
};

module.exports = nextConfig;
```


### tailwind.config.ts

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Dark theme colors (from UI mockup)
        'editor-bg': '#2B2B2B',
        'sidebar-bg': '#1E1E1E',
        'header-bg': '#181818',
        'border': 'rgba(255, 255, 255, 0.1)',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'Monaco', 'monospace'],
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
export default config
```


### .eslintrc.json

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { 
      "argsIgnorePattern": "^_",
      "varsIgnorePattern": "^_"
    }],
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```


### .prettierrc

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```



## Type Definitions

<!-- 
Core TypeScript types:
-->

### types/database.ts

```typescript
// Generated from Supabase (run: supabase gen types typescript)

export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      projects: {
        Row: {
          id: string
          name: string
          description: string | null
          current_stage: string
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          description?: string | null
          current_stage?: string
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          description?: string | null
          current_stage?: string
          updated_at?: string
        }
      }
      artifacts: {
        Row: {
          id: string
          project_id: string
          name: string
          slug: string
          stage: string
          status: string
          content: Json
          section_metadata: Json
          sections_total: number
          sections_complete: number
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          project_id: string
          name: string
          slug: string
          stage: string
          status?: string
          content?: Json
          section_metadata?: Json
          sections_total?: number
          sections_complete?: number
        }
        Update: {
          // ... similar to Insert
        }
      }
      // ... other tables
    }
  }
}
```


### types/index.ts

```typescript
import { Database } from './database'

// Helper types
export type Project = Database['public']['Tables']['projects']['Row']
export type Artifact = Database['public']['Tables']['artifacts']['Row']
export type Message = Database['public']['Tables']['messages']['Row']

export type StageType = 'discovery' | 'design' | 'environment' | 'workflow' | 'implementation'
export type ArtifactStatus = 'draft' | 'finalized'

export interface SectionMetadata {
  slug: string
  title: string
  is_done: boolean
  is_collapsed: boolean
  order: number
}

// UI types
export interface ProgressStats {
  complete: number
  total: number
  percentage: number
  display: string
}
```



## Supabase Setup

<!-- 
Database client configuration:
-->

### lib/supabase/client.ts

```typescript
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
import { Database } from '@/types/database'

export function createClient() {
  return createClientComponentClient<Database>()
}

// Singleton for client components
export const supabase = createClient()
```


### lib/supabase/server.ts

```typescript
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { Database } from '@/types/database'

export function createServerClient() {
  return createServerComponentClient<Database>({ cookies })
}
```


### lib/supabase/queries.ts

```typescript
import { supabase } from './client'
import type { Artifact, Project } from '@/types'

export async function getProject(id: string) {
  const { data, error } = await supabase
    .from('projects')
    .select('*')
    .eq('id', id)
    .single()
  
  if (error) throw error
  return data as Project
}

export async function getArtifactsByStage(projectId: string, stage: string) {
  const { data, error } = await supabase
    .from('artifacts')
    .select('*')
    .eq('project_id', projectId)
    .eq('stage', stage)
    .order('name')
  
  if (error) throw error
  return data as Artifact[]
}

// ... more queries
```



## Tiptap Configuration

<!-- 
Editor setup:
-->

### lib/tiptap/extensions.ts

```typescript
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import CharacterCount from '@tiptap/extension-character-count'

export const extensions = [
  StarterKit.configure({
    heading: {
      levels: [1, 2, 3],
    },
    bulletList: {
      keepMarks: true,
      keepAttributes: false,
    },
  }),
  Placeholder.configure({
    placeholder: 'Start writing...',
  }),
  CharacterCount,
  // Add custom extensions later (Section node, Done checkbox)
]
```


### lib/tiptap/utils.ts

```typescript
import { JSONContent } from '@tiptap/core'

export function tiptapToMarkdown(json: JSONContent): string {
  // Convert Tiptap JSON to Markdown
  // Simplified version - full implementation in Week 2
  return JSON.stringify(json)
}

export function markdownToTiptap(markdown: string): JSONContent {
  // Convert Markdown to Tiptap JSON
  // Simplified version - full implementation in Week 2
  return JSON.parse(markdown)
}
```



## Base Components

<!-- 
Minimal UI components:
-->

### components/ui/button.tsx

```typescript
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          'rounded font-medium transition-colors',
          {
            'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
            'bg-gray-700 text-white hover:bg-gray-600': variant === 'secondary',
            'hover:bg-gray-800': variant === 'ghost',
            'px-2 py-1 text-sm': size === 'sm',
            'px-4 py-2 text-base': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'
```


### components/layout/header.tsx

```typescript
export function Header() {
  return (
    <header className="h-9 flex items-center justify-between px-4 bg-header-bg border-b border-border">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-400">ACK</span>
      </div>
      
      {/* Stage tabs will go here */}
      <nav className="flex-1"></nav>
      
      {/* User menu will go here */}
      <div></div>
    </header>
  )
}
```


### components/layout/sidebar.tsx

```typescript
export function Sidebar() {
  return (
    <aside className="w-60 bg-sidebar-bg border-r border-border flex flex-col">
      <div className="h-9 flex items-center px-3 justify-between border-b border-border">
        <span className="text-xs font-semibold uppercase text-gray-400 tracking-wide">
          Explorer
        </span>
      </div>
      
      {/* File tree will go here */}
      <div className="flex-1 overflow-y-auto p-2">
        <p className="text-sm text-gray-500">No files yet</p>
      </div>
    </aside>
  )
}
```


### components/layout/footer.tsx

```typescript
export function Footer() {
  return (
    <footer className="h-7 flex items-center justify-between px-3 bg-header-bg border-t border-border text-xs">
      <div className="flex items-center gap-3 text-gray-500">
        <span>Ln 1, Col 1</span>
      </div>
      <div className="flex items-center gap-3 text-gray-500">
        <span>UTF-8</span>
        <span>Markdown</span>
      </div>
    </footer>
  )
}
```


### components/editor/editor-placeholder.tsx

```typescript
export function EditorPlaceholder() {
  return (
    <div className="flex-1 bg-editor-bg flex items-center justify-center">
      <p className="text-gray-500">Select a file to edit</p>
    </div>
  )
}
```


### components/chat/chat-placeholder.tsx

```typescript
export function ChatPlaceholder() {
  return (
    <aside className="w-80 bg-sidebar-bg border-l border-border flex flex-col">
      <div className="h-9 flex items-center px-3 border-b border-border">
        <span className="text-xs font-semibold uppercase text-gray-400 tracking-wide">
          Assistant
        </span>
      </div>
      <div className="flex-1 p-4">
        <p className="text-sm text-gray-500">Chat coming soon</p>
      </div>
    </aside>
  )
}
```



## Layout Setup

<!-- 
Main layout structure:
-->

### app/layout.tsx

```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ACK - Agent Context Kit',
  description: 'AI-augmented planning layer for development',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gray-900 text-gray-100`}>
        {children}
      </body>
    </html>
  )
}
```


### app/page.tsx

```typescript
import { Header } from '@/components/layout/header'
import { Sidebar } from '@/components/layout/sidebar'
import { Footer } from '@/components/layout/footer'
import { EditorPlaceholder } from '@/components/editor/editor-placeholder'
import { ChatPlaceholder } from '@/components/chat/chat-placeholder'

export default function Home() {
  return (
    <div className="h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 flex overflow-hidden">
        <Sidebar />
        <EditorPlaceholder />
        <ChatPlaceholder />
      </main>
      
      <Footer />
    </div>
  )
}
```


### app/globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: content-box;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
```



## Utilities

<!-- 
Helper functions:
-->

### lib/utils.ts

```typescript
import { clsx, type ClassValue } from 'clsx'

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
}

export function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}
```



## Custom Hooks

<!-- 
React hooks for common patterns:
-->

### hooks/use-project.ts

```typescript
import { useState, useEffect } from 'react'
import { getProject } from '@/lib/supabase/queries'
import type { Project } from '@/types'

export function useProject(id: string) {
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  
  useEffect(() => {
    getProject(id)
      .then(setProject)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [id])
  
  return { project, loading, error }
}
```



---

## Scaffolding Checklist

### Configuration Files
- [ ] next.config.js created
- [ ] tailwind.config.ts configured
- [ ] .eslintrc.json set up
- [ ] .prettierrc created
- [ ] globals.css with base styles

### Type Definitions
- [ ] types/database.ts generated from Supabase
- [ ] types/index.ts with core types
- [ ] All exports properly typed

### Supabase Setup
- [ ] lib/supabase/client.ts
- [ ] lib/supabase/server.ts
- [ ] lib/supabase/queries.ts with basic queries
- [ ] Connection tested

### Tiptap Setup
- [ ] lib/tiptap/extensions.ts
- [ ] lib/tiptap/utils.ts
- [ ] Basic editor renders

### Base Components
- [ ] Button component
- [ ] Header component
- [ ] Sidebar component
- [ ] Footer component
- [ ] Placeholder components

### Layout
- [ ] app/layout.tsx root layout
- [ ] app/page.tsx main page
- [ ] 3-panel layout renders correctly

### Testing
- [ ] `npm run dev` works
- [ ] 3-panel layout visible
- [ ] No console errors
- [ ] TypeScript compiles


---

## Verification Commands

```bash
# Start dev server
npm run dev

# Check TypeScript
npm run type-check

# Check linting
npm run lint

# Format code
npx prettier --write .
```


---

**Expected result:** 
- Visit `http://localhost:3000`
- See 3-panel layout (sidebar, editor placeholder, chat placeholder)
- Header and footer render
- No functionality yet - just structure


**Next steps:** Week 2 - Implement actual functionality (file tree, editor, state management)
