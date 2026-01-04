---
# Core
type: "architecture"
description: "Tier-1 Memory Kit specification for Claude Code native memory system"
version: "2.0.0"
updated: "2026-01-03T10:00:00"

# Optional
scope: "global"
depends_on: ["ags-spec"]
---

# Tier-1 Memory Kit Specification

## Purpose

Define the structure, content, and governance of Claude Code's native memory system (CLAUDE.md + rules/) as Tier-1 of the two-tier memory architecture.

Tier-1 provides **curated, stable guidance** that persists across sessions: conventions, invariants, preferences, and workflow rules.

---

## Scope

### In Scope
- Global memory (`~/.claude/CLAUDE.md`)
- Project memory (`.claude/CLAUDE.md` + `.claude/rules/`)
- Local memory (`CLAUDE.local.md`)
- Frontmatter schema for memory files
- Governance and change management
- Plan/task workflow patterns
- Commit governance

### Out of Scope
- Tier-2 (claude-mem) — separate specification
- Cross-project memory promotion — deferred
- Conditional `paths:` loading — deferred until specific use case
- Rules directory at global level — deferred (content fits in single file)

---

## Constraints

- **Line limit:** 200 lines max per file (soft target: 150)
- **Progressive disclosure:** Essential info first, details via imports
- **YAML frontmatter:** Required on all governed memory files
- **Token budgets:** Global ~2k, Project ~5k, Local ~1k

---

## Memory Hierarchy (Official Claude Code Behavior)

Claude Code loads memory in this order. **All levels are loaded; higher priority wins on conflict.**

| Priority | Location | Purpose | Shared |
|----------|----------|---------|--------|
| 1 (highest) | Enterprise `/Library/Application Support/ClaudeCode/CLAUDE.md` | Org-wide policy | All users |
| 2 | Project `.claude/CLAUDE.md` or `./CLAUDE.md` | Team-shared | Team via git |
| 3 | User `~/.claude/CLAUDE.md` | Personal defaults | Just you |
| 4 (lowest) | Local `./CLAUDE.local.md` | Personal overrides | Just you |

**Precedence model:**
- All memory files are loaded
- If no conflict, all content applies
- On conflict, higher priority wins
- User preferences are defaults; projects can override

**Rules directories:**
- `~/.claude/rules/*.md` — User-level (loaded before project)
- `.claude/rules/*.md` — Project-level (same priority as project CLAUDE.md)
- All `.md` files auto-loaded; subdirectories supported

---

## Level Allocation

### Global Level (`~/.claude/CLAUDE.md`)

**Purpose:** Universal invariants that apply to ALL projects. Personal workflow defaults.

**Structure:**
```
~/.claude/
└── CLAUDE.md              # All global content (no rules/ directory needed)
```

**Content:**
- Security invariants (never commit secrets)
- Safety protocols (confirm destructive ops)
- Commit standards
- Plan implementation workflow
- Communication preferences

**Token budget:** ~2,000 tokens
**Modification:** Human only

**Note:** No `~/.claude/rules/` directory for now. Add later if content exceeds single file capacity.

### Project Level (`.claude/`)

**Purpose:** Project-specific rules, decisions, and ephemeral working state.

**Structure:**
```
.claude/
├── CLAUDE.md              # Project context + ephemeral state (agent-writable)
└── rules/                 # Governing rules (human-controlled)
    ├── architecture.md    # Structural decisions
    ├── stack.md           # Technology-specific rules
    └── domain.md          # Domain terminology, business rules
```

**Token budget:** ~5,000 tokens for rules, additional via @imports
**Modification:** 
- CLAUDE.md: Agent (via hooks) or human
- rules/: Human only (honor system, document constraint in global CLAUDE.md)

### Local Level (`./CLAUDE.local.md`)

**Purpose:** Personal overrides, temporary context, sensitive local config.

**Location:** Project root (NOT inside `.claude/`)
**Auto-gitignored:** Yes

**Content:**
- Environment-specific overrides
- Temporary debugging notes
- Local credentials references

**Token budget:** ~1,000 tokens
**Modification:** Anyone, no tracking

---

## Frontmatter Schema

### Core Fields (Required on ALL Memory Files)

```yaml
---
# Core (required)
type: "rule_constitution"
description: "Universal security and integrity invariants"
version: "1.0.0"
updated: "2026-01-02T14:30:00"
---
```

| Field | Format | Purpose |
|-------|--------|---------|
| `type` | controlled vocabulary | Document category |
| `description` | string | Human-readable purpose (filename is machine ID) |
| `version` | SemVer X.Y.Z | Track meaning changes |
| `updated` | ISO 8601 datetime | Last modification timestamp |

### Optional Fields (Document-Specific)

```yaml
---
# Core (required)
type: "memory_project"
description: "Project context and current working state"
version: "1.0.0"
updated: "2026-01-02T14:30:00"

# Optional (document-specific)
scope: "project"
paths: "src/api/**/*.ts"
depends_on: ["architecture.md"]
---
```

| Field | When Used |
|-------|-----------|
| `scope` | CLAUDE.md files (global/project/local disambiguation) |
| `paths` | Conditional loading (future use) |
| `depends_on` | Rules that reference other rules |

### Type Vocabulary (Memory-Specific)

**Global types:**
- `memory_global` — Global CLAUDE.md entry point
- `rule_constitution` — Non-negotiable invariants

**Project types:**
- `memory_project` — Project CLAUDE.md entry point
- `rule_architecture` — Structural decisions
- `rule_stack` — Technology-specific rules
- `rule_domain` — Business rules, terminology
- `rule_testing` — Testing conventions
- `rule_security` — Security requirements

**Other:**
- `plan` — Implementation plan files

---

## Static vs Dynamic Sections

Memory files (especially project CLAUDE.md) contain both stable and ephemeral content.

**Use HTML comments to mark sections:**

```markdown
<!-- ====== STATIC SECTION (preserve on prune) ====== -->

## Stack
...

## Commands
...

<!-- ====== DYNAMIC SECTION (prune regularly) ====== -->

## Current Focus
...

## Recent Activity
...
```

| Section Type | Content | Prune Behavior |
|--------------|---------|----------------|
| **Static** | Stack, commands, architecture, gotchas | Preserve |
| **Dynamic** | Current focus, recent activity, active plan pointer | Prune regularly |

---

## XML Tags for Priority Signaling

Use `<constraints>` tags for highest-priority invariants in global CLAUDE.md:

```markdown
<constraints>
- Never commit secrets, credentials, or API keys
- Never modify `.claude/rules/` without explicit human approval
- Commit after completing each task
</constraints>
```

**Use XML tags for:**
- Global constraints (non-negotiables)
- Critical safety rules

**Do NOT use for:**
- Everything else (standard markdown headers are sufficient)

---

## Governance Model

| Level | Who Can Modify | Change Process |
|-------|----------------|----------------|
| Global (`~/.claude/CLAUDE.md`) | Human only | Manual edit + version bump |
| Project rules (`.claude/rules/`) | Human only | Edit + commit to git (honor system) |
| Project CLAUDE.md (`.claude/CLAUDE.md`) | Agent or human | Auto-maintained, prune regularly |
| Local (`CLAUDE.local.md`) | Anyone | No tracking |

### Rules Protection

Agents should NOT modify `.claude/rules/` directly. This is enforced by:

1. **Documentation** (current): Explicit constraint in global CLAUDE.md
2. **Hard enforcement** (future/backlog): Git hooks to block uncommitted rule changes

---

## Commit Governance

### Commit Cadence

```markdown
## Commit Standards
- Commit after completing each task (atomic commits)
- If task >30 min, commit at logical checkpoints
- Never batch more than 3 tasks per commit
- Before commit: lint, test, verify builds
```

### Commit Message Format

```
type(scope): TASK-XXX description
```

Examples:
- `feat(auth): TASK-005 implement login endpoint`
- `fix(api): TASK-012 handle null response`
- `chore(deps): TASK-003 update dependencies`

### Why Task-Level Commits

- **Crash recovery:** Know exactly which tasks completed (check git log)
- **Traceability:** Git history maps 1:1 to task list
- **Atomic rollback:** Revert single task if needed

---

## Plan Implementation Workflow

### Plan File Location

```
docs/plans/PLAN-[name].md
```

### Plan Workflow

1. **Create plan file** in `docs/plans/`
2. **Print summary** to screen
3. **Detailed breakdown** in the markdown file
4. **Execute phases** sequentially or in parallel (if isolated)
5. **Update task status** inline as completed

### Plan Structure

```markdown
---
type: "plan"
description: "User authentication implementation"
version: "1.0.0"
updated: "2026-01-02T14:30:00"
status: "in-progress"
---

# Plan: [Feature Name]

## Summary
[Brief description — printed to screen]

## Phase 1: [Domain] (e.g., Database)
- [ ] TASK-001: Description
- [ ] TASK-002: Description
- [x] TASK-003: Description (completed 2026-01-02, commit abc123)

## Phase 2: [Domain] (e.g., API)
- [ ] TASK-004: Description
- [ ] TASK-005: Description

## Notes
- [Gotchas discovered during implementation]
- [Decisions made mid-plan]
```

### Phase Guidelines

- **Domain-isolated:** Group by code area (database, API, frontend)
- **Size:** 5-10 tasks per phase maximum
- **Independent:** Phases should not have cross-dependencies when possible

### Parallelization

- **Use sub-agents** for isolated phases
- **Safe:** Phase 3 (database) while Phase 1 (frontend) runs
- **NOT safe:** Two agents editing `src/components/` simultaneously
- **Rule:** DO NOT parallelize tasks in overlapping code areas

### Task Completion

When completing a task:
1. Mark checkbox: `- [x] TASK-XXX: Description`
2. Add completion info: `(completed 2026-01-02, commit abc123)`
3. Commit with conventional message

---

## Prune Skill (Maintenance)

### Naming Convention

```
prune-memory-project-tier1
```

Future: `prune-memory-project-tier2` for Tier-2 memory.

### Prune Behavior

**Preserve (static sections):**
- Stack
- Commands
- Architecture
- Gotchas

**Prune (dynamic sections):**
- Completed tasks in "Current Focus"
- Old entries in "Recent Activity"
- Stale file references

**Target size:** 
- Global: ~35 lines
- Project: ~50 lines

### Trigger

Manual command for now. Future: hook or scheduled.

---

## File Templates

### Global CLAUDE.md (`~/.claude/CLAUDE.md`)

```yaml
---
# Core
type: "memory_global"
description: "Universal invariants and workflow patterns"
version: "1.0.0"
updated: "2026-01-02T14:30:00"

# Optional
scope: "global"
---
```

```markdown
# Global Context

<constraints>
- Never commit secrets, credentials, or API keys
- Never modify `.claude/rules/` without explicit human approval
- Confirm before destructive operations (delete, drop, overwrite)
- Commit after completing each task
</constraints>

## Commit Standards
- Commit after each task completion
- If task >30 min, commit at logical checkpoints
- Never batch more than 3 tasks per commit
- Format: `type(scope): TASK-XXX description`
- Before commit: lint, test, verify builds

## Plan Implementation
- Create plans in `docs/plans/PLAN-[name].md`
- Print summary to screen; detailed breakdown in file
- Phases: domain-isolated, 5-10 tasks max
- Parallelize isolated phases with sub-agents
- DO NOT parallelize tasks in same code area

## Communication
- Be concise — bullets over paragraphs
- Flag blockers immediately
- When uncertain, ask rather than assume
```

**~35 lines.**

### Project CLAUDE.md (`.claude/CLAUDE.md`)

```yaml
---
# Core
type: "memory_project"
description: "Project context and current working state"
version: "1.0.0"
updated: "2026-01-02T14:30:00"

# Optional
scope: "project"
---
```

```markdown
# [Project Name]

<!-- ====== STATIC SECTION (preserve on prune) ====== -->

## Stack
- Runtime: [e.g., Node 20]
- Framework: [e.g., Next.js 14]
- Database: [e.g., Supabase]

## Commands
- Dev: `[command]`
- Test: `[command]`
- Build: `[command]`
- Lint: `[command]`

## Architecture
- Source: `src/`
- Tests: `tests/`
- Plans: `docs/plans/`

## Gotchas
- [Project-specific pitfalls]

<!-- ====== DYNAMIC SECTION (prune regularly) ====== -->

## Current Focus
- Active plan: `docs/plans/PLAN-[name].md`
- Current phase: [Phase X]
- Current task: [TASK-XXX]

## Recent Activity
- Working in: [directories]
- Last commit: [sha] - [message]
```

**~40 lines.**

### Project Rule Template (`.claude/rules/*.md`)

```yaml
---
# Core
type: "rule_stack"
description: "Technology choices and framework-specific patterns"
version: "1.0.0"
updated: "2026-01-02T14:30:00"
---
```

```markdown
# Stack Rules

## Purpose
Technology-specific patterns for this project.

## Rules

### Framework
- [Framework-specific rules]

### Database
- [Database-specific rules]

### Testing
- [Testing conventions]
```

---

## Installation

### Global Setup

```bash
# Create directory
mkdir -p ~/.claude

# Create CLAUDE.md (copy template above)
vim ~/.claude/CLAUDE.md
```

### Project Setup

```bash
# In project root
mkdir -p .claude/rules
mkdir -p docs/plans

# Create project CLAUDE.md
vim .claude/CLAUDE.md

# Create rules as needed
vim .claude/rules/stack.md
```

---

## Validation

### Manual Checks
- [ ] Frontmatter has 4 core fields (type, description, version, updated)
- [ ] Line count ≤ 200
- [ ] Static/dynamic sections labeled (if applicable)
- [ ] Version incremented if meaning changed

### Automated (Future)
- Lint script for frontmatter validation
- Line count check
- Type vocabulary enforcement

---

## Backlog

### Deferred Items
- Global `~/.claude/rules/` directory (add when content exceeds single file)
- Hard enforcement for rules/ protection (git hooks)
- Conditional `paths:` loading (specific use case needed)
- Automated prune trigger (hook or scheduled)
- Validation tooling

### Open Questions
- Should tasks live in plan files or separate `tasks.md`? (Current: in plan files)
- Agent-derived rules staging mechanism?

---

## References

- Claude Code Memory Docs: https://code.claude.com/docs/en/memory
- Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices

---

## Review & Change History

**Current Version:** 2.0.0
**Review Status:** draft

### Changes Since Last Review (v1.0.0 → v2.0.0)
- Simplified frontmatter: 4 core fields (type, description, version, updated)
- Replaced `title` with `description` (filename is machine ID)
- Changed `updated` to ISO 8601 datetime format
- Removed global rules/ directory (content fits in single file)
- Added static/dynamic section markers with HTML comments
- Added `<constraints>` XML tags for priority signaling
- Added commit governance (task-level commits)
- Added plan implementation workflow (docs/plans/)
- Defined phase structure (domain-isolated, 5-10 tasks)
- Added parallelization guidance (sub-agents for isolated phases)
- Added prune skill naming convention (`prune-memory-project-tier1`)
- Clarified precedence model (all loaded; conflict = higher wins)
- Documented rules/ protection (honor system for now)
- Removed redundant fields: doc_id, title, status, owner, created, review_status
