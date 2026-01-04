# Claude Code Memory Options & Recommended Architecture (2026-01-01)

## 0) Executive decision

**Recommended baseline (start now):**
1. **Claude Code native memory (CLAUDE.md + `.claude/rules/`)** as the Tier‑1 system of record for *stable* guidance: repo conventions, commands, architecture invariants, security gates, definitions, and “how we work.”
2. **Claude‑Mem** as Tier‑2 *session persistence* for Claude Code (tool-usage capture → compressed “observations” → searchable recall) to survive crashes/context resets.

**Recommended extension (optional, once Tier‑1/2 are stable):**
3. **Mem0** for *cross‑project* and *non‑dev* agent memory, if you want one memory substrate shared across a personal chief‑of‑staff agent and development agents. This requires you to design an integration boundary and governance (what gets written, what gets recalled, and when).

**Not recommended as a primary coding-memory solution:**
- **Claude Desktop Projects knowledge base**: valuable for design/planning and long-form context, but not ideal as your main “coding memory” because your coding loop lives in the IDE/Claude Code, not the desktop UI.

---

## 1) Your requirements mapped to capabilities

### 1.1 What you need (normalized)
- **Persistence across sessions**: survive agent crashes, IDE crashes, new chat/session resets.
- **Project + global memory**: per‑repo context plus cross‑repo learnings, preferences, and reusable patterns.
- **Low friction**: memory should be available inside the IDE/Claude Code workflow.
- **Curatable**: you need pruning, validity windows, and conflict resolution (prevent “memory drift” and stale rules).
- **Governable**: clear tiers of authority and precedence (what overrides what).

### 1.2 Memory types you’re actually dealing with
- **Instruction memory**: rules/guidelines/invariants (“always do X”, “never do Y”).
- **Reference memory**: facts about codebases, domains, decisions, APIs, constraints.
- **Episodic/session memory**: what happened recently (debugging timeline, prior attempts, commands run, outcomes).
- **Preference memory**: personal style, tool preferences, formatting, etc.

---

## 2) Tier‑1: Claude Code native memory (CLAUDE.md + rules)

Claude Code supports hierarchical memory files, including user-level and project-level, plus modular rule files under `.claude/rules/`. It also supports `@path` imports to split memory into topic-specific files.

### 2.1 What Tier‑1 is best at
- **Durable, curated “truth”**: conventions, architecture decisions, guardrails.
- **Deterministic precedence**: global → project → path-scoped rules.
- **Team-shareable**: check into git (except `CLAUDE.local.md`).

### 2.2 Practical structure to adopt
Use Tier‑1 as the stable corpus. Keep it small, explicit, and organized.

**Recommended repo layout**
```
./.claude/
  CLAUDE.md
  rules/
    00-principles.md
    10-style.md
    20-testing.md
    30-architecture.md
    40-security.md
    50-tooling.md
    frontend/react.md        # optional
    backend/api.md           # optional
```

**Recommended global layout (applies to all repos)**
```
~/.claude/
  CLAUDE.md
  rules/
    preferences.md
    workflows.md
    security-baseline.md
```

### 2.3 “instructions.md” and “constitution.md” in practice
You can absolutely implement these as:
- `.claude/rules/constitution.md` (stable principles and prohibitions)
- `.claude/rules/instructions.md` (execution conventions and workflow rules)

But the important part is **tiering + scoping**, not filenames. The `.claude/rules/` mechanism + optional `paths:` frontmatter is the lever that makes this usable at scale.

### 2.4 Known limitations
- It’s **not** a long-term episodic memory system; it’s curated instruction memory.
- Overgrowth kills it. If you dump logs and raw history into Tier‑1, it will degrade adherence and waste tokens.

---

## 3) Claude Desktop Projects knowledge base (planning memory)

Claude Projects allow you to upload documents and set project instructions. On paid plans, Projects can use a retrieval mode (“RAG mode”) as the knowledge base grows.

### 3.1 When it’s useful
- Product discovery, requirements, planning, architecture discussions
- Long documents you want Claude to reference without pasting repeatedly

### 3.2 Why it’s not your main coding memory
- It’s **not co-located with your coding loop**.
- It doesn’t automatically solve IDE/agent crash resets inside Claude Code.

Use it as a *planning and design workspace*, not the persistence layer for code execution.

---

## 4) Tier‑2 option A: Claude‑Mem (Claude Code plugin)

Claude‑Mem is designed specifically for the problem you described: **persistence across Claude Code sessions**. It captures tool usage and compresses it into “observations” that are later retrievable via MCP tools (search/timeline/get_observations).

### 4.1 What it is best at
- **Episodic memory** (what happened last time): debugging attempts, commands run, edits, outcomes.
- **Token efficiency**: retrieve a small index first, then fetch details only when needed.
- **IDE-native**: it’s built around Claude Code workflows.

### 4.2 Key operational risk
- It is an active OSS project; expect operational wrinkles (version churn, storage growth, occasional bugs).
- You must define **write filters** (what gets recorded) and **retention policies** to prevent runaway storage and stale recall.

---

## 5) Tier‑2 option B: Mem0 (universal memory layer)

Mem0 is a general-purpose memory system (hosted or self-hosted) designed to add memory to AI apps and agents. It supports multi-level memory concepts and has SDKs/APIs.

### 5.1 Where Mem0 fits for you
- **Cross-project / cross-agent memory**, including non-dev agents.
- A shared “personal + org” memory substrate if you want your chief‑of‑staff agent and coding agents to learn from the same pool.

### 5.2 What you’ll need to build (non-trivial)
Mem0 is not “Claude Code native.” You will need an integration pattern:
- A writer (what gets stored, schema/tags, redaction)
- A retriever (when to pull memories, how many, ranking)
- Governance (avoid poisoning your agents with stale or wrong memories)

If you’re trying to solve “IDE crash resets” first, Mem0 is usually **phase 2**, not phase 1.

---

## 6) Recommended target architecture

### 6.1 The simplest architecture that meets your needs
**Two-tier architecture:**

**Tier‑1 (Curated Rules / Truth)**
- Claude Code: `~/.claude/*` + per-repo `.claude/*`
- Small, audited, human-curated

**Tier‑2 (Episodic Session Memory)**
- Claude‑Mem local DB(s)
- Captures tool usage and compresses to searchable observations

This alone solves:
- “Agent/IDE crash set-back” (episodic recall)
- “Don’t lose context between sessions” (retrieve prior work quickly)

### 6.2 The scalable architecture (adds global cross‑project memory)
Add a **Global Memory Service** layer:

- **Global memory store**: Mem0 (self-hosted) or a similar memory DB
- **Project partitions**: repo_id / project_id as first-class tags
- **Adapters**:
  - Claude Code adapter (push/pull) – likely via MCP server(s) and conventions
  - Personal agent adapter (push/pull)

### 6.3 Precedence rules (non-negotiable)
1. **Human-curated rules override everything** (Tier‑1).
2. **Project rules override global preferences** (repo > user).
3. **Episodic memory never overrides invariants** (it can suggest, not dictate).
4. **Any memory item must carry metadata**: source, timestamp, scope, confidence, expiry.

---

## 7) Governance & curation plan (you will need this)

### 7.1 What gets written to Tier‑1
Only **stable** items:
- commands that are *actually correct*
- architectural invariants
- code style conventions
- security requirements
- “how we work” workflow gates

### 7.2 What gets written to Tier‑2
- debugging timelines
- attempted fixes and outcomes
- local environment gotchas
- “why this decision was made” (short form)

### 7.3 Retention and pruning (starter defaults)
- Tier‑1: manual edits + periodic review (weekly per active repo)
- Tier‑2: rolling retention (e.g., 30–90 days) + pin/upgrade mechanism:
  - “Promote to Tier‑1” for anything that proves stable and reusable
  - Auto-expire anything not referenced for N days

### 7.4 Drift prevention
- If Tier‑2 “observations” conflict with Tier‑1 rules, Tier‑1 wins.
- Require “decision log” entries for major changes (promote to Tier‑1 only with a decision record).

---

## 8) Recommended rollout (practical)

### Phase 1 (now): Make Tier‑1 real
- Standardize `.claude/` structure per repo.
- Add `constitution.md` + `instructions.md` as rule modules (path-scoped where appropriate).
- Keep it short; make it enforceable.

### Phase 2 (now): Add Claude‑Mem for persistence
- Install and run per repo.
- Define retention + storage location conventions.
- Create a “promote to Tier‑1” workflow (human decides).

### Phase 3 (later): Decide on Mem0
Proceed only if you need:
- shared memory across dev + personal agents, *and*
- you’re ready to implement governance (schemas, redaction, TTL, conflict handling).

---

## 9) Open decisions (you should make explicitly)
1. **Local-first vs hosted**: do you require offline/local-only memory for code projects?
2. **Security model**: what is allowed to be stored (secrets, customer data, credentials)?
3. **Cross-project scope**: what kinds of memories should propagate across repos (patterns vs facts)?
4. **Promotion workflow**: what is the gate to promote ephemeral memory into curated rules?

---

## 10) Sources (URLs)

```
https://code.claude.com/docs/en/memory
https://www.anthropic.com/engineering/claude-code-best-practices
https://support.anthropic.com/en/articles/9519177-how-can-i-create-and-manage-projects
https://github.com/thedotmack/claude-mem
https://github.com/mem0ai/mem0
https://docs.mem0.ai/platform/overview
```
