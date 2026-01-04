# Repository Initialization: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "environment"
---

## Repository Setup

<!-- 
Initial repository configuration:
- Git initialization
- Remote setup
- Branch strategy
- .gitignore
-->

### Git Initialization

**Repository name:**


**Remote URL:**


**Initial setup commands:**
```bash
# Initialize repo
git init

# Set remote
git remote add origin [URL]

# Set default branch
git branch -M main

# Initial commit
git add .
git commit -m "Initial commit: ACK v1.0 project setup"
git push -u origin main
```


### Branch Strategy

**Branch model:**
- [ ] Git Flow (main, develop, feature/*, hotfix/*)
- [ ] GitHub Flow (main, feature/*)
- [ ] Trunk-based (main only)

**Branch naming:**
- Features: `feature/[name]` (e.g., `feature/tiptap-editor`)
- Fixes: `fix/[name]`
- Releases: `release/v[version]`


### .gitignore Configuration

**Template:**
```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output

# Next.js
.next/
out/
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Vercel
.vercel

# Misc

```



## Project Structure

<!-- 
Directory organization:
- Folder layout
- File organization
- Module boundaries
-->

### Directory Tree

```
/ack-mvp/
│
├── /app/                       # Next.js App Router
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   ├── /projects/              # Projects routes
│   │   ├── page.tsx            # Projects list
│   │   └── /[id]/              # Project detail
│   │       ├── page.tsx
│   │       └── /[stage]/       # Stage view
│   └── /api/                   # API routes
│       ├── /projects/
│       ├── /artifacts/
│       └── /chat/
│
├── /components/                # React components
│   ├── /ui/                    # Base UI components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   └── dialog.tsx
│   ├── /layout/                # Layout components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── footer.tsx
│   ├── /editor/                # Editor components
│   │   ├── tiptap-editor.tsx
│   │   ├── section-node.tsx
│   │   └── toolbar.tsx
│   └── /chat/                  # Chat components
│       ├── chat-panel.tsx
│       ├── message-bubble.tsx
│       └── input.tsx
│
├── /lib/                       # Utilities & config
│   ├── /supabase/              # Supabase client
│   │   ├── client.ts
│   │   ├── server.ts
│   │   └── /queries/
│   ├── /tiptap/                # Tiptap config
│   │   ├── extensions.ts
│   │   └── utils.ts
│   ├── /agents/                # Agent logic
│   │   ├── context.ts
│   │   └── operations.ts
│   └── utils.ts                # General utilities
│
├── /types/                     # TypeScript types
│   ├── database.ts             # Supabase types
│   ├── tiptap.ts              # Tiptap types
│   └── index.ts
│
├── /hooks/                     # Custom React hooks
│   ├── use-artifact.ts
│   ├── use-chat.ts
│   └── use-project.ts
│
├── /config/                    # Configuration
│   ├── site.ts                # Site config
│   └── constants.ts
│
├── /public/                    # Static assets
│   ├── /images/
│   └── /icons/
│
├── /scripts/                   # Utility scripts
│   ├── seed.ts                # Database seeding
│   └── migrate.ts
│
├── /docs/                      # Documentation
│   ├── README.md
│   └── /architecture/
│
├── .env.example               # Environment template
├── .eslintrc.json            # ESLint config
├── .prettierrc               # Prettier config
├── next.config.js            # Next.js config
├── tailwind.config.ts        # Tailwind config
├── tsconfig.json             # TypeScript config
├── package.json              # Dependencies
└── README.md                 # Project readme
```



## Environment Configuration

<!-- 
Environment variables and secrets:
- Required variables
- Optional variables
- Local vs production
-->

### Required Environment Variables

**.env.local:**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://[project-id].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[anon-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]

# Anthropic
ANTHROPIC_API_KEY=[api-key]

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

**.env.production:**
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://[project-id].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=[anon-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]

# Anthropic
ANTHROPIC_API_KEY=[api-key]

# App
NEXT_PUBLIC_APP_URL=https://ipe.yourdomain.com
NODE_ENV=production

# Analytics (optional)
NEXT_PUBLIC_GA_ID=[ga-id]
```

### Environment Variable Checklist

- [ ] Created `.env.example` with all required vars (no values)
- [ ] Created `.env.local` with actual values
- [ ] Added `.env*` to .gitignore
- [ ] Documented each variable in README
- [ ] Set production vars in Vercel dashboard



## README Documentation

<!-- 
What should the README include?
-->

### README.md Template

```markdown
# ACK - Agent Context Kit

AI-augmented planning layer for development projects.

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Supabase account
- Anthropic API key

### Installation

\`\`\`bash
# Clone repo
git clone [url]
cd ack-mvp

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with your keys

# Run database migrations
npm run db:migrate

# Start dev server
npm run dev
\`\`\`

Visit `http://localhost:3000`

## Project Structure

See [ARCHITECTURE.md](./docs/ARCHITECTURE.md)

## Tech Stack

- **Frontend:** Next.js 14, React, Tailwind CSS
- **Editor:** Tiptap
- **Database:** Supabase (PostgreSQL)
- **AI:** Anthropic Claude
- **Deployment:** Vercel

## Development

\`\`\`bash
# Run dev server
npm run dev

# Run tests
npm test

# Lint
npm run lint

# Type check
npm run type-check
\`\`\`

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

[Your License]
```



## Initial Files

<!-- 
Critical files to create immediately:
-->

### package.json

**Initial dependencies:**
```json
{
  "name": "ack-mvp",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@supabase/supabase-js": "^2.38.0",
    "@tiptap/react": "^2.1.0",
    "@tiptap/starter-kit": "^2.1.0",
    "@anthropic-ai/sdk": "^0.10.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "tailwindcss": "^3.4.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "14.2.0"
  }
}
```


### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```



---

## Setup Checklist

### Phase 1: Repository
- [ ] Create GitHub repository
- [ ] Clone locally
- [ ] Initialize git
- [ ] Create initial .gitignore
- [ ] First commit and push

### Phase 2: Project Files
- [ ] Create package.json
- [ ] Create tsconfig.json
- [ ] Create next.config.js
- [ ] Create tailwind.config.ts
- [ ] Create .env.example

### Phase 3: Directory Structure
- [ ] Create /app directory
- [ ] Create /components directory
- [ ] Create /lib directory
- [ ] Create /types directory
- [ ] Create /hooks directory
- [ ] Create /public directory

### Phase 4: Configuration
- [ ] Set up environment variables
- [ ] Configure ESLint
- [ ] Configure Prettier
- [ ] Set up TypeScript

### Phase 5: Documentation
- [ ] Write README.md
- [ ] Create CONTRIBUTING.md
- [ ] Create LICENSE
- [ ] Document environment setup


---

## Commands Reference

```bash
# Initialize new Next.js project
npx create-next-app@latest ack-mvp

# Install dependencies
npm install [package-name]

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run type checking
npm run type-check

# Run linting
npm run lint

# Run tests
npm test
```


---

**Next steps:** See `dependencies.md` for package installation
