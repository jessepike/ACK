---
type: "guide"
description: "Setup stage overview and artifact inventory"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# Stage 3: Setup (Environment + Workflow)

## Intent

Initialize everything needed for implementation. Bridge from "we know what to build" to "agents can execute."

## Process

1. Initialize repository
2. Pull/apply templates (Next.js, etc.)
3. Install dependencies
4. Configure tooling
5. Select and configure agents needed
6. Set up memory (CLAUDE.md, rules/)
7. Scaffold project structure
8. Validate alignment before proceeding

## Inputs

| Artifact | From |
|----------|------|
| Project Brief | Stage 1 |
| Architecture + derivatives | Stage 2 |
| Dependencies/requirements | Stage 2 |

## Outputs

| Artifact | Type | Description |
|----------|------|-------------|
| Scaffolded project | Deliverable | Files, folders, configs in place |
| .claude/ setup | Deliverable | Memory and rules configured |
| Agent harness | Deliverable | Tools, workflows, patterns ready |
| Environment config | Supporting | .env templates, MCP config |

## Exit Criteria

- Repository initialized
- All dependencies installed
- Context and memory configured
- Agent harness ready
- Validation checkpoint passed

## Artifacts in This Directory

- `environment.md` - Environment configuration notes
- `agents.md` - Agent selection and configuration
- `tooling.md` - Tooling decisions
- `checklist.md` - Setup validation checklist
