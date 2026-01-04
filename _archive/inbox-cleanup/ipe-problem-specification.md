# IPE Problem Specification
## The Pain of AI-Augmented Development (Solution-Agnostic)

**Date:** 2025-01-01  
**Author:** Jess Pike  
**Purpose:** Define the problem clearly before proposing solutions

---

## The Shift

Software development is undergoing a fundamental transition:

**Yesterday:** Humans write code. IDE is the primary workspace. AI assists.  
**Tomorrow:** Humans direct AI agents. Agents write code. Humans validate and steer.

The tools haven't caught up. Current IDEs—even "AI-native" ones—are built for yesterday's model: a human typing code with AI helping. But the work is shifting from *coding* to *context engineering, intent translation, and governance*.

This isn't about making coding faster. It's about a new kind of work that doesn't have proper tooling yet.

---

## The Core Problem

**AI coding agents are powerful but unreliable at staying aligned.**

They don't remember. They don't follow instructions consistently. They drift from intent without anyone noticing. The human becomes:
- The only source of truth
- The only enforcer of intent
- The only persistent memory
- The only validator

**That's unsustainable at AI speed.**

Agents can produce in minutes what takes hours to review. You can't maintain quality at that velocity when you're the entire governance system.

---

## Symptoms

### 1. Instruction Following is Inconsistent

Agents follow instructions about 60-70% of the time. Tell them to do three things, they might do one. Sometimes none. Sometimes all three. It's unpredictable.

**What this costs:**
- Constant correction and re-prompting
- Repeated explanations of the same constraints
- Wasted cycles on work that has to be redone
- Erosion of trust in the output

### 2. No Persistent Memory

Every session starts from zero. The agent doesn't remember:
- Previous decisions and why they were made
- Rejected alternatives
- Project context and constraints
- Your preferences and patterns

**What this costs:**
- 10-20 minutes of re-explanation at session start
- Context loss between sessions
- Decisions get relitigated because rationale wasn't preserved
- You become the sole keeper of project knowledge

### 3. Context is Scattered

Planning happens across multiple disconnected tools:
- Claude Desktop for some conversations
- ChatGPT for others
- Gemini through browser
- Apple Notes for quick captures
- Markdown files in repos
- Chat history that's unsearchable

**What this costs:**
- Can't find previous decisions
- Duplicate work because you forgot what was already done
- No single source of truth
- Context reassembly before every work session

### 4. Drift Happens Undetected

Agents follow the instruction in front of them, not the broader intent behind it. Small deviations compound. By the time you notice:
- The architecture has shifted from what was planned
- Features were implemented differently than specified
- Assumptions were made that contradict earlier decisions

**What this costs:**
- Expensive refactoring
- Technical debt accumulation
- Loss of coherence in the codebase
- "How did we get here?" moments

### 5. No Prompt Versioning

Prompts and instructions evolve, but there's no system to track:
- Which version of a prompt worked best
- What changed between iterations
- Why certain approaches were abandoned

**What this costs:**
- Reinventing prompts that worked before
- No learning accumulation
- Can't reproduce good results reliably

### 6. Manual Governance Doesn't Scale

You're the only validator. Every output needs human review to catch:
- Drift from intent
- Quality issues
- Instruction violations
- Architectural misalignment

**What this costs:**
- Bottleneck on all progress
- Exhaustion from constant vigilance
- Things slip through because you can't review everything
- Velocity limited by human attention, not AI capability

### 7. Environment Configuration is Fragmented

The AI development environment itself is scattered across:
- Multiple agents (Claude, GPT-4, Gemini, specialized models)
- Skills and capabilities per agent
- MCP servers and tools
- IDE plugins and extensions
- Memory systems (Claude memory, mem0, custom solutions)
- Agent configuration files (.cursorrules, CLAUDE.md, system prompts)
- Traditional dependencies (npm, pip, cargo, etc.)
- Workflows and methodologies

**What this costs:**
- Every project starts with manual tool selection and setup
- No reproducible "environment manifest" for AI-augmented projects
- Configuration scattered across multiple systems
- Can't easily say "clone this project's AI setup for a new project"
- Decisions about tooling aren't captured—just the results

### 8. No Decision Framework for Tooling

When starting a project, you need to decide:
- Which agents to use and for what tasks
- Which tools/plugins to enable
- What memory systems to set up
- How to configure each component
- What workflows to follow

There's no structured way to make these decisions or capture them for future reference.

**What this costs:**
- Reinventing the wheel on every project
- Inconsistent tooling choices
- No learning accumulation about what works
- Can't share or replicate successful configurations

---

## The Fundamental Tension

**AI agents are fast. Humans are thorough. There's no bridge.**

You need:
- AI-speed execution
- Human-quality governance

Without tooling, you get one or the other:
- Move fast → quality suffers, drift accumulates
- Stay thorough → velocity tanks, AI advantage disappears

---

## What's Needed (Capabilities, Not Solutions)

### Context Engineering
- Structured way to capture intent that agents can consume
- Not prose documentation—machine-readable specifications
- Persistent across sessions and tools

### Memory Layer  
- Project-level persistent memory
- Queryable by agents and humans
- Survives session boundaries
- Tracks decisions, rationale, constraints

### Automatic Context Injection
- Agents receive relevant context without manual paste
- Right context for the task at hand
- No re-explanation tax

### Drift Detection (Automated)
- System detects when implementation diverges from intent
- Flags issues for human review
- Catches drift before it compounds
- Not manual comparison—that doesn't scale

### Lightweight Checkpoints
- Simple "is this done?" validation
- Not formal gates—just clarity on status
- Easy to mark progress without overhead

### Version History
- Track how artifacts evolve
- See what changed and when
- Not formal change orders—just history

### Environment Manifest
- Declare what agents, tools, plugins, skills a project needs
- Reproducible setup—"initialize project with this configuration"
- Capture tooling decisions alongside the project
- Reusable templates for similar projects

### Decision Scaffolding
- Structured process for "what do I need for this project?"
- Guided selection of agents, tools, workflows
- Capture rationale for choices
- Learn from previous project setups

### Minimal Friction
- Reduces overhead, doesn't add it
- Fits into existing workflow
- Doesn't require context switching to another app
- Simple over feature-rich

---

## What It's NOT About

- **Not about better documentation.** Docs are passive. This is about active enforcement.
- **Not about project management.** Jira/Linear handle tasks. This is about intent and alignment.
- **Not about IDE features.** IDEs are for coding. This is for directing.
- **Not about team collaboration.** This is solo developer scale first.
- **Not about building a product for market.** This is about solving a personal, real problem.

---

## The Bet

The hypothesis: **80% of software development work is shifting from the IDE to a planning/governance layer.**

If true, the tooling gap is massive. Current tools are:
- IDEs with AI bolted on (still editor-centric)
- Chat interfaces (no structure, no memory)
- Documentation tools (passive, not enforced)
- Workarounds (instructions.md, .cursorrules) that work 60-70% of the time

None of them are built for the model where humans direct and AI executes.

---

## Success Criteria

Whatever solution emerges should achieve:

1. **Agent instruction compliance goes from 60-70% to 90%+**
2. **Context re-explanation drops from 20 min/session to near zero**
3. **Drift is caught automatically before it compounds**
4. **Memory persists across sessions and tools**
5. **Overhead is reduced, not increased**
6. **Can be used immediately on real projects**

---

## Open Questions

1. Where should this capability live? (Separate tool? IDE plugin? Repo-based?)
2. How lightweight can drift detection be while still being useful?
3. What's the minimum structure that provides value?
4. How do you make governance feel like leverage, not bureaucracy?
5. What exists today that partially solves this? What's missing?

---

## Next Steps

1. Research: How are others attempting to solve pieces of this?
2. Brainstorm: 2-3 solution approaches at different weight classes
3. Evaluate: Which approach best fits the actual need?
4. Build: Start with the lightest thing that could work

---

**This document defines the problem. Solutions come next.**
