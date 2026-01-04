---
type: "guide"
description: "ACK project overview and navigation"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# ACK - Agent Context Kit

A meta-project that produces reusable templates, workflows, and orchestration patterns for AI-assisted software development.

## Quick Links

| Document | Purpose |
|----------|---------|
| [Intent](ack-intent.md) | North Star - why ACK exists |
| [Project Brief](ack-project-brief.md) | What we're building, how |

## Project Structure

```
/ack/
├── ack-intent.md               # North Star outcome document
├── ack-project-brief.md        # Project concept and approach
│
├── 1-discovery/                # Discovery stage artifacts
├── 2-design/                   # Design stage artifacts
├── 3-setup/                    # Setup stage artifacts
├── 4-implementation/           # Implementation planning artifacts
│
├── ack-src/                    # THE PRODUCT (what we're building)
│   ├── gov/                    # Artifact Governance System
│   ├── mem/                    # Memory Kit (Tier-1)
│   ├── registry/               # Agent Context Registry
│   ├── schemas/                # Frontmatter schema, etc.
│   ├── templates/              # What other projects copy
│   └── scripts/                # Setup and validation scripts
│
├── inbox/                      # Working area (cleanup in progress)
└── README.md                   # This file
```

## Stage Model

| Stage | Purpose | Output |
|-------|---------|--------|
| 1. Discovery | Validate concept | Project Brief |
| 2. Design | Define what to build | Architecture + derivatives |
| 3. Setup | Initialize everything | Configured project + agent harness |
| 4. Implementation | Plan execution | Plan + Tasks |

## For Other Projects

To use ACK in a new project:

```bash
# 1. Copy project structure
cp -r ~/code/ack/ack-src/templates/stages/* ./

# 2. Symlink to shared primitives
ln -s ~/code/ack/ack-src/registry ./.ack-registry

# 3. Run setup script
~/code/ack/ack-src/scripts/ack-init.sh
```

## Status

This project is actively being built using its own methodology (dogfooding).
