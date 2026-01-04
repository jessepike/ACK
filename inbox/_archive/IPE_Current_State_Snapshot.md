# IPE Current State Snapshot
## Control Tower View

**Generated:** 2026-01-02
**Purpose:** Macro coordination across all workstreams
**Sync Frequency:** Update when workstreams report significant progress

---

## 1. The Problem (Unchanged)

AI-augmented development suffers from three core failures:

| Problem | Impact | Current Workarounds |
|---------|--------|---------------------|
| **Context Loss** | Re-explanation tax every session; agents lose project understanding | Manual session dumps to markdown; Claude Projects; scattered docs |
| **Agent Drift** | Output diverges from intent; detected too late | Human code review; tests as safety net; post-hoc linting |
| **Manual Governance** | Verification can't scale at AI generation speed | Hope; careful prompting; expensive human review |

**Research Validation:** All four deep research reports (Gemini, Claude, ChatGPT, Gemini Pro) confirm these as the defining challenges of late 2025. No one has solved them.

**Key Insight:** "Context Engineering" has replaced prompt engineering as the primary leverage point. The discipline now is structuring information for AI consumption, not crafting clever prompts.

---

## 2. The Pivot

### BEFORE: Standalone IPE Application
- **Platform:** Next.js + Supabase + Tiptap editor
- **Approach:** Build a separate planning tool; output feeds into IDE
- **Complexity:** Full-stack app development; database schema; UI components
- **Timeline:** Months of building before using

### AFTER: IDE-Integrated Workflow System
- **Platform:** Anti-Gravity + Zed (existing IDEs)
- **Approach:** Structured folder hierarchies + context files + lightweight scripts
- **Complexity:** Markdown artifacts + validation scripts + memory hierarchy
- **Timeline:** Iterative; usable as we build

### What Changed
| Aspect | Before | After |
|--------|--------|-------|
| Memory Layer | App database | CLAUDE.md hierarchy + claude-mem |
| Governance | In-app validation UI | Git hooks + CLI validation scripts |
| Artifacts | Database records with Tiptap | Structured markdown + YAML frontmatter |
| Agent Coordination | App chat interface | IDE-native + MCP servers |
| Delivery | Monolithic app launch | Incremental capability building |

### What Stayed the Same
- The 5-stage workflow model (Discovery → Design → Environment → Workflow → Implementation)
- Artifact-as-governance philosophy
- Spec-driven development approach
- Multi-agent orchestration patterns
- The core problems being solved

---

## 3. Current Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONTROL TOWER (This Session)                │
│         Macro coordination, dependency tracking, decisions      │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│  AGS Session  │       │ Memory Session│       │Registry Session│
│  (Governance) │       │ (Two-Tier)    │       │(Agents/Skills) │
└───────────────┘       └───────────────┘       └───────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │   Claude Registry     │
                    │ ~/code/tools/         │
                    │   claude-registry/    │
                    └───────────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
        Projects            Projects            Projects
        (symlinks)          (symlinks)          (symlinks)
```

---

## 4. Active Workstreams

### 4.1 AGS (Artifact Governance System)
**Session:** [Governance critical review](https://claude.ai/chat/f923247c-9e13-4894-bc39-4e76ec53da6b)
**Status:** Working validation, needs CLI fixes

**Completed:**
- Frontmatter schema specification
- Controlled vocabularies (type, tier, status, authority enums)
- Artifact registry structure
- ADR (Architecture Decision Record) templates
- Validation scripts with enum checking
- Drift detection capability (conceptual)
- Git-based enforcement hooks
- Emergency bypass protocols
- Adoption guides

**In Progress:**
- CLI flag implementation wiring
- Dead code cleanup in drift detection
- Missing imports preventing execution

**Blocking Issues:**
- Core validation functions not executing due to import issues
- CLI flags defined but not connected to logic

**Integration Points:**
- Needs alignment with Claude Registry frontmatter
- Governs artifacts produced by all other workstreams

---

### 4.2 Two-Tier Memory System
**Session:** [Two-tier memory system](https://claude.ai/chat/56f2f7fc-df4c-466b-8c04-f971d8dc10b4)
**Status:** Design phase, architecture defined

**Completed:**
- Tier-1/Tier-2 conceptual split defined
- Initial tier1_kit structure created
- Global and project-level CLAUDE.md templates
- Rules directory concept

**Architecture:**
```
Tier-1: Native Claude Code Memory
├── ~/.claude/CLAUDE.md (global)
├── ~/.claude/rules/ (global rules)
├── project/.claude/CLAUDE.md (project)
├── project/.claude/rules/ (project rules)
└── project/subdir/CLAUDE.md (local)

Tier-2: claude-mem (Cross-Session State)
├── Development database
└── Personal chief-of-staff database
```

**Open Design Questions:**
- Content taxonomy: what goes where in hierarchy?
- Rules granularity: one rule per file vs. grouped?
- Agent write permissions: can agents modify CLAUDE.md?
- Import strategies: how does lower level pull from higher?
- Cross-project learning: how do patterns propagate?
- Token budgets per level

**Blocking Issues:**
- Need content taxonomy decision before implementation
- Rules organization pattern not finalized

**Integration Points:**
- Memory content needs AGS governance
- Registry agents/skills need memory hierarchy placement

---

### 4.3 Claude Registry
**Session:** [AI dev workflow infrastructure](https://claude.ai/chat/24ce7334-c87e-480b-8412-3107fccc9169)
**Status:** Structure complete, needs inventory expansion

**Completed:**
- Registry location: `~/code/tools/claude-registry`
- Six primitive types defined:
  - **Agents:** Domain experts (Railway, Supabase, Next.js)
  - **Skills:** Procedural knowledge documents
  - **Tools:** MCP server specs, CLI specifications
  - **Commands:** Slash-triggered workflows
  - **Prompts:** Reusable templates
  - **Policies:** Constraint rules
- Complete domain packages: Railway, Supabase, Next.js
- Symlink-based durability model

**In Progress:**
- MCP server inventory (many available, need cataloging)
- AGS frontmatter retrofit on all registry files
- Overlap analysis with built-in Claude Code functionality

**Blocking Issues:**
- Need MCP server complete inventory
- AGS frontmatter not yet applied to registry files

**Integration Points:**
- Registry primitives need AGS-compliant frontmatter
- Agents need to know memory hierarchy for state persistence

---

## 5. Backlog & Future Ideas

### 5.1 High Priority (Enable Current Work)

| Item | Source | Why Important |
|------|--------|---------------|
| MCP server complete inventory | Registry session | Enables tool integration; prevents reinventing |
| AGS frontmatter for registry | Registry + AGS sessions | Consistency across all artifacts |
| Content taxonomy for Tier-1 | Memory session | Unblocks memory implementation |
| CLI wiring fixes for AGS | AGS session | Enables governance enforcement |

### 5.2 Medium Priority (Near-Term Capability)

| Item | Source | Description |
|------|--------|-------------|
| Drift detection real-time | AGS session | "Linter for Logic" - catch drift during generation |
| Cross-project learning | Memory session | Patterns propagate from project to global |
| Agent specialization | Registry session | More domain packages beyond Rail/Supa/Next |
| Validation as Git hook | AGS session | Block commits that violate governance |

### 5.3 Lower Priority (Future Exploration)

| Item | Source | Notes |
|------|--------|-------|
| AGENTS.md adoption | Research synthesis | Vendor-neutral standard; may replace custom format |
| Mem0 integration | Research synthesis | External memory layer; evaluate against claude-mem |
| Multi-agent orchestration | Research synthesis | BMAD patterns for specialized agents per phase |
| Manager View pattern | Research synthesis | Google Antigravity's approach to agent direction |
| Spec Kit integration | Research synthesis | GitHub's spec-driven workflow toolkit |

### 5.4 Deferred Ideas (Captured for Later)

| Item | Original Context | Why Deferred |
|------|------------------|--------------|
| Next.js app scaffolding | Original IPE app | Pivot to IDE-integrated approach |
| Tiptap editor integration | Original IPE app | Not building standalone editor |
| Supabase database schema | Original IPE app | Memory now in CLAUDE.md + claude-mem |
| In-app chat interface | Original IPE app | Using IDE-native agent interfaces |
| Stage transition automation | Stage 4 spec | Too complex for initial implementation |

---

## 6. Macro Workflow Framework

### 6.1 The Five Stages (Retained from Original)

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: DISCOVERY                                              │
│ What are we building? Why? For whom?                            │
│ Artifacts: concept.md, research.md, validation.md, scope.md     │
├─────────────────────────────────────────────────────────────────┤
│ STAGE 2: SOLUTION DESIGN                                        │
│ How will we build it? What tech? What architecture?             │
│ Artifacts: stack.md, architecture.md, data-model.md, context.md │
├─────────────────────────────────────────────────────────────────┤
│ STAGE 3: ENVIRONMENT SETUP                                      │
│ Initialize repo, tooling, dependencies, scaffolding             │
│ Artifacts: repo-init.md, dependencies.md, scaffolding.md        │
├─────────────────────────────────────────────────────────────────┤
│ STAGE 4: WORKFLOW CONFIGURATION                                 │
│ Agent rules, dev workflow, operational playbook                 │
│ Artifacts: agent-rules.md, dev-workflow.md, operations.md       │
├─────────────────────────────────────────────────────────────────┤
│ STAGE 5: IMPLEMENTATION PLANNING                                │
│ Hierarchical execution: phases → milestones → gates → tasks     │
│ Artifacts: phases.md, milestones.md, tasks.md                   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 First Principles Approach Per Stage

Each stage needs:

| Element | Description | Current State |
|---------|-------------|---------------|
| **Problem Definition** | What problem does this stage solve? | Defined in original specs |
| **Primitives** | Atomic units that compose this stage | Partially identified |
| **Inputs** | What does this stage need to begin? | Implicit in stage flow |
| **Outputs** | What artifacts does this stage produce? | Defined per stage |
| **Validation Criteria** | How do we know this stage is complete? | Needs definition |
| **Automation Level** | What's manual vs. automated? | Needs definition |
| **Agent Role** | What can agents do here? | Needs definition |

### 6.3 The Wrapper: Consistency Requirements

For the workflow to hold together, each stage must:

1. **Governance Compliance**
   - All artifacts have AGS-compliant frontmatter
   - Changes tracked in decision logs
   - Drift detection active

2. **Memory Integration**
   - Stage context available in CLAUDE.md
   - Progress persists across sessions
   - Cross-stage references maintained

3. **Validation Gates**
   - Entry criteria: what must exist to start?
   - Exit criteria: what must be complete to finish?
   - Automated checks where possible

4. **Agent Boundaries**
   - What agents can modify
   - What requires human approval
   - How to request human decision

---

## 7. Integration Dependency Map

```
                    ┌─────────────┐
                    │    AGS      │
                    │ (Governance)│
                    └──────┬──────┘
                           │ governs
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │   Memory    │ │  Registry   │ │  Workflow   │
    │  (Two-Tier) │ │  (Agents)   │ │  (Stages)   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    uses/references
                           │
                    ┌──────▼──────┐
                    │   Projects  │
                    │ (Your Work) │
                    └─────────────┘
```

**Critical Path:**
1. AGS must work first (validates everything else)
2. Memory hierarchy needs AGS compliance
3. Registry needs AGS frontmatter
4. Workflow stages use all three

---

## 8. Recommended Next Steps

### Immediate (Unblock Current Work)

1. **Fix AGS CLI wiring** - Without working validation, nothing is enforced
2. **Decide content taxonomy** - Unblocks Tier-1 memory implementation
3. **Apply AGS frontmatter to registry** - Consistency across systems

### Short-Term (Build Foundation)

4. **Complete MCP server inventory** - Know what tools exist
5. **Implement Tier-1 memory kit** - Enable persistent context
6. **Define stage validation criteria** - Know when stages are "done"

### Medium-Term (Enable Workflow)

7. **Wire Git hooks for governance** - Automate enforcement
8. **Build stage primitives** - Atomize each stage's components
9. **Test end-to-end on real project** - Validate the system works

---

## 9. Open Questions for Decision

| Question | Options | Impact | Owner |
|----------|---------|--------|-------|
| Rules organization | One file per rule vs. grouped by domain | Memory implementation | Memory session |
| Agent write permissions | Full write / Append only / Read only | Automation level | Memory session |
| Frontmatter complexity | Minimal (5 fields) vs. Full AGS (12+ fields) | Adoption friction | AGS + Registry |
| Validation timing | Git hooks / CLI on-demand / Continuous | Developer experience | AGS session |

---

## 10. Session Sync Protocol

**When to update this document:**
- Workstream completes a major milestone
- Blocking issue identified
- Design decision made that affects other workstreams
- New backlog item identified

**How to sync:**
- Control Tower (this session) re-pulls recent chats
- Updates relevant sections
- Flags items needing cross-workstream coordination

---

## Appendix: Obsolete Files (Removed from Project)

The following files were part of the standalone app approach and have been archived:

- `IPE_Interface_Mockup.md`
- `IPE_Content_Editor_Specification.md`
- `ipe-demo-design-stack.md`
- `ipe-demo-design-architecture.md`
- `ipe-demo-design-data-model.md`
- `ipe-demo-design-context-schema.md`
- `ipe-demo-environment-repo-init.md`
- `ipe-demo-environment-dependencies.md`
- `ipe-demo-environment-scaffolding.md`
- `Stage_4_Workflow_Configuration_Specification.md`
- `Stage_5_Implementation_Planning_Specification.md`
- `section-metadata.ts`
- `validate-ipe.sh`
- `validate-tasks.py`
- `QUICK_REFERENCE.md`
- `Option_A_Complete_Summary.md`
- `Option_C_Complete_Summary.md`
- `IPE_Progress_Dashboard.md`
- `IPE_Progress_Dashboard_Final.md`
- `IPE_Stage_Navigation_v2.md`
- `IPE_Validation_Checklist.md`
- `IPE_Next_Steps_Tracking.md`

**Retained files:**
- `IPE_Product_Brief.md` - Problem statement
- `ipe-research-synthesis.md` - Validated research
- `ipe-demo-discovery-*.md` - Core concepts
- `IPE_Artifact_Schema_Specification.md` - AGS foundation
- `IPE_CLAUDE_Memory_Integration.md` - Memory foundation
- `README.md` - Update needed
- `00-ARTIFACT-INDEX.md` - Update needed

---

**Document Version:** 1.0
**Last Updated:** 2026-01-02
**Next Review:** When any workstream reports significant progress
