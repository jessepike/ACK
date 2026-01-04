# IPE Discovery Stage - Design Specification

---

**Version:** 1.0  
**Created:** 2024-12-31  
**Status:** Design Complete

---

## Overview

Discovery is Stage 1 of the IPE (Integrated Planning Environment) workflow. It transforms a raw concept into a validated, documented Project Brief Package ready for Solution Design.

**Purpose:** Concept definition, validation research, and scope determination

**Phases:**
- **1A: Concept Definition** - What is it, core features, value proposition
- **1B: Deep Research** - Market validation, gap analysis, feasibility assessment

**Output:** Project Brief Package (4 core artifacts + synthesis document)

---

## Core Artifacts

### Pre-Templated Structure

All artifacts are visible from Discovery start with status indicators:
- **Red text** = Not Started (empty)
- **Orange text** = In Progress (content exists, not complete)
- **Green text** = Complete (human marked)

```
Discovery
  concept.md [in progress] ← research.md
  research.md [empty]
  validation.md [empty]
  scope.md [empty]
  
Resources
  competitor-analysis.pdf
  market-report.md
```

### Artifact Templates

#### concept.md

```yaml
---
status: in-progress
stage: discovery
created: 2024-12-31 [Human]
updated: 2024-12-31 [Claude]
related: []
---

# Concept Definition

## What Is It?
<!-- One sentence elevator pitch -->

## Problem Being Solved
<!-- What pain point does this address? -->

## Core Features
<!-- 3-5 essential capabilities -->
- 
- 
- 

## Value Proposition
<!-- Why would someone use this? -->

## Target User
<!-- Who is this for? Be specific. -->

## Success Looks Like
<!-- How do you know this worked? -->

## Out of Scope (MVP)
<!-- What are we explicitly NOT doing? -->
```

#### research.md

```yaml
---
status: empty
stage: discovery
created: 2024-12-31 [Human]
updated: 2024-12-31 [Human]
related: [concept.md]
---

# Research

## Market Landscape
<!-- Existing solutions, competitors, alternatives -->

## Gap Analysis
<!-- What's missing? Where's the opportunity? -->

## Technical Feasibility
<!-- Can this be built? What are the constraints? -->

## Risk Factors
<!-- What could kill this idea? -->

## User Validation
<!-- Evidence this problem is real and worth solving -->

## Key Insights
<!-- What did we learn that changes our thinking? -->
```

#### validation.md

```yaml
---
status: empty
stage: discovery
created: 2024-12-31 [Human]
updated: 2024-12-31 [Human]
related: [concept.md, research.md]
---

# Validation

## Problem Validation
<!-- Is this problem real and worth solving? -->

## Solution Validation
<!-- Does our approach address the problem effectively? -->

## Market Validation
<!-- Is there demand? Who will pay? -->

## Technical Validation
<!-- Can we actually build this? -->

## Evidence
<!-- Data, interviews, experiments that support validation -->

## Invalidated Assumptions
<!-- What did we learn was wrong? -->
```

#### scope.md

```yaml
---
status: empty
stage: discovery
created: 2024-12-31 [Human]
updated: 2024-12-31 [Human]
related: [concept.md]
---

# Scope Definition

## In Scope - MVP
<!-- What must be included in first version -->

## Out of Scope - MVP
<!-- Explicitly excluded from first version -->

## Future Phases
<!-- Planned for later versions -->

## Constraints
<!-- Time, budget, technical, team limitations -->

## Success Criteria
<!-- How do we know MVP is successful? -->

## Assumptions
<!-- What must be true for this to work? -->
```

---

## Interface Design

### Layout Structure

**Top Bar:**
- Project name + stage tabs
- Active stage = user-selected color, others gray
- Stages: Discovery | Solution Design | Environment Setup | Workflow Config | Implementation

**Left Panel (300px):**
- File browser with artifact tree
- Status indicated by text color
- Cross-reference indicators (← →)
- Collapsible Resources section

**Main Content Area (60/40 split):**

**Left Column - Document Editor:**
- Markdown viewer/editor
- Progressive disclosure (collapsed sections)
- Section headers with expand arrows
- Preview: first 2-3 sentences when content exists
- Manual "Mark Complete" checkbox per section

**Right Column - Agent Chat:**
- Slack-style linear feed
- Multi-participant (humans + AI agents)
- @mention support for agents/people
- Command shortcuts (/, @)
- Agent mode selector (Planning/Fast/Passive)
- Minimalist design, subtle agent badges

**Bottom Footer (24px):**
- Status indicator
- Current activity
- Notification icons

### Color Scheme

**Base:** Dark theme (#1e1e1e to #252526)
**Accents:** Blue-gray for active states (#007acc)
**Borders:** Subtle dividers (#3e3e42)
**Status:**
- Green = Complete
- Orange = In Progress
- Red = Not Started
- Gray = Empty/inactive

---

## Workflow Mechanics

### MVP Workflow

1. User opens Discovery stage
2. Pre-templated artifacts visible (all red/empty)
3. User selects artifact (e.g., concept.md)
4. User expands section
5. User chats with agents for help/research
6. **Manual copy-paste** from chat to artifact sections
7. Section auto-saves on edit
8. User manually marks section complete (checkbox)
9. Repeat until all sections complete
10. User manually marks artifact as "Finalized"

### Status Progression

**Section Level:**
- Empty → In Progress → Complete (human marks)

**Artifact Level:**
- Draft (sections incomplete)
- Complete - Awaiting Finalization (all sections complete)
- Finalized (human explicitly approved, locked)

**Stage Level:**
- In Progress
- Ready for Review (all artifacts finalized)
- Agent Validation (running validation checks)
- Awaiting Gate Approval (human decision)
- Complete → unlocks Solution Design

### Agent Interaction Modes

**Planning Mode:**
- Deep research and analysis
- Verbose explanations
- Use for complex tasks

**Fast Mode:**
- Direct execution
- Minimal explanation
- Use for simple tasks

**Passive Mode:**
- Wait for explicit commands
- No proactive suggestions

---

## Multi-Agent Review Process

### Review Workflow

**Problem Solved:** Scattered feedback from multiple AI models is difficult to synthesize

**IPE Solution:**

1. Generate synthesis document (consolidates all 4 artifacts)
2. **Export for Review** → Creates review package with structured prompt
3. User takes to external agents (Gemini, ChatGPT, etc.)
4. **Import Review** → Paste feedback (auto-appends as appendix)
5. Repeat for multiple agents
6. View all reviews in single document
7. `/synthesize reviews` → AI consolidates feedback
8. `/synthesize final` OR manual edits → v1.0-final
9. Finalize → locks document

### Review Template

```markdown
# [Agent Name] Review - Discovery Synthesis

## Overall Assessment
[High-level evaluation: Strong/Adequate/Needs Work]

## Strengths
- [What works well]
- [Solid foundations]

## Gaps & Weaknesses
- [Missing elements]
- [Logical inconsistencies]
- [Unclear sections]

## Critical Risks
- [What could kill this idea]
- [Unaddressed challenges]

## Recommendations
- [Specific improvements]
- [Additional research needed]

## Confidence Level
[High/Medium/Low confidence in this assessment]
```

### Review Prompt (Provided by IPE)

```
You are reviewing a Discovery stage synthesis document for [PROJECT NAME]. 

Use the structured template below to provide comprehensive feedback.
Be critical and constructive. Identify gaps, risks, and opportunities.

Focus on:
- Logical consistency across sections
- Market/technical feasibility
- Scope clarity and boundaries
- Missing critical elements

[TEMPLATE STRUCTURE INSERTED]
```

### Synthesis Document Structure

```markdown
Discovery Synthesis Document (v1.0-draft)
├── Original Content (synthesized from all artifacts)
├── Appendix A: Claude Opus Review
├── Appendix B: Gemini Review  
├── Appendix C: ChatGPT Review
└── [After synthesis] → v1.0-final
```

---

## Governance & Version Control

### Finalization = Lock

When artifact is finalized:
- Becomes locked (read-only)
- Changes require formal change order
- Version bumps (v1.0 → v1.1)
- Audit trail maintained

### Change Order Process

```
Modified: concept.md (v1.0 → v1.1)
Reason: [User input required]
Files changed: 1
+ 3 lines
- 1 line

[Commit Change] [Cancel]
```

**Triggers:**
- Version bump with rationale
- Git-style commit message
- Updates dependent artifacts
- Maintains history for compliance

### Source Package Archive

```
📁 Discovery (Stage Complete) ✓
  📄 discovery-synthesis.md [v1.0-final]
  
  ⋮ Show Source Materials (hidden by default)
  
  When expanded:
  📁 Source Materials
    📄 concept.md [v1.0]
    📄 research.md [v1.0]
    📄 validation.md [v1.0]
    📄 scope.md [v1.0]
    
    📁 Review Trail
      📄 synthesis-draft.md [v1.0-draft]
      📄 claude-opus-review.md
      📄 gemini-review.md
      📄 chatgpt-review.md
      
  📁 Resources
    🔗 competitor-analysis.pdf
    🔗 market-report.md
```

**Purpose:**
- Retrospective source validation
- Access to rejected ideas
- Audit trail for governance
- Reference for change orders

---

## Settings & Configuration

### Agent Configuration

```
Settings > Agent Configuration

Default Agent: [Dropdown: Claude Sonnet 4.5]

Workflow-Specific Agents:
┌─────────────────────────────────────┐
│ Discovery Validation               │
│ Agent: [Claude Opus 4.1      ▼]   │
│ Mode:  [Planning            ▼]    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Research & Analysis                │
│ Agent: [Gemini 3 Flash      ▼]    │
│ Mode:  [Planning            ▼]    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Document Synthesis                 │
│ Agent: [Claude Sonnet 4.5   ▼]    │
│ Mode:  [Fast                ▼]    │
└─────────────────────────────────────┘

[+ Add Workflow Agent]
```

**Key Principle:** All agents are interchangeable. User selects best agent for each task.

### Agent Validation Configuration

```yaml
validation_rules:
  - check: gap_analysis
    description: "Identify gaps in logic/coverage"
    enabled: true
  
  - check: consistency_review
    description: "Detect conflicting statements across artifacts"
    enabled: true
  
  - check: completeness_check
    description: "Verify all critical elements present"
    enabled: true
  
  - check: quality_threshold
    description: "Assess overall quality standards"
    enabled: true
  
  # User can add custom validation rules
```

**Context:** Validation rules become context for reviewer agent

---

## Chat Commands

### Discovery-Specific Commands

- `/research [topic]` - Initiate research on specific topic
- `/validate [assumption]` - Test assumption or hypothesis
- `/synthesize reviews` - Consolidate all review appendices
- `/synthesize final` - Generate final synthesis document
- `/export review` - Package synthesis for external review
- `/add-to [artifact]` - Extract chat content to artifact (future)

### General Commands

- `@[agent-name]` - Direct message to specific agent
- `/` - Show command menu
- `#[artifact]` - Reference specific artifact in chat

---

## Stage Completion Checklist

```
Discovery Stage Status: Ready for Review

Artifacts:
✓ concept.md [Finalized]
✓ research.md [Finalized]
✓ validation.md [Finalized]
✓ scope.md [Finalized]
✓ discovery-synthesis.md [Generated]

[Run Agent Validation]
[Complete Discovery Stage]
```

**Agent Validation Checks:**
- Gaps in logic/coverage
- Conflicting statements across artifacts
- Missing critical elements
- Quality threshold met

**Human Gate Decision:**
- Review validation report
- Approve to proceed to Solution Design
- OR return to Discovery for refinement
- OR prototype to reduce uncertainty

---

## Cross-Cutting Concerns

### Living Documentation
- All artifacts evolve throughout lifecycle
- Human and AI can update
- Requires active curation and pruning
- Continuous value assessment

### Progressive Disclosure
- Sections collapsed by default
- Expand on-demand to reduce cognitive load
- First 2-3 sentences preview when content exists

### Cross-References
- Sidebar visual indicators (← →)
- Color-coded by status (green/orange/red)
- Related artifacts in YAML frontmatter

---

## Future Features (Backlog)

### Phase 2+ Enhancements

**Agent Automation:**
- Auto-suggest content as sections filled
- Proactive research assistance
- Smart content synthesis across artifacts

**Collaboration:**
- Invite co-workers to Discovery sessions
- User presence indicators (green = active)
- Subtle agent vs human badges
- Multi-user editing

**Advanced Workflows:**
- Agent direct-write with approval flow
- `/add-to [artifact]` command extracts chat content
- Smart extraction (agent identifies target section)

**Synthesis Automation:**
- Auto-generate synthesis when all artifacts finalized
- Agent prompt: "Ready to synthesize?"

**Canvas Editor:**
- Inline comments on sections
- @mention agents for section-specific edits
- Threaded feedback per section
- Similar to Anthropic Artifacts commenting

**Review Consolidation:**
- AI-assisted synthesis of review appendices
- Conflict resolution suggestions
- Automated feedback integration

### Ideas TBD (Needs Evaluation)

**Cross-Reference Options:**
- Document header link pills
- Inline link badges with `[[filename]]` syntax
- Dependency graph mini-map view
- Hover preview tooltips

**Section Completion Alternatives:**
- Auto-complete when content exists
- Minimum word count threshold
- Required sub-bullet completion
- AI quality assessment

**Content Preview Options:**
- Section headers only (no preview)
- Section headers + completion percentage
- Section headers + word count indicator
- Full section always visible (no collapse)

**Agent Mode Configuration:**
- Global mode (applies to all agents)
- Per-agent mode settings
- Context-aware mode switching

---

## Design Principles

**Core Themes:**
- **Minimalism** - Clean, professional, no clutter
- **Consistency** - Structured templates, repeatable patterns
- **Friction Reduction** - Smooth workflows, predictable behavior
- **Control** - Human always in charge of finalization
- **Flexibility** - Interchangeable agents, adaptable to user needs
- **Governance** - Audit trails, change control, source preservation

---

## Success Metrics (Discovery Stage)

**Quantitative:**
- Time from concept to finalized brief (target: 40% reduction)
- Number of iterations required
- Review cycle efficiency
- Artifact completeness at finalization

**Qualitative:**
- User confidence in moving to Solution Design
- Quality of documentation
- Clarity of scope and boundaries
- Reduced decision fatigue

---

## Next Steps

1. **Validate this specification** with target users
2. **Prototype key interactions** (artifact editing, chat interface)
3. **Move to Solution Design stage** to architect IPE technical solution
4. Define stack, data model, context schema for IPE itself

---

**End of Discovery Stage Specification**
