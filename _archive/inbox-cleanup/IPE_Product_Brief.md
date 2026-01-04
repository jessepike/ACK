# IPE Product Brief

---

## Problem Statement

AI-augmented solo developers lack a unified environment for pre-implementation planning. The IDE handles code execution, but critical upstream work—research, architecture decisions, context management, agent orchestration, tooling selection—happens in scattered CLIs, docs, and mental models. This fragmentation causes:

- Context loss between planning and implementation
- Inconsistent project scaffolding and documentation
- Manual agent/tool configuration per project
- No systematic handoff from planning to IDE

## Solution Overview

**IPE (Integrated Planning Environment)** - A planning layer that orchestrates AI-augmented development from concept to implementation-ready state. Output becomes IDE input.

## Core Capabilities

**5-Stage Workflow:**

1. **Discovery** - Concept definition and validation research
2. **Solution Design** - Stack, architecture, data model, context schema decisions
3. **Environment Setup** - Repo initialization, tooling installation, scaffolding
4. **Workflow Configuration** - Agent rules, dev workflow, operational playbook
5. **Implementation Planning** - Hierarchical execution plan (phases → milestones → gates → tasks)

**Key Features:**

- **Living Documentation** - All artifacts are version-controlled, curated, and evolve throughout lifecycle
- **Agent Orchestration Interface** - Slack-style chat for human + multi-agent collaboration
- **Context Architecture** - Structured artifact schemas with YAML frontmatter, consistent linking
- **Environment Manifest** - BOM tracking of all tooling, configs, dependencies
- **Change Management** - Locked implementation plans require formal change orders
- **Cross-Stage Maintenance** - Continuous artifact curation and value assessment

## Target User

Solo AI-augmented developers who:
- Build with AI coding tools (Claude Code, Cursor, etc.)
- Manage multiple projects with complex context requirements
- Need reproducible project scaffolding patterns
- Want systematic agent coordination across development phases

## Success Criteria

**Measurable Outcomes:**

- Reduce concept-to-implementation time by 40%
- Eliminate manual project setup steps (100% automated scaffolding)
- Zero context loss handoffs between planning and IDE
- Reusable patterns across projects (stack templates, agent configs)

**Qualitative Indicators:**

- Developers report confidence in technical decisions before coding begins
- Consistent documentation quality across all projects
- Reduced cognitive load managing agent coordination
- Clear audit trail of planning decisions and rationale

## Non-Goals (MVP Scope)

- **Not building:** IDE replacement, code execution environment, deployment pipeline
- **Not supporting:** Team collaboration features, real-time multi-user editing
- **Not handling:** Post-development operations (monitoring, incident response)
- **Not optimizing for:** Non-technical stakeholders, waterfall processes

## Assumptions & Constraints

**Assumptions:**
- Users have AI coding tools already configured (Claude API access, etc.)
- Projects are solo-developer owned (not enterprise team context)
- Markdown is acceptable format for planning artifacts
- Users understand git workflows and version control

**Constraints:**
- Must integrate with existing AI tooling (MCP servers, Claude Code)
- Must output in formats consumable by standard IDEs
- Must run on developer workstations (not cloud-first)
- Context windows limit artifact sizes

## Open Questions & Risks

**Technical:**
- How does IPE detect when to transition between stages automatically vs. requiring human approval?
- What's the mechanism for importing existing projects into IPE mid-lifecycle?
- How do we handle conflicting agent recommendations during planning?

**Product:**
- Do users need IPE to support multiple active projects simultaneously?
- Should artifact templates be extensible/customizable per user preference?
- How prescriptive should context schema be vs. allowing flexibility?

**Market:**
- Is solo developer TAM sufficient for standalone product, or does this need team features for viability?
- What's willingness-to-pay for planning tools vs. execution tools?

## Output Artifacts (Stage 1 Complete)

This brief represents the Discovery stage output. Next stage (Solution Design) will produce:
- stack.md (technology decisions)
- architecture.md (IPE system design)
- data-model.md (how artifacts, stages, and state are modeled)
- context-schema.md (artifact types and structures)

---

**Status:** Discovery complete, awaiting gate decision to proceed to Solution Design or prototype first.

**Created:** 2024-12-31  
**Version:** 1.0
