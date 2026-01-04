---
type: artifact_registry
description: "Agent Context Registry Inventory"
version: 0.2.0
updated: 2026-01-02
status: active
depends_on: []
doc_id: inv-001
slug: registry-inventory
title: "Agent Context Registry Inventory"
tier: tier1
authority: binding
review_status: draft
created: 2026-01-02
owner: human
---

# Agent Context Registry Inventory

Complete inventory of primitives in the agent-context-registry.

## Summary

| Primitive Type | Count | Status |
|----------------|-------|--------|
| Agents | 3 | Complete for 3 domains |
| Skills | 3 | Need Anthropic format alignment |
| Tools | 3 | Complete |
| Commands | 6 | 1 deprecated |
| Prompts | 6 | Complete |
| Policies | 0 | Not yet created |
| Domains | 3 | Railway, Supabase, Next.js |

## Agents

| ID | Name | Domain | Status |
|----|------|--------|--------|
| agent-001 | railway-expert | Railway | ✅ Active |
| agent-002 | supabase-expert | Supabase | ✅ Active |
| agent-003 | nextjs-expert | Next.js | ✅ Active |

**Missing:**
- [ ] github-expert
- [ ] langchain-expert
- [ ] python-expert

## Skills

| ID | Name | Domain | Anthropic Format? |
|----|------|--------|-------------------|
| skill-001 | railway/SKILL.md | Railway | ⚠️ Needs alignment |
| skill-002 | supabase/SKILL.md | Supabase | ⚠️ Needs alignment |
| skill-003 | nextjs/SKILL.md | Next.js | ⚠️ Needs alignment |

**Action needed:** Add `name` and `description` to frontmatter per Anthropic standard.

**Missing:**
- [ ] github/SKILL.md
- [ ] code-review (global)
- [ ] commit-standards (global)

## Tools

| ID | Name | Type | Domain |
|----|------|------|--------|
| tool-001 | railway.md | MCP + CLI | Railway |
| tool-002 | supabase.md | MCP | Supabase |
| tool-003 | nextjs-cli.md | CLI | Next.js |

**Missing:**
- [ ] github.md (MCP)
- [ ] context7.md (MCP) — global
- [ ] claude-in-chrome.md (MCP) — global
- [ ] sequential-thinking.md — global

## Commands

| ID | Name | Domain | Status |
|----|------|--------|--------|
| cmd-001 | railway-debug | Railway | ✅ Active |
| cmd-002 | supabase-debug | Supabase | ✅ Active |
| cmd-003 | nextjs-debug | Next.js | ✅ Active |
| cmd-004 | commit | Git (global) | ✅ Active |
| cmd-005 | pr | Git (global) | ✅ Active |
| cmd-006 | branch | Git (global) | ✅ Active |
| cmd-007 | review | — | ⚠️ Deprecated (use built-in) |

**Missing:**
- [ ] github-pr (GitHub-specific)
- [ ] github-issue

## Prompts

| ID | Name | Purpose |
|----|------|---------|
| prompt-001 | commit-message | Conventional commit format |
| prompt-002 | pr-description | PR template |
| prompt-003 | code-review | Review checklist |
| prompt-004 | error-diagnosis | Debug template |
| prompt-005 | branch-name | Branch naming |
| prompt-006 | documentation | Doc template |

## Policies

None created yet.

**Planned:**
- [ ] code-review-policy.md — What must be reviewed
- [ ] commit-standards-policy.md — Commit message rules
- [ ] security-policy.md — Security requirements

## MCP Servers (Documented)

| Server | Status | Tier |
|--------|--------|------|
| Railway | ✅ Documented | Domain |
| Supabase | ✅ Documented | Domain |
| Context7 | ✅ In inventory | Global |
| Playwright | ✅ In inventory | Domain |
| GitHub | ✅ In inventory | Global |
| Claude in Chrome | 📝 Needs doc | Global |
| Sequential Thinking | 📝 Needs doc | Global |

## Domain Packages

### Railway (Complete)
- ✅ Agent: railway-expert.md
- ✅ Skill: railway/SKILL.md
- ✅ Tool: railway.md
- ✅ Command: railway-debug.md
- ✅ Summary: RAILWAY.md

### Supabase (Complete)
- ✅ Agent: supabase-expert.md
- ✅ Skill: supabase/SKILL.md
- ✅ Tool: supabase.md
- ✅ Command: supabase-debug.md
- ✅ Summary: SUPABASE.md

### Next.js (Complete)
- ✅ Agent: nextjs-expert.md
- ✅ Skill: nextjs/SKILL.md
- ✅ Tool: nextjs-cli.md
- ✅ Command: nextjs-debug.md
- ✅ Summary: NEXTJS.md

### GitHub (Missing)
- ❌ Agent: github-expert.md
- ❌ Skill: github/SKILL.md
- ❌ Tool: github.md
- ❌ Commands: github-pr.md, github-issue.md
- ❌ Summary: GITHUB.md

## Reference Docs

| Doc | Purpose | Status |
|-----|---------|--------|
| PRIMITIVES.md | Explains 6 types | ✅ Created |
| MCP_INVENTORY.md | MCP server catalog | ✅ Created |
| BUILTIN_COMMANDS_REFERENCE.md | Built-in vs custom | ✅ Created |
| SKILL_CREATION_GUIDE.md | How to create skills | ✅ Created |
| HIERARCHY_TIERS.md | Global/Domain/Project | ✅ Created |

## Templates

| Template | Purpose |
|----------|---------|
| mcp-base.json | Base MCP config |
| PROJECT_INTEGRATION.md | How to integrate |

## Priority Backlog

### High (Blocks usage)
1. [ ] GitHub domain package (every project uses git)
2. [ ] Global MCP config (context7, github, claude-in-chrome)
3. [ ] Align skills to Anthropic format

### Medium (Improves quality)
4. [ ] Create first policies
5. [ ] Reorganize into global/domains structure
6. [ ] LangChain domain package

### Low (Future)
7. [ ] Python domain package
8. [ ] TypeScript domain package
9. [ ] Project integration tooling

---

## Review & Change History

**Current Version:** 0.2.0
**Review Status:** draft

### Changes Since Last Review
- Added hierarchy documentation
- Added skill creation guide
- Identified Anthropic format gap
