# IPE Stage Navigation - Complete Specification

**Version:** 2.0  
**Updated:** 2025-12-31  
**Status:** Incorporates Stages 1-5 + Hook Integration

---

## Overview

This document defines how IPE progresses through its five stages, what triggers stage transitions, how validation ensures quality, and how hooks automate the workflow.

**Five Stages:**
1. Discovery - Understand the problem
2. Solution Design - Define the solution
3. Environment Setup - Prepare the workspace
4. Workflow Configuration - Define how we work
5. Implementation Planning - Plan what to build

---

## Stage Progression Logic

```
START
  ↓
┌─────────────────────────────────────┐
│ Stage 1: Discovery                  │
│ ✓ All artifacts finalized           │
│ ✓ Requirements clear                │
│ ✓ Stakeholders aligned              │
└──────────────┬──────────────────────┘
               ↓
         [VALIDATION]
         All artifacts exist?
         All marked finalized?
               ↓ YES
┌─────────────────────────────────────┐
│ Stage 2: Solution Design            │
│ ✓ All artifacts finalized           │
│ ✓ Architecture defined              │
│ ✓ Stack selected                    │
└──────────────┬──────────────────────┘
               ↓
         [VALIDATION]
         Design complete?
         Stack feasible?
               ↓ YES
┌─────────────────────────────────────┐
│ Stage 3: Environment Setup          │
│ ✓ All artifacts finalized           │
│ ✓ Repository created                │
│ ✓ Tools installed                   │
└──────────────┬──────────────────────┘
               ↓
         [VALIDATION]
         Environment works?
         Tests pass?
               ↓ YES
┌─────────────────────────────────────┐
│ Stage 4: Workflow Configuration     │
│ ✓ All governed artifacts finalized  │
│ ✓ CLAUDE.md generated              │
│ ✓ Hooks configured                  │
└──────────────┬──────────────────────┘
               ↓
         [VALIDATION]
         Workflows defined?
         Hooks working?
               ↓ YES
┌─────────────────────────────────────┐
│ Stage 5: Implementation Planning    │
│ ✓ Pass 1 complete (tasks defined)  │
│ ✓ Pass 2 complete (skills mapped)  │
│ ✓ Plan locked                       │
└──────────────┬──────────────────────┘
               ↓
         [VALIDATION]
         All tasks have criteria?
         Dependencies valid?
               ↓ YES
┌─────────────────────────────────────┐
│ IMPLEMENTATION EXECUTION            │
│ (Follow tasks.md)                   │
└─────────────────────────────────────┘
```

---

## Stage 1: Discovery

### Entry Criteria
- Project initiated
- Problem statement exists
- Initial stakeholder identified

### Exit Criteria

**Artifacts:**
- [ ] discovery-synthesis.md - finalized
- [ ] stakeholders.md - finalized
- [ ] requirements.md - finalized
- [ ] constraints.md - finalized
- [ ] success-criteria.md - finalized
- [ ] Optional: discovery-session-notes.md

**Validation:**
```bash
# Check all required artifacts exist and finalized
ls .ipe/discovery/*.md
grep "status: finalized" .ipe/discovery/*.md

# Minimum 4 required artifacts finalized
```

**Hook Integration:**
- SessionEnd hook checks artifact status
- If all finalized → marks Stage 1 complete in CLAUDE.md
- Updates current stage to 2

### Transition to Stage 2

**Automatic:**
```
SessionEnd Hook:
  → Detects all Stage 1 artifacts finalized
  → Updates CLAUDE.md:
    ✅ Stage 1: Discovery (YYYY-MM-DD)
    Stage: 2
  → Creates stage summary
```

**Manual trigger if needed:**
```bash
./ipe/scripts/finalize-stage.sh 1
```

---

## Stage 2: Solution Design

### Entry Criteria
- Stage 1 complete
- All discovery artifacts finalized
- Requirements clearly defined

### Exit Criteria

**Artifacts:**
- [ ] architecture.md - finalized
- [ ] stack.md - finalized
- [ ] data-model.md - finalized
- [ ] api-design.md - finalized (if applicable)
- [ ] design-decisions.md - finalized
- [ ] Optional: solution-synthesis.md

**Validation:**
```bash
# Check all required artifacts exist and finalized
ls .ipe/solution-design/*.md
grep "status: finalized" .ipe/solution-design/*.md

# Verify stack is feasible
# (Human judgment - does stack support requirements?)
```

**Quality Gates:**
- Architecture supports all requirements
- Stack selections have rationale
- Data model is normalized/appropriate
- Design decisions documented

**Hook Integration:**
- SessionEnd hook checks artifact status
- If all finalized → marks Stage 2 complete
- Updates current stage to 3
- Imports key decisions into CLAUDE.md

### Transition to Stage 3

**Automatic:**
```
SessionEnd Hook:
  → Detects all Stage 2 artifacts finalized
  → Updates CLAUDE.md:
    ✅ Stage 2: Solution Design (YYYY-MM-DD)
    Stage: 3
  → Imports architecture.md, stack.md decisions
```

---

## Stage 3: Environment Setup

### Entry Criteria
- Stage 2 complete
- Solution design finalized
- Technology stack selected

### Exit Criteria

**Artifacts:**
- [ ] repo-structure.md - finalized
- [ ] environment-config.md - finalized
- [ ] setup-guide.md - finalized
- [ ] environment-manifest.json - finalized
- [ ] Optional: environment-synthesis.md

**Validation:**
```bash
# Check all required artifacts exist and finalized
ls .ipe/environment-setup/*.md
grep "status: finalized" .ipe/environment-setup/*.md

# Verify repository structure exists
ls -la src/ tests/ docs/

# Verify environment works
pytest --version
python --version
# (Check all tools from environment-manifest.json)
```

**Quality Gates:**
- Repository structure created
- All tools from stack.md installed
- Basic tests can run
- Documentation accessible

**Hook Integration:**
- SessionEnd hook checks artifact status
- If all finalized → marks Stage 3 complete
- Updates current stage to 4
- Baseline for drift detection established

### Transition to Stage 4

**Automatic:**
```
SessionEnd Hook:
  → Detects all Stage 3 artifacts finalized
  → Updates CLAUDE.md:
    ✅ Stage 3: Environment Setup (YYYY-MM-DD)
    Stage: 4
  → Imports repo-structure.md
  → Enables drift detection hooks
```

---

## Stage 4: Workflow Configuration

### Entry Criteria
- Stage 3 complete
- Environment fully set up
- Repository structure exists

### Exit Criteria

**Governed Artifacts (Must be finalized):**
- [ ] dev-workflow.md - finalized
- [ ] environment-variants.md - finalized
- [ ] context-management.md - finalized
- [ ] claude-config.md - finalized

**Continuous Artifacts (Must exist, may evolve):**
- [ ] claude.md - created and populated
- [ ] agent.md - created and populated
- [ ] operations-playbook.md - created

**Generated Artifacts:**
- [ ] .claude/CLAUDE.md - generated from claude-config.md
- [ ] .claude/settings.json - hooks configured

**Validation:**
```bash
# Check governed artifacts finalized
grep "status: finalized" .ipe/workflow-config/dev-workflow.md
grep "status: finalized" .ipe/workflow-config/environment-variants.md
grep "status: finalized" .ipe/workflow-config/context-management.md
grep "status: finalized" .ipe/workflow-config/claude-config.md

# Check continuous artifacts exist
ls .claude/claude.md
ls .agent/agent.md
ls .ipe/workflow-config/operations-playbook.md

# Verify CLAUDE.md generated
ls .claude/CLAUDE.md

# Verify hooks configured
jq .hooks .claude/settings.json

# Run CLAUDE.md validation
./.claude/hooks/validate-claude-md.sh
```

**Quality Gates:**
- All workflows documented
- Agent behavior rules defined
- CLAUDE.md structure correct
- Hooks installed and tested
- Token budget under limit (<20K)

**Hook Integration:**
- SessionEnd hook checks governed artifacts
- If all finalized → marks Stage 4 complete
- Updates current stage to 5
- Activates all implementation tracking hooks

### Transition to Stage 5

**Automatic:**
```
SessionEnd Hook:
  → Detects all governed artifacts finalized
  → Checks CLAUDE.md exists and valid
  → Checks hooks configured
  → Updates CLAUDE.md:
    ✅ Stage 4: Workflow Configuration (YYYY-MM-DD)
    Stage: 5
  → Enables implementation tracking
```

**Manual validation:**
```bash
# Test all hooks
./.claude/hooks/test-hooks.sh

# Validate CLAUDE.md
./.claude/hooks/validate-claude-md.sh

# If all pass, can proceed to Stage 5
```

---

## Stage 5: Implementation Planning

### Entry Criteria
- Stage 4 complete
- Workflows defined
- CLAUDE.md and hooks working

### Two-Pass Approach

**Pass 1: Core Plan**
- [ ] phases.md - created
- [ ] tasks.md - created
- [ ] dependencies.md - created
- [ ] effort-estimates.md - created

**Pass 1 Validation:**
```bash
# All Pass 1 artifacts exist
ls .ipe/implementation/phases.md
ls .ipe/implementation/tasks.md
ls .ipe/implementation/dependencies.md
ls .ipe/implementation/effort-estimates.md

# Human review and approval
# Agent cannot proceed to Pass 2 without approval
```

**Pass 2: Execution Support**
- [ ] skills-and-agents.md - created

**Pass 2 Validation:**
```bash
# Pass 2 artifact exists
ls .ipe/implementation/skills-and-agents.md

# All skills available or creation plan exists
# Human review and approval
```

### Exit Criteria

**All Artifacts Locked:**
- [ ] phases.md - locked
- [ ] tasks.md - locked
- [ ] dependencies.md - locked
- [ ] effort-estimates.md - locked
- [ ] skills-and-agents.md - locked

**Validation:**
```bash
# Check all artifacts locked
grep "status: locked" .ipe/implementation/*.md

# Validate content
python scripts/validate-implementation-plan.py

# Checks:
# - All solution features have tasks
# - All tasks have acceptance criteria
# - Dependencies form valid DAG
# - Estimates are realistic
# - No circular dependencies
```

**Quality Gates:**
- Every feature from solution design has tasks
- Each task has clear, testable acceptance criteria
- Dependencies are logical and complete
- Critical path identified
- Estimates sum to realistic timeline
- Skills exist or can be created

**Hook Integration:**
- SessionEnd hook checks all artifacts locked
- If all locked → marks Stage 5 complete
- Implementation phase can begin
- Task tracking hooks now active

### Transition to Implementation

**Automatic:**
```
SessionEnd Hook:
  → Detects all Stage 5 artifacts locked
  → Validates implementation plan
  → Updates CLAUDE.md:
    ✅ Stage 5: Implementation Planning (YYYY-MM-DD)
    Implementation Status: Ready to Begin
  → Loads tasks.md into CLAUDE.md imports
  → Activates task tracking hooks
```

**Manual start:**
```bash
# Validate entire plan
python scripts/validate-implementation-plan.py

# If validation passes, begin implementation
# Agent starts with TASK-001
```

---

## Cross-Stage Validation

### Overall IPE Validation

**Run before starting implementation:**

```bash
# Comprehensive IPE validation
./scripts/validate-ipe.sh

# Checks:
# ✓ All 5 stages complete
# ✓ All required artifacts exist
# ✓ All artifacts have proper status
# ✓ Cross-references valid
# ✓ No broken links
# ✓ CLAUDE.md valid
# ✓ Hooks configured
# ✓ Repository structure correct
# ✓ Implementation plan complete
```

**Validation Output:**
```
IPE Validation Report
=====================

Stage 1: Discovery
  ✓ All artifacts finalized
  ✓ Requirements documented

Stage 2: Solution Design
  ✓ All artifacts finalized
  ✓ Stack selected and viable

Stage 3: Environment Setup
  ✓ All artifacts finalized
  ✓ Repository structure exists
  ✓ Environment functional

Stage 4: Workflow Configuration
  ✓ Governed artifacts finalized
  ✓ Continuous artifacts exist
  ✓ CLAUDE.md generated
  ✓ Hooks configured

Stage 5: Implementation Planning
  ✓ All artifacts locked
  ✓ Tasks have acceptance criteria
  ✓ Dependencies valid
  ✓ Estimates reasonable

Overall: ✅ READY FOR IMPLEMENTATION

Next: Start TASK-001
```

---

## Hook Integration Points

### SessionStart Hook (inject-stage-context.sh)

**Runs:** Every Claude Code session start

**Actions:**
1. Display current stage
2. Show completed stages
3. Display task progress (if Stage 5+)
4. Show recent activity
5. Run validation
6. Provide next actions

**Output Example:**
```
═══════════════════════════════════════════════════════════════
  IPE Session Context
═══════════════════════════════════════════════════════════════

📍 Current Stage: 5 - Implementation Planning
✅ Completed Stages: 4
📋 Task Progress: 0/20 complete, 0 in progress, 0 blocked
🕐 Recent Activity: Last: 2025-01-02T10:00:00Z | Current: Stage 5

🔍 Context Validation:
✓ All validation checks passed

📚 Quick Reference:
  Current stage artifacts: .ipe/implementation/

🎯 Next Actions:
  → Check .ipe/implementation/tasks.md
  → Begin Pass 1: Create phases.md
```

### Stop Hook (update-claude-md.sh)

**Runs:** When agent stops responding

**Actions:**
1. Read implementation-state.json
2. Extract current task
3. Get task progress from tasks.md
4. Update CLAUDE.md [ACTIVE-CONTEXT] section
5. Update state file timestamp

**Updates CLAUDE.md:**
```markdown
## [ACTIVE-CONTEXT] - Current Work (Auto-Updated)

**Current Task:** TASK-005
**Task Progress:** 5/20 complete, 1 in progress
**Recent Files:** src/main.py, tests/test_health.py
**Last Updated:** 2025-01-02T15:30:00Z
```

### SessionEnd Hook (finalize-stage.sh)

**Runs:** When Claude Code session ends

**Actions:**
1. Check current stage
2. Validate all stage artifacts
3. If all finalized/locked → mark stage complete
4. Update CLAUDE.md with completion marker
5. Move to next stage
6. Create stage summary

**Updates CLAUDE.md:**
```markdown
## Completed Stages
✅ Stage 1: Discovery (2025-01-01)
✅ Stage 2: Solution Design (2025-01-02)
✅ Stage 3: Environment Setup (2025-01-03)
✅ Stage 4: Workflow Configuration (2025-01-04)

## Current Stage
Stage: 5 - Implementation Planning
```

### PostToolUse Hooks

**check-structure.sh:**
- Validates file placement against repo-structure.md
- Blocks critical violations
- Warns on minor issues

**track-implementation.sh:**
- Updates implementation-state.json
- Tracks file modifications
- Detects task completions
- Auto-commits completed tasks

---

## Implementation Execution (After Stage 5)

### Task Execution Loop

```
1. Agent reads tasks.md
   ↓
2. Identifies next task (by dependencies)
   ↓
3. Reads task specification
   ↓
4. Implements according to acceptance criteria
   ↓
5. Tests implementation
   ↓
6. Marks task complete in tasks.md:
   - Completion date
   - Git commit SHA
   - Brief notes
   ↓
7. Git commit: [TASK-XXX] Description
   ↓
8. PostToolUse hook updates state
   ↓
9. Stop hook updates CLAUDE.md
   ↓
10. Loop to next task
```

### Progress Tracking

**Automated via hooks:**
- implementation-state.json updated after each file change
- tasks.md completions trigger auto-commits
- CLAUDE.md shows current progress
- State preserved across sessions

**Manual tracking:**
```bash
# View current progress
cat .ipe/implementation-state.json | jq .

# Check task completion
grep "Status: ✅ Complete" .ipe/implementation/tasks.md

# View active task
grep "Status: 🔄 In Progress" .ipe/implementation/tasks.md
```

---

## Deviation Handling

### When Agent Encounters Blocker

**Protocol:**
1. STOP immediately
2. Document in tasks.md as comment
3. Alert human via system message
4. Wait for decision

**Minor deviation (quick review):**
```markdown
<!-- DEVIATION REQUEST by Claude
Task: TASK-010
Issue: Library X incompatible with Python 3.12
Proposed: Use Library Y (same functionality)
Impact: No scope change
-->

<!-- APPROVED by Human on 2025-01-03
Proceed with Library Y
-->
```

**Major deviation (change order):**
```markdown
## Change Order: CO-001
Date: 2025-01-03
Affected Tasks: TASK-010, TASK-011
Reason: API design changed after stakeholder feedback
Impact: Scope change, +2 days
Status: Approved
Version: tasks.md 1.0.0 → 1.1.0
```

---

## Stage Reversal

**Can we go backwards?**

**Generally NO** - stages build on each other

**Exception: Discovery of critical issue**

**Process:**
1. Create issue document in current stage
2. Reference back to problematic artifact
3. Create change order if needed
4. Update affected artifacts
5. Re-validate forward progression

**Example:**
```
During Stage 5 (Implementation Planning):
Discover architecture won't support requirement R-007

Actions:
1. Document in .ipe/implementation/issues/architecture-issue-001.md
2. Reference .ipe/solution-design/architecture.md
3. Create CO-002 for architecture.md update
4. Update architecture.md (version bump)
5. Validate Stage 3-4 artifacts still valid
6. Continue Stage 5 with updated architecture
```

---

## Validation Checkpoint Summary

| Stage | Validation Type | Automated? | Required |
|-------|----------------|------------|----------|
| 1 → 2 | All artifacts finalized | ✅ Hook | Yes |
| 2 → 3 | All artifacts finalized | ✅ Hook | Yes |
| 3 → 4 | All artifacts finalized | ✅ Hook | Yes |
| 3 → 4 | Environment works | ❌ Manual | Yes |
| 4 → 5 | Governed artifacts finalized | ✅ Hook | Yes |
| 4 → 5 | CLAUDE.md valid | ✅ Script | Yes |
| 4 → 5 | Hooks configured | ✅ Script | Yes |
| 5 → Impl | Pass 1 complete | ❌ Manual | Yes |
| 5 → Impl | Pass 2 complete | ❌ Manual | Yes |
| 5 → Impl | All artifacts locked | ✅ Hook | Yes |
| 5 → Impl | Dependencies valid | ✅ Script | Yes |
| 5 → Impl | Complete plan valid | ✅ Script | Yes |

---

## Quick Reference

### Stage Status Commands

```bash
# Check current stage
grep "^Stage:" .claude/CLAUDE.md

# List completed stages
grep "^✅ Stage" .claude/CLAUDE.md

# Validate current stage
./scripts/validate-stage.sh $(grep "^Stage:" .claude/CLAUDE.md | cut -d: -f2)

# Manually trigger stage finalization
./.claude/hooks/finalize-stage.sh
```

### File Locations by Stage

```
Stage 1: .ipe/discovery/
Stage 2: .ipe/solution-design/
Stage 3: .ipe/environment-setup/
Stage 4: .ipe/workflow-config/
         .claude/ (generated artifacts)
Stage 5: .ipe/implementation/
```

### Critical Files

```
.claude/CLAUDE.md               # Auto-generated context
.claude/claude.md               # Agent behavior rules
.claude/settings.json           # Hook configuration
.ipe/implementation/tasks.md    # Task specifications
.ipe/implementation-state.json  # Current execution state
```

---

## Version History

**2.0.0** (2025-12-31)
- Added Stage 4 completion logic
- Added Stage 5 two-pass approach
- Integrated hook automation
- Added deviation handling
- Complete validation checkpoints

**1.0.0** (2025-12-31)
- Initial stage navigation
- Stages 1-3 defined
- Basic progression logic
