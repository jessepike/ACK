# Project Concept: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
---

## What Is It?

ACK (Agent Context Kit) is the translation layer between human intent and AI execution. It captures your ideas in structured, versioned artifacts that AI coding agents can actually consume—providing the context, guardrails, and governance that stateless agents can't maintain themselves.

The tool provides a 5-stage workflow: Discovery → Solution Design → Environment Setup → Workflow Configuration → Implementation Planning. Each stage produces versioned artifacts that serve as the single source of truth for your project. Critical documents are hashed and require formal change orders to modify. Drift detectors monitor for divergence between what was planned and what's being built—catching misalignment early before it compounds. An embedded chat interface lets you collaborate with AI agents who can read, validate, and update your planning documents while respecting governance boundaries.

What makes ACK different: AI coding agents are remarkably good at writing code and following instructions, but they lack persistent memory and drift without guardrails. The human becomes the bottleneck—the only one holding context, the only validator, the only brake on a system that moves faster than humans can absorb. ACK solves this by capturing clear human intent in structured artifacts, then providing the context injection, orchestration, and governance mechanisms that keep agents aligned. The planning isn't just for you—it's the executable specification that AI agents will operate within.


## Problem Being Solved

AI coding agents are powerful but stateless. They excel at generating code from instructions, but they don't remember previous sessions, don't track evolving decisions, and will confidently drift from your original intent without realizing it. The human developer becomes the sole keeper of context—manually re-explaining the project, catching misalignment, and course-correcting repeatedly.

Meanwhile, these agents work *fast*. They generate code faster than humans can review, absorb, and validate. Without structure, you're either slowing everything down with constant manual oversight or letting quality slip as drift compounds undetected. The asymmetry between agent execution speed and human comprehension speed is unsustainable.

**Key pain points:**

- **Context loss between sessions.** You spend 20 minutes re-explaining project context to AI agents every time you start working. Previous decisions, rejected alternatives, and rationale disappear into chat history. The agent has no "project brain" to query.

- **Agent drift without guardrails.** AI agents follow the instruction in front of them, not the broader intent behind it. Small deviations compound. By the time you notice the implementation has strayed, you're deep in refactoring.

- **No single source of truth.** Planning happens in scattered docs, chat transcripts, and mental models. When an agent asks "what's the architecture?" there's no canonical answer—just fragments you have to reassemble and explain.

- **Speed mismatch.** Agents can produce in minutes what takes humans hours to properly review. You can't maintain quality at AI velocity without systematic validation—and right now, you *are* the system.

- **Manual governance is exhausting.** You're the only validator. Every PR, every generated file needs human review to catch drift. There's no systematic way to check "does this still match what we planned?"

- **No handoff protocol.** When planning is "done," there's no structured export to implementation. Agents can't programmatically consume your intent—they just get whatever context you remember to paste.


## Core Features

### Structured Artifact System

All planning outputs follow consistent schemas with YAML frontmatter, typed sections, and machine-readable structure. Artifacts are version-controlled with full history. Critical documents can be locked, requiring formal change orders to modify. This isn't documentation for humans to read—it's specification for agents to execute within.

### Context Injection Engine

Agents receive relevant project context automatically based on what they're working on. No more copy-pasting background. The system maintains a persistent "project brain" that agents can query, ensuring continuity across sessions and preventing the re-explanation tax.

### Governance Layer

Drift detection monitors implementation against planning artifacts, flagging divergence early. Hash verification ensures document integrity. Change order workflows enforce intentional modifications to locked specs. MVP implements manual validation checkpoints; the vision is automated validator agents monitoring continuously.

### Stage-Based Workflow

Five stages guide projects from concept to implementation-ready: Discovery, Solution Design, Environment Setup, Workflow Configuration, and Implementation Planning. Each stage has defined artifacts, completion criteria, and gate reviews before progression. Structure prevents the "just start coding" trap.

### Agent Orchestration Interface

Slack-style chat panel purpose-built for planning work. Agents can read current artifacts, suggest edits, validate consistency, and update sections—all within governance boundaries. The interface is for planning collaboration, not general-purpose chat.


## Value Proposition

**Maintain velocity without sacrificing quality.** AI agents move fast. ACK provides the structure that lets you keep pace—systematic validation instead of exhaustive manual review, drift detection instead of hoping you catch mistakes, single source of truth instead of scattered context.

**Reduce the re-explanation tax to zero.** Every session starts with full context. Agents know the project history, the decisions made, the alternatives rejected. You stop being the sole keeper of institutional knowledge.

**Catch drift before it compounds.** Small misalignments early become expensive refactors later. Governance mechanisms flag divergence when it's cheap to fix, not after you've built three features on a flawed foundation.

**Translate intent into executable specification.** The gap between "what you want" and "what agents build" is a translation problem. ACK structures your intent in formats agents can consume, with guardrails that keep execution aligned.

**Build a reusable system, not one-off documents.** Artifact templates, workflow patterns, and governance rules carry across projects. Each project improves the system.


## Success Looks Like

**3 months:**
- ACK used to plan and build ACK itself (dogfooding complete)
- 3-6 additional projects actively using ACK, including complex/enterprise-class ones
- Workflow feels natural—I'm not fighting the tool
- Drift detection proving value: catching misalignments I would have missed
- Context re-explanation tax eliminated: sessions start productive immediately

**6 months:**
- Open sourced and public
- Community forming: developers using it, forking it, building upon it
- Patterns documented: which artifact structures work, which need refinement
- Governance layer battle-tested across diverse project types
- Feedback loop established with early adopters

**12 months:**
- ACK is my default workflow for any significant project
- Active community contributing templates, improvements, integrations
- Tool has paid for itself many times over in time saved and mistakes avoided
- Clear signal on whether commercial path makes sense (not a goal, but data in hand)


## Non-Goals

ACK is NOT:

- **An IDE or code editor.** ACK handles pre-implementation planning. Code execution stays in your existing tools (VS Code, Cursor, etc.). ACK's output *feeds* your IDE—it doesn't replace it.

- **Version control.** Git remains your source of truth for code. ACK manages artifact versioning for planning documents, but repo management stays with Git/GitHub.

- **Issue tracking or project management.** We'll build integrations with Linear, Jira, and GitHub Issues in the future, but ACK doesn't replace them. Task management happens in your existing tools.

- **A general-purpose AI chat interface.** The agent chat is purpose-built for planning artifacts—reading, validating, and updating structured documents. It's not a replacement for Claude or ChatGPT for general questions.

- **Everything at once.** ACK fills a specific gap: the translation layer between human intent and AI execution. We're not building an all-in-one platform. We're building the planning and governance layer that's missing.


---

## Notes & Questions

- [ ] Research: How does Cursor handle context injection? What can we learn?
- [ ] Decision: Should artifact templates be user-customizable in MVP or locked?
- [ ] Validate: Is "governance layer" the right term, or too enterprise-y?
- [ ] Explore: Could ACK patterns apply beyond software development?
