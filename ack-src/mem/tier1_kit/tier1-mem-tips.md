Maintaining and pruning CLAUDE.md files (and associated project markdown) is essential for staying within Claude's 200k token context window and ensuring the model doesn't get "distracted" by outdated instructions.The following best practices are compiled from Anthropic’s engineering guidelines and power-user workflows.1. Maintenance & Pruning StrategiesSince CLAUDE.md is prepended to every prompt, it should be treated as a hot cache of your most critical project information, not a comprehensive archive.The "Rule of Recency": Regularly remove completed tasks. If you use a todo section, prune items as soon as they are committed.Context Handoffs: When a conversation becomes too long (causing Claude to slow down or hallucinate), ask Claude to:"Summarize our progress, key technical decisions, and current blockers into a dense Markdown snippet for a new session." Replace your old CLAUDE.md content with this fresh summary.Modularize Knowledge: Don't put everything in one file.CLAUDE.md: Current active tasks, specific style rules, and immediate build commands.Architecture.md: Long-term design patterns and data schemas (only reference this when needed).Decisions.log: A history of "why" things were built a certain way (keep this out of active context unless debugging).2. Optimization for "Claude Code"If you are using the Claude Code CLI tool, optimization is even more critical for performance and cost.Optimization TipActionUse XML TagsWrap complex sections in tags like <architecture> or <rules> to help Claude parse hierarchy faster.Lean InstructionsAvoid narrative prose. Use short, declarative bullet points. (e.g., "Use ES modules" instead of "We have decided that for this project we will be using ES modules.")The # ShortcutIn a Claude Code session, use the # key to instantly add a new instruction or rule directly into your CLAUDE.md.Context ClearingUse the /clear command frequently to reset the local session window while keeping the CLAUDE.md file as the "anchor."3. Structural Best PracticesA well-optimized markdown file uses a hierarchy that Claude understands natively.Recommended CLAUDE.md Sections:Tech Stack: Specific versions (e.g., Next.js 14, Python 3.11).Naming Conventions: Variable casing, folder structure patterns.Build/Test Commands: The exact strings needed to run the project.The "Never" List: Explicitly state what Claude should not do (e.g., "Never use external CSS files, use Tailwind only").4. Automation & ToolsJina Reader: Use r.jina.ai/[URL] to convert documentation into clean, pruned markdown before adding it to your project knowledge. This removes "web junk" (headers, footers) that wastes tokens.Pre-processing: If you have massive files, use a "Rolling Summary" technique. Ask a separate Claude instance to condense a 50-page spec into a 2-page Markdown summary before feeding it to your main project agent.
------
This template is designed to maximize **information density** while minimizing **token waste**. It uses clear headers and XML-like structures, which help Claude's internal attention mechanism prioritize your instructions over the general noise of a codebase.

---

## The "Lean" CLAUDE.md Template

```markdown
# [Project Name] Context

<priority_rules>
- **Style:** [e.g., TypeScript, Functional, Tailwind, Shadcn]
- **No-Go's:** [e.g., No class-based components, No external state libs]
- **Testing:** [e.g., Vitest for logic, Playwright for E2E]
</priority_rules>

## 🛠 Tech Stack
- **Runtime:** [e.g., Node v20.x / Bun]
- **Framework:** [e.g., Next.js 14 (App Router)]
- **Database:** [e.g., Prisma + PostgreSQL]
- **Key Libs:** [e.g., Zod, TRPC, Lucide]

## ⌨️ Common Commands
- **Dev:** `npm run dev`
- **Build:** `npm run build`
- **Test:** `npm test`
- **Lint:** `npm run lint --fix`

## 🏗 Architecture Patterns
- **Folder Structure:** [e.g., Feature-based inside /src/features]
- **Data Flow:** [e.g., Server Actions for mutations, React Query for caching]
- **Naming:** [e.g., PascalCase for components, camelCase for utils]

## 📋 Current Focus (Prune Weekly)
- [ ] Task 1: [Short description]
- [ ] Task 2: [Short description]
- [x] Completed: [Briefly note recent major change to avoid repetition]

## ⚠️ Known Gotchas
- [e.g., Always use 'use client' for components using Framer Motion]
- [e.g., Hydration errors occur if using Date.now() in SSR]

```

---

## Why this works for Claude:

1. **`<priority_rules>` Tags:** Using pseudo-XML tags signals to Claude that this section is a high-priority "system directive." It helps prevent the model from slipping into its default training biases.
2. **Command Quick-Ref:** By including the exact strings for `Dev`, `Build`, and `Test`, Claude can execute or suggest commands via "Claude Code" without having to hunt through your `package.json`.
3. **The "Never" List:** AI models often perform better when told what *not* to do. It narrows the "probability space" of its responses.
4. **Recency Pruning:** The **Current Focus** section should be the only part of this file that changes daily. Keeping the "Completed" list short (only the last 2-3 items) prevents the context window from filling up with "zombie" information.

### Maintenance Pro-Tip:

Every Friday (or at the end of a sprint), run this prompt:

> *"Claude, review my CLAUDE.md and my recent git commits. Prune the 'Current Focus' section, move stable architectural decisions to the 'Patterns' section, and remove any redundant instructions to keep the file under 500 words."*

**Would you like me to fill in the placeholders (Tech Stack/Commands) based on a specific repository or set of files you have open?**
