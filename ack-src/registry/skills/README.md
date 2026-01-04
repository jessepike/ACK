---
doc_id: "guide-001"
slug: "skill-creation-guide"
title: "Skill Creation Guide"
type: "research_note"
tier: "tier1"
status: "active"
authority: "binding"
version: "0.1.0"
review_status: "draft"
created: "2026-01-02"
updated: "2026-01-02"
owner: "human"
depends_on: []
---

# Skill Creation Guide

Captures learnings from building the agent-context-registry. Ensures consistency for future skill/agent/tool creation.

## Anthropic Skill Standard

Source: `/mnt/skills/examples/skill-creator/SKILL.md`

### Required Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/       - Executable code (Python/Bash)
    ├── references/    - Docs loaded into context as needed
    └── assets/        - Files used in output (templates, icons)
```

### Frontmatter (Anthropic Required)

```yaml
---
name: skill-name
description: >
  What the skill does AND when to trigger it.
  Include specific triggers/contexts.
  This is the PRIMARY triggering mechanism.
---
```

### Our AGS Overlay

We add governance fields for internal tracking:

```yaml
---
# Anthropic required
name: skill-name
description: What it does and when to use it

# AGS governance (our addition)
doc_id: "skill-XXX"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
owner: "human"
depends_on: []
---
```

## Core Principles

### 1. Context Window is a Public Good

> "Only add context Claude doesn't already have. Challenge each piece: Does Claude really need this?"

- Prefer concise examples over verbose explanations
- Keep SKILL.md under 500 lines
- Use progressive disclosure

### 2. Progressive Disclosure

Three-level loading:

1. **Metadata** (~100 words) — Always in context
2. **SKILL.md body** (<5k words) — When skill triggers
3. **Bundled resources** — As needed by Claude

### 3. Degrees of Freedom

| Freedom Level | When to Use | Format |
|---------------|-------------|--------|
| High | Multiple valid approaches | Text instructions |
| Medium | Preferred pattern exists | Pseudocode, params |
| Low | Fragile, consistency critical | Specific scripts |

### 4. What NOT to Include

Do NOT create:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

Only include what Claude needs to do the job.

## Skill Creation Workflow

### Step 1: Understand with Concrete Examples

- What functionality should it support?
- How would it be used?
- What triggers it?

### Step 2: Plan Reusable Contents

For each example, identify:
- Scripts that would be rewritten repeatedly
- References Claude needs (schemas, docs)
- Assets for output (templates, boilerplate)

### Step 3: Initialize

Use Anthropic's init script:
```bash
/mnt/skills/examples/skill-creator/scripts/init_skill.py <skill-name> --path <output-dir>
```

### Step 4: Edit

- Start with bundled resources (scripts, references, assets)
- Test scripts by running them
- Write SKILL.md with clear triggering description
- Use imperative/infinitive form

### Step 5: Package

```bash
/mnt/skills/examples/skill-creator/scripts/package_skill.py <path/to/skill>
```

Creates `.skill` file (zip with .skill extension).

### Step 6: Iterate

Test on real tasks, notice struggles, improve.

## Agent vs Skill vs Tool

| Primitive | Purpose | Structure |
|-----------|---------|-----------|
| **Agent** | Domain expert persona | Prompt defining expertise, approach |
| **Skill** | Procedural knowledge | SKILL.md + scripts/references/assets |
| **Tool** | External capability | MCP server or CLI spec |

**When to use which:**
- Agent: "Act as an expert in X"
- Skill: "Here's how to do X step-by-step"
- Tool: "Here's how to connect to X"

## Description Writing

The description is the PRIMARY trigger. Include:

1. What the skill does
2. Specific triggers/contexts
3. File types or domains it handles

**Example:**
> "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"

## Testing Checklist

- [ ] Frontmatter has name + description
- [ ] Description includes trigger conditions
- [ ] SKILL.md under 500 lines
- [ ] Scripts tested and working
- [ ] No unnecessary files (README, CHANGELOG)
- [ ] References split out if SKILL.md too long
- [ ] AGS fields added for governance

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation from Anthropic skill-creator analysis
