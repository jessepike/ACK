---
type: "artifact_registry"
description: "Complete inventory of primitives in the ACK registry"
version: "0.3.0"
updated: "2026-01-03T00:00:00"
---

# Agent Context Registry Inventory

Complete inventory of primitives in the ACK registry.

## Summary

| Primitive Type | Count | Status |
|----------------|-------|--------|
| Agents | 4 | Railway, Supabase, Next.js, GitHub |
| Skills | 4 | Need Anthropic format alignment |
| Tools | 4 | Complete |
| Commands | 7 | All active |
| Prompts | 6 | Complete |
| Policies | 0 | Not yet created |
| Domains | 4 | Railway, Supabase, Next.js, GitHub |

## Agents

| ID | Name | Domain | Status |
|----|------|--------|--------|
| agent-001 | railway-expert | Railway | ✅ Active |
| agent-002 | supabase-expert | Supabase | ✅ Active |
| agent-003 | nextjs-expert | Next.js | ✅ Active |
| agent-004 | github-expert | GitHub | ✅ Active |

**Backlog:**
- [ ] langchain-expert
- [ ] python-expert

## Skills

| ID | Name | Domain | Anthropic Format? |
|----|------|--------|-------------------|
| skill-001 | railway/SKILL.md | Railway | ⚠️ Needs alignment |
| skill-002 | supabase/SKILL.md | Supabase | ⚠️ Needs alignment |
| skill-003 | nextjs/SKILL.md | Next.js | ⚠️ Needs alignment |
| skill-004 | github-SKILL.md | GitHub | ✅ Has name/description |

**Action needed:** Add `name` and `description` to frontmatter per Anthropic standard.

**Backlog:**
- [ ] code-review (global)
- [ ] commit-standards (global)

## Tools

| ID | Name | Type | Domain |
|----|------|------|--------|
| tool-001 | railway.md | MCP + CLI | Railway |
| tool-002 | supabase.md | MCP | Supabase |
| tool-003 | nextjs-cli.md | CLI | Next.js |
| tool-004 | github.md | MCP + CLI | GitHub |

**Backlog:**
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
| cmd-008 | github-debug | GitHub | ✅ Active |

**Backlog:**
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

**Backlog:**
- [ ] code-review-policy.md — What must be reviewed
- [ ] commit-standards-policy.md — Commit message rules
- [ ] security-policy.md — Security requirements

## MCP Servers (Documented)

| Server | Status | Tier |
|--------|--------|------|
| Railway | ✅ Documented | Domain |
| Supabase | ✅ Documented | Domain |
| GitHub | ✅ Documented | Global |
| Context7 | ✅ In inventory | Global |
| Playwright | ✅ In inventory | Domain |
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

### GitHub (Complete)
- ✅ Agent: github-expert.md
- ✅ Skill: github-SKILL.md
- ✅ Tool: github.md
- ✅ Command: github-debug.md
- ⚠️ Summary: GITHUB.md (not yet created)

## Reference Docs

| Doc | Purpose | Status |
|-----|---------|--------|
| MCP_INVENTORY.md | MCP server catalog | ✅ Created |
| BUILTIN_COMMANDS_REFERENCE.md | Built-in vs custom | ✅ Created |
| SKILL_CREATION_GUIDE.md | How to create skills | ✅ Created |

## Priority Backlog

### High (Blocks usage)
1. [x] ~~GitHub domain package~~ ✅ Complete
2. [ ] Global MCP config (context7, github, claude-in-chrome)
3. [ ] Align skills to Anthropic format

### Medium (Improves quality)
4. [ ] Create first policies
5. [ ] Reorganize into structured hierarchy
6. [ ] LangChain domain package

### Low (Future)
7. [ ] Python domain package
8. [ ] TypeScript domain package
9. [ ] Project integration tooling

---

## Review & Change History

**Current Version:** 0.3.0
**Review Status:** draft

### Changes Since Last Review
- GitHub domain package now complete (agent, skill, tool, command)
- Removed deprecated review.md command
- Updated to ACK frontmatter schema
- Updated counts and status
