# Tier-1 Memory Kit

Starter templates for Claude Code's native memory system (CLAUDE.md + rules/).

## Quick Start

### Global Installation

```bash
cd tier1_kit
chmod +x install_global.sh
./install_global.sh
```

This installs:
- `~/.claude/CLAUDE.md` — Global entry point
- `~/.claude/rules/constitution.md` — Non-negotiable invariants
- `~/.claude/rules/preferences.md` — Personal style preferences
- `~/.claude/rules/workflows.md` — Process patterns

### Project Setup

```bash
# In your project root
mkdir -p .claude/rules
cp tier1_kit/project/CLAUDE.md .claude/
cp tier1_kit/project/rules/*.md .claude/rules/

# Customize for your project
# Edit .claude/CLAUDE.md with project info
# Edit rules files as needed
```

## Structure

```
tier1_kit/
├── global/
│   ├── CLAUDE.md           # Global entry point
│   └── rules/
│       ├── constitution.md # Security, safety, integrity
│       ├── preferences.md  # Code style, formatting
│       └── workflows.md    # Development process
├── project/
│   ├── CLAUDE.md           # Project template
│   └── rules/
│       ├── architecture.md # Project structure
│       ├── stack.md        # Technology rules
│       └── domain.md       # Business rules
└── install_global.sh       # Installation script
```

## Customization

All files use AGS-aligned YAML frontmatter. Update these fields:
- `version` — Increment when meaning changes
- `updated` — Set to current date
- `status` — draft | active | deprecated

Keep each file under 200 lines (hard limit).

## Specification

See `TIER1_KIT_SPEC.md` for complete architecture and governance rules.

## Related

- [Claude Code Memory Docs](https://code.claude.com/docs/en/memory)
- AGS Templates: `~/code/tools/gov/ags_template_v1.0.0/`
