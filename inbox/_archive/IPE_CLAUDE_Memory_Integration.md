# IPE CLAUDE.md Memory Integration

**Document:** IPE CLAUDE.md Memory Integration Specification  
**Version:** 1.0.0  
**Stage:** 4 (Workflow Configuration)  
**Purpose:** Leverage Claude Code's built-in memory system for persistent project context

---

## Overview

CLAUDE.md provides a hierarchical, version-controlled memory system for Claude Code projects. IPE integrates CLAUDE.md to maintain context across sessions, prevent decision amnesia, and ensure agents have continuous access to critical project information.

**Key Benefits:**
- Zero-setup (built into Claude Code)
- Version-controlled with project
- Automatic loading at session start
- Supports imports from stage artifacts
- Team-shared knowledge base

---

## Memory Hierarchy

Claude Code loads memory files in this order (highest to lowest priority):

```
1. Enterprise Policy (managed by IT)
   └── /Library/Application Support/ClaudeCode/CLAUDE.md (macOS)
   └── /etc/claude-code/CLAUDE.md (Linux)
   └── C:\Program Files\ClaudeCode\CLAUDE.md (Windows)

2. Project Memory (team-shared, version-controlled)
   └── .claude/CLAUDE.md                    ← IPE PRIMARY
   └── CLAUDE.md                             ← Legacy location

3. User Memory (personal, all projects)
   └── ~/.claude/CLAUDE.md

4. Project Local (personal, this project only, .gitignored)
   └── .claude/CLAUDE.local.md
```

**IPE uses:** `.claude/CLAUDE.md` (project memory)

---

## IPE Directory Structure with CLAUDE.md

```
project-root/
├── .ipe/                          # IPE planning artifacts
│   ├── discovery/
│   ├── solution-design/
│   ├── environment-setup/
│   ├── workflow-config/
│   │   └── claude-config.md       ← NEW: Defines CLAUDE.md structure
│   └── implementation/
│
├── .claude/                       # Claude Code integration
│   ├── CLAUDE.md                  ← AUTO-GENERATED from claude-config.md
│   ├── CLAUDE.local.md            ← User-specific overrides (.gitignored)
│   ├── skills/
│   ├── agents/
│   ├── settings.json              # Hooks, tools, config
│   └── hooks/                     # Hook scripts
│
└── [project files]
```

---

## Stage 4 Artifact: claude-config.md

**New artifact in Stage 4 (Workflow Configuration):**

**Purpose:** Defines what context gets loaded into CLAUDE.md and how it's structured

**Location:** `.ipe/workflow-config/claude-config.md`

### claude-config.md Template

```markdown
---
artifact: claude-config.md
status: draft
stage: workflow-config
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: [agent-rules.md, dev-workflow.md]
---

# Claude Memory Configuration

## Overview

This document defines the structure and content of `.claude/CLAUDE.md`, which 
provides persistent context to Claude Code across sessions.

## Memory Structure

### 1. Project Status
**Purpose:** Current stage, active tasks, completion status
**Update frequency:** On stage transitions, task completion
**Source:** Automated from implementation-state.json

### 2. Completed Stages
**Purpose:** Historical record of what's been finalized
**Update frequency:** On stage finalization
**Source:** Automated from stage status

### 3. Key Decisions
**Purpose:** Critical architectural and technical choices
**Update frequency:** On decision finalization
**Source:** Manual extraction from stage artifacts

### 4. Critical Rules
**Purpose:** Non-negotiable constraints and requirements
**Update frequency:** Rarely (foundational rules)
**Source:** Imported from repo-structure.md, agent-rules.md

### 5. Artifact Imports
**Purpose:** Direct access to finalized stage artifacts
**Update frequency:** On stage completion
**Source:** Automated imports via @path syntax

### 6. Active Context
**Purpose:** Current work in progress
**Update frequency:** Real-time during implementation
**Source:** Automated from tasks.md, implementation-state.json

## Import Strategy

### Static Imports (Always Loaded)
```markdown
## Foundation Documents
@.ipe/discovery/synthesis.md
@.ipe/solution-design/stack.md
@.ipe/environment-setup/repo-structure.md
@.ipe/workflow-config/agent-rules.md
```

**Purpose:** Core decisions that inform all work
**When:** After each stage is finalized

### Dynamic Imports (Conditionally Loaded)
```markdown
## Current Stage Context
@.ipe/implementation/phases.md
@.ipe/implementation/tasks.md
@.ipe/implementation/skills-and-agents.md
```

**Purpose:** Active implementation context
**When:** During Stage 5 (Implementation)

### Progressive Imports (As Needed)
```markdown
## Architecture Details
<!-- Uncomment when working on specific areas -->
<!-- @.ipe/solution-design/architecture.md -->
<!-- @.ipe/solution-design/data-model.md -->
```

**Purpose:** Detailed specs loaded on-demand
**When:** Agent requests or user triggers

## Content Guidelines

### What to Include
- **Stage completion status** - Track progress
- **Key decisions** - Prevent re-litigating settled choices
- **Critical constraints** - Non-negotiable rules
- **Active tasks** - What's currently in progress
- **File placement rules** - Reference repo-structure.md
- **Agent behavior** - Reference agent-rules.md

### What to Exclude
- **Verbose explanations** - Keep concise, link to artifacts
- **Temporary notes** - Use CLAUDE.local.md instead
- **Sensitive data** - Never commit secrets
- **Implementation details** - Import from artifacts, don't duplicate

### Token Budget
- **Target:** <5,000 tokens for CLAUDE.md itself
- **Imported content:** 10,000-15,000 tokens total
- **Total context:** ~20,000 tokens at session start
- **Rationale:** Leave room for conversation, files, tool outputs

## Update Mechanisms

### Automated Updates
```bash
# Via hooks in .claude/settings.json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/update-claude-md.sh"
      }]
    }],
    "SessionEnd": [{
      "hooks": [{
        "type": "command", 
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/finalize-stage.sh"
      }]
    }]
  }
}
```

**Triggers:**
- Task completion → Update active tasks
- Stage completion → Add to completed stages, update imports
- Session end → Sync state to CLAUDE.md

### Manual Updates
```bash
# Quick add via # shortcut (in Claude Code session)
> # Always validate file paths against repo-structure.md

# Direct edit via /memory command
> /memory
[Opens .claude/CLAUDE.md in editor]
```

## Maintenance Workflow

### Daily (Automated)
- Update active tasks from tasks.md
- Sync completion status
- Refresh import list

### Weekly (Agent-prompted)
- Review and prune stale content
- Verify import accuracy
- Check token budget

### Per-Stage (Manual)
- Add stage completion marker
- Update static imports
- Extract key decisions

## Example: Generated CLAUDE.md

See "CLAUDE.md Generation Example" section below.

## Validation Rules

### Structure Validation
- Must start with project status
- Must include critical rules section
- Must have artifact imports section
- Token count < 20,000 total

### Content Validation  
- No secrets or credentials
- All imports reference existing files
- Decisions reference source artifacts
- Rules align with agent-rules.md

### Quality Checks
- Is information still current?
- Are imports still relevant?
- Is content concise enough?
- Does it prevent common mistakes?

## Integration with Stage 5

### Implementation Planning Phase
```markdown
## Current Stage
Stage 5: Implementation Planning
Phase: Defining tasks and execution strategy

## Active Work
- Creating tasks.md (task breakdown)
- Defining skills-and-agents.md (execution infrastructure)
- Planning phase structure

## Next Steps
1. Complete tasks.md (all tasks defined)
2. Identify required skills/agents
3. Validate task dependencies
4. Finalize implementation plan
```

### Execution Phase
```markdown
## Current Stage  
Stage 5: Implementation
Phase: MVP - Foundation
Active: TASK-012 (User authentication)

## Progress
Tasks Complete: 11/50
Phase: MVP (40% complete)
Last Commit: abc123d - [TASK-011] Database schema

## Active Tasks
TASK-012: Implement user authentication
├─ Status: In Progress
├─ Agent: MainAgent
├─ Files: src/auth/service.py, src/models/user.py
└─ Checkpoint: Password hashing complete

## Recent Decisions
- Use bcrypt for password hashing (TASK-012)
- Session tokens expire after 24h (TASK-010)
```

## Hooks for CLAUDE.md Maintenance

### update-claude-md.sh (Stop Hook)
```bash
#!/bin/bash
# Updates CLAUDE.md with current state

PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
STATE_FILE="$PROJECT_ROOT/.ipe/implementation-state.json"
CLAUDE_MD="$PROJECT_ROOT/.claude/CLAUDE.md"

# Extract current state
current_task=$(jq -r '.current_task' "$STATE_FILE")
completed=$(jq -r '.progress.tasks_complete' "$STATE_FILE")
total=$(jq -r '.progress.tasks_total' "$STATE_FILE")

# Update Active Tasks section
sed -i "/## Active Tasks/,/^## / {
  /## Active Tasks/!{
    /^## /!d
  }
}" "$CLAUDE_MD"

# Insert current state
cat >> "$CLAUDE_MD" << EOF

## Active Tasks
Current: $current_task
Progress: $completed/$total tasks complete

EOF
```

### finalize-stage.sh (SessionEnd Hook)
```bash
#!/bin/bash
# Marks stage as complete in CLAUDE.md

stage_complete() {
  # Check if all stage artifacts are finalized
  # Return 0 if complete, 1 if not
}

if stage_complete; then
  stage_num=$(get_current_stage)
  stage_name=$(get_stage_name "$stage_num")
  
  # Add to completed stages
  sed -i "/## Completed Stages/a ✅ Stage $stage_num: $stage_name ($(date +%Y-%m-%d))" \
    "$CLAUDE_PROJECT_DIR/.claude/CLAUDE.md"
  
  # Update imports
  add_stage_imports "$stage_num"
fi
```

---

## CLAUDE.md Generation Example

**Generated `.claude/CLAUDE.md` after Stage 3 completion:**

```markdown
# IPE Project Context

**Last Updated:** 2025-01-04 15:30:00  
**Session:** Implementation Planning

---

## Current Stage

**Stage 5:** Implementation Planning  
**Phase:** Defining tasks and execution strategy  
**Status:** Active

**Focus:**
- Breaking down implementation into atomic tasks
- Identifying required skills and sub-agents
- Planning phase/milestone structure

---

## Completed Stages

✅ **Stage 1:** Discovery (2025-01-02)  
✅ **Stage 2:** Solution Design (2025-01-03)  
✅ **Stage 3:** Environment Setup (2025-01-04)  
⏳ **Stage 4:** Workflow Configuration (2025-01-05)  
⏳ **Stage 5:** Implementation Planning (In Progress)

---

## Key Decisions

### Technology Stack
- **Language:** Python 3.12
- **Framework:** FastAPI (async-first)
- **Database:** PostgreSQL 16 with SQLAlchemy
- **Testing:** pytest + coverage
- **API:** RESTful with OpenAPI/Swagger

**Source:** [stack.md](.ipe/solution-design/stack.md)

### Architecture
- **Pattern:** Microservices with event bus
- **Communication:** Async message queues (Redis)
- **Scalability:** Horizontal via Docker/K8s
- **State:** Stateless services, DB for persistence

**Source:** [architecture.md](.ipe/solution-design/architecture.md)

### Repository Structure
- **Source code:** `src/` only
- **Tests:** `tests/` (mirrors src structure)
- **No code in root** except entry points
- **Enforcement:** Via repo-structure.md rules

**Source:** [repo-structure.md](.ipe/environment-setup/repo-structure.md)

---

## Critical Rules

### File Placement (ENFORCED)
ALWAYS validate file locations against repo-structure.md before creating files.

**Correct:**
- ✅ `src/api/v1_users.py` (API routes)
- ✅ `src/models/user.py` (data models)
- ✅ `tests/api/test_users.py` (tests mirror src)

**Incorrect:**
- ❌ `user.py` (root level)
- ❌ `src/test_user.py` (tests not in src)
- ❌ `api/users.py` (missing src prefix)

### Agent Behavior (REQUIRED)
1. **Task Completion Protocol**
   - Mark task complete in tasks.md
   - Add completion date + commit SHA
   - Git commit with [TASK-XXX] prefix
   - Generate progress summary

2. **Deviation Protocol**
   - STOP if task cannot be completed as specified
   - Document issue, alert human, wait for decision
   - DO NOT improvise alternative approaches

3. **Tool Failure Protocol**
   - Retry with correct syntax
   - If still failing, STOP and alert human
   - DO NOT create workaround scripts without approval

**Source:** [agent-rules.md](.ipe/workflow-config/agent-rules.md)

---

## Artifact Imports

### Foundation (Always Loaded)
@.ipe/discovery/synthesis.md  
@.ipe/solution-design/stack.md  
@.ipe/environment-setup/repo-structure.md

### Current Work (Implementation)
@.ipe/implementation/phases.md  
@.ipe/implementation/tasks.md  
@.ipe/implementation/skills-and-agents.md

### Reference (On-Demand)
<!-- Uncomment when working on specific areas -->
<!-- @.ipe/solution-design/architecture.md -->
<!-- @.ipe/solution-design/data-model.md -->
<!-- @.ipe/workflow-config/dev-workflow.md -->

---

## Active Context

**Implementation Plan:** [phases.md](.ipe/implementation/phases.md)  
**Task Breakdown:** [tasks.md](.ipe/implementation/tasks.md)  
**Execution Setup:** [skills-and-agents.md](.ipe/implementation/skills-and-agents.md)

**Next Actions:**
1. Complete task definitions in tasks.md
2. Identify required skills/agents
3. Validate task dependencies
4. Finalize feature-plan.md

---

## Environment Status

**Setup Complete:** ✅ Stage 3 validated  
**Environment File:** `.env.template` → `.env`  
**Dependencies:** requirements.txt installed  
**Validation:** All import tests passing

**Tools Available:**
- pytest, black, mypy, ruff
- SQLAlchemy, FastAPI, Pydantic
- Redis, PostgreSQL drivers

---

## Session Continuity

**Last Session:** 2025-01-04 14:00:00  
**Last Action:** Completed environment validation  
**Current Focus:** Breaking down implementation tasks

**Recovery Info:**
- All stage artifacts finalized through Stage 3
- Implementation plan in progress
- No blocked tasks
- Next: Define TASK-001 through TASK-050
```

---

## claude-config.md Example

**Location:** `.ipe/workflow-config/claude-config.md`

```markdown
---
artifact: claude-config.md
status: finalized
stage: workflow-config
created: 2025-01-05 [Jess]
updated: 2025-01-05 [Claude]
version: 1.0.0
---

# Claude Memory Configuration

## Purpose

Defines structure and content management for `.claude/CLAUDE.md`, ensuring 
consistent context injection across all Claude Code sessions.

## Memory Structure Definition

### Section 1: Current Stage (Dynamic)
**Content:**
- Stage number and name
- Current phase/milestone
- Active focus areas

**Update Trigger:** Stage transitions, phase changes  
**Source:** implementation-state.json  
**Token Budget:** ~200 tokens

### Section 2: Completed Stages (Append-Only)
**Content:**
- Chronological list with dates
- Status indicators (✅ complete, ⏳ in-progress)

**Update Trigger:** Stage finalization  
**Source:** Stage completion hooks  
**Token Budget:** ~150 tokens

### Section 3: Key Decisions (Curated)
**Content:**
- Technology stack choices
- Architecture patterns
- Critical constraints
- Links to source artifacts

**Update Trigger:** Decision finalization  
**Source:** Manual extraction from syntheses  
**Token Budget:** ~1,000 tokens

### Section 4: Critical Rules (Static)
**Content:**
- File placement rules (from repo-structure.md)
- Agent behavior protocols (from agent-rules.md)
- Task completion requirements (from dev-workflow.md)

**Update Trigger:** Rarely (foundational rules)  
**Source:** Imported from workflow config  
**Token Budget:** ~1,500 tokens

### Section 5: Artifact Imports (Progressive)
**Content:**
- Static imports (always loaded)
- Dynamic imports (stage-specific)
- Optional imports (commented out)

**Update Trigger:** Stage completion  
**Source:** Automated via hooks  
**Token Budget:** ~10,000 tokens (imported content)

### Section 6: Active Context (Real-Time)
**Content:**
- Current task(s)
- Recent progress
- Next steps

**Update Trigger:** Task completion, Stop hook  
**Source:** tasks.md, implementation-state.json  
**Token Budget:** ~500 tokens

### Section 7: Environment Status (Reference)
**Content:**
- Setup completion status
- Available tools
- Configuration state

**Update Trigger:** Environment changes  
**Source:** environment-manifest.json  
**Token Budget:** ~200 tokens

## Import Management

### Import Timing Strategy

**Session Start (Immediate):**
```markdown
@.ipe/environment-setup/repo-structure.md
@.ipe/workflow-config/agent-rules.md
```
**Why:** Critical rules needed from first action

**Stage 5 Start (Implementation):**
```markdown
@.ipe/implementation/phases.md
@.ipe/implementation/tasks.md
@.ipe/implementation/skills-and-agents.md
```
**Why:** Execution context for task work

**On-Demand (User/Agent Request):**
```markdown
<!-- @.ipe/solution-design/architecture.md -->
<!-- @.ipe/solution-design/data-model.md -->
```
**Why:** Detailed specs not always needed

### Import Syntax Examples

**Absolute path:**
```markdown
@/Users/jess/projects/risk-tools/.ipe/discovery/synthesis.md
```

**Relative to project root:**
```markdown
@.ipe/discovery/synthesis.md
```

**User home directory:**
```markdown
@~/.claude/my-global-rules.md
```

**Multiple related files:**
```markdown
## Architecture Details
@.ipe/solution-design/stack.md
@.ipe/solution-design/architecture.md
@.ipe/solution-design/data-model.md
```

## Automation Hooks

### Hook 1: update-claude-md.sh (Stop Hook)
**Trigger:** Agent stops responding (task complete or pause)  
**Actions:**
- Read implementation-state.json
- Update "Active Context" section
- Refresh task progress counters

**Implementation:**
```bash
#!/bin/bash
# .claude/hooks/update-claude-md.sh

STATE="$CLAUDE_PROJECT_DIR/.ipe/implementation-state.json"
CLAUDE_MD="$CLAUDE_PROJECT_DIR/.claude/CLAUDE.md"

# Extract current state
current=$(jq -r '.current_task' "$STATE")
completed=$(jq -r '.progress.tasks_complete' "$STATE")
total=$(jq -r '.progress.tasks_total' "$STATE")
last_commit=$(jq -r '.git_state.last_commit' "$STATE")

# Update Active Context section (in-place edit)
# [Implementation details in hooks specification]
```

### Hook 2: finalize-stage.sh (SessionEnd Hook)
**Trigger:** Session ends + stage is complete  
**Actions:**
- Mark stage as completed
- Add completion date
- Update static imports

**Implementation:**
```bash
#!/bin/bash
# .claude/hooks/finalize-stage.sh

if stage_is_complete; then
  # Add to completed stages
  # Update import list
  # Archive stage context
fi
```

### Hook 3: inject-stage-context.sh (SessionStart Hook)
**Trigger:** New session starts  
**Actions:**
- Load CLAUDE.md with imports
- Inject recent observations (if claude-mem installed)
- Display stage status

**Implementation:**
```bash
#!/bin/bash
# .claude/hooks/inject-stage-context.sh

# CLAUDE.md is auto-loaded by Claude Code
# This hook adds supplementary context

if command -v curl &> /dev/null; then
  # Inject recent observations from claude-mem
  recent=$(curl -s localhost:37777/api/recent?limit=10)
  echo "$recent" | format_for_context
fi

# Display current stage
stage=$(grep "^**Stage" "$CLAUDE_PROJECT_DIR/.claude/CLAUDE.md")
echo "Context loaded: $stage"
```

## Token Budget Management

### Target Budgets (Total ~20,000 tokens)

| Component | Budget | Priority |
|-----------|--------|----------|
| CLAUDE.md core | 3,000 | Critical |
| Static imports | 5,000 | Critical |
| Dynamic imports | 7,000 | High |
| Optional imports | 5,000 | Medium |
| **Total** | **20,000** | - |

### Budget Tracking

**Automated monitoring:**
```bash
# .claude/hooks/check-token-budget.sh

CLAUDE_MD="$CLAUDE_PROJECT_DIR/.claude/CLAUDE.md"

# Rough token count (4 chars = 1 token)
char_count=$(wc -c < "$CLAUDE_MD")
token_estimate=$((char_count / 4))

if [ $token_estimate -gt 20000 ]; then
  echo "⚠️  CLAUDE.md exceeds token budget: ~$token_estimate tokens"
  echo "Consider moving content to optional imports"
fi
```

### Optimization Strategies

**When over budget:**
1. Move detailed specs to optional imports
2. Condense key decisions (link to full artifacts)
3. Archive old active context
4. Remove stale environment status

**Example optimization:**
```markdown
### Before (verbose, 800 tokens)
## Key Decisions

### Technology Stack
We chose Python 3.12 because it offers the latest async features, 
improved type hints, and better performance. FastAPI was selected 
over Flask because it provides automatic OpenAPI documentation, 
native async support, and built-in validation with Pydantic...

### After (concise, 200 tokens)  
## Key Decisions

**Stack:** Python 3.12 + FastAPI + PostgreSQL  
**Rationale:** Async-first, type-safe, auto-docs  
**Details:** @.ipe/solution-design/stack.md
```

## Maintenance Guidelines

### Daily Maintenance (Automated)
- ✅ Update active tasks after each Stop
- ✅ Sync progress counters
- ✅ Refresh git state

### Weekly Maintenance (Agent-Prompted)
- Review token budget
- Prune completed task references
- Verify import accuracy
- Check for stale content

### Per-Stage Maintenance (Manual)
- Extract and add key decisions
- Update static imports
- Mark stage completion
- Archive old active context

### Quality Checks
```markdown
## Weekly Quality Check

- [ ] Token budget under 20,000?
- [ ] All imports reference existing files?
- [ ] Decisions link to source artifacts?
- [ ] Active context is current?
- [ ] No sensitive data present?
- [ ] Rules align with agent-rules.md?
```

## Validation Script

**Location:** `.claude/hooks/validate-claude-md.sh`

```bash
#!/bin/bash
# Validates CLAUDE.md structure and content

CLAUDE_MD="$CLAUDE_PROJECT_DIR/.claude/CLAUDE.md"
errors=0

# Check required sections
required_sections=(
  "Current Stage"
  "Completed Stages"
  "Key Decisions"
  "Critical Rules"
  "Artifact Imports"
)

for section in "${required_sections[@]}"; do
  if ! grep -q "## $section" "$CLAUDE_MD"; then
    echo "❌ Missing section: $section"
    errors=$((errors + 1))
  fi
done

# Check token budget
char_count=$(wc -c < "$CLAUDE_MD")
token_estimate=$((char_count / 4))

if [ $token_estimate -gt 25000 ]; then
  echo "❌ Token budget exceeded: ~$token_estimate tokens"
  errors=$((errors + 1))
fi

# Check imports exist
while IFS= read -r import_line; do
  file=$(echo "$import_line" | sed 's/@//' | sed 's/^ *//')
  if [[ ! -f "$CLAUDE_PROJECT_DIR/$file" ]]; then
    echo "❌ Import not found: $file"
    errors=$((errors + 1))
  fi
done < <(grep "^@" "$CLAUDE_MD")

if [ $errors -eq 0 ]; then
  echo "✅ CLAUDE.md validation passed"
  exit 0
else
  echo "❌ CLAUDE.md validation failed ($errors errors)"
  exit 1
fi
```

---

## Integration with Other IPE Components

### With Stage Artifacts
- CLAUDE.md imports finalized artifacts
- Decisions extracted from syntheses
- Rules reference workflow config

### With Hooks System
- SessionStart: Load CLAUDE.md + inject context
- Stop: Update active tasks
- SessionEnd: Finalize stage if complete

### With State Management
- implementation-state.json → Active Context
- tasks.md → Task progress
- Git commits → Recent activity

### With claude-mem (if installed)
- CLAUDE.md: Static project context
- claude-mem: Dynamic implementation history
- Combined: Complete session context

**Example combined context:**
```
Session Start:
1. Load CLAUDE.md (~15,000 tokens)
   - Stage status, decisions, rules, imports
2. Inject claude-mem index (~500 tokens)
   - Recent observations summary
3. Total: ~15,500 tokens baseline

Agent requests detail:
4. Fetch specific observation (~500 tokens)
5. Or read source file directly

Total context: ~16,000 tokens (efficient)
```

---

## Troubleshooting

### Problem: CLAUDE.md not loading
**Diagnosis:**
```bash
# Check file exists
ls -la .claude/CLAUDE.md

# Check Claude Code can read it
cat .claude/CLAUDE.md | head -20

# Check for syntax errors in imports
grep "^@" .claude/CLAUDE.md
```

**Solution:**
- Verify file location (`.claude/` not `.ipe/`)
- Check file permissions (readable)
- Validate import paths

### Problem: Imports not working
**Diagnosis:**
```bash
# Test import resolution
grep "^@" .claude/CLAUDE.md | while read import; do
  file=$(echo "$import" | sed 's/@//')
  if [[ ! -f "$file" ]]; then
    echo "Missing: $file"
  fi
done
```

**Solution:**
- Use relative paths from project root
- Verify files exist before importing
- Check for typos in paths

### Problem: Token budget exceeded
**Diagnosis:**
```bash
# Count tokens
wc -c .claude/CLAUDE.md | awk '{print $1/4 " tokens (estimate)"}'

# Find largest sections
awk '/^## / {section=$0; next} {count[section]+=length} END {for(s in count) print count[s]/4, s}' .claude/CLAUDE.md | sort -rn
```

**Solution:**
- Move verbose content to optional imports
- Condense key decisions
- Remove stale context

### Problem: Context not updating
**Diagnosis:**
```bash
# Check hook execution
grep "update-claude-md" ~/.claude/projects/*/logs/*

# Manually trigger update
./.claude/hooks/update-claude-md.sh
```

**Solution:**
- Verify hooks are configured in settings.json
- Check hook script permissions (executable)
- Run hooks manually to test

---

## Best Practices Summary

### Do ✅
- Keep CLAUDE.md concise (target 3,000 tokens core)
- Use imports for detailed content
- Update via hooks (automated)
- Version-control with project
- Extract decisions from syntheses
- Link to source artifacts
- Validate token budget weekly

### Don't ❌
- Duplicate content from imports
- Store secrets or credentials
- Let it grow unbounded
- Skip validation checks
- Manual updates (use hooks)
- Hardcode paths (use relative)
- Ignore token budget

---

## Next Steps

1. **Review this spec** - Ensure approach aligns with workflow
2. **Create claude-config.md** - Use template above
3. **Generate initial CLAUDE.md** - From current stage status
4. **Configure hooks** - Automated updates
5. **Validate** - Run validation script
6. **Test** - Start new session, verify context loads

---

## Appendix: Quick Reference

### File Locations
```
.ipe/workflow-config/claude-config.md  ← This artifact
.claude/CLAUDE.md                      ← Generated context file
.claude/CLAUDE.local.md                ← User overrides (optional)
.claude/hooks/update-claude-md.sh      ← Stop hook
.claude/hooks/finalize-stage.sh        ← SessionEnd hook
.claude/hooks/validate-claude-md.sh    ← Validation
```

### Key Commands
```bash
# Quick add memory
> # [your memory text here]

# Edit CLAUDE.md
> /memory

# Validate structure
./.claude/hooks/validate-claude-md.sh

# Check token count
wc -c .claude/CLAUDE.md | awk '{print $1/4}'

# Test import resolution  
grep "^@" .claude/CLAUDE.md | while read i; do ls ${i#@}; done
```

### Import Syntax
```markdown
@.ipe/path/to/artifact.md              # Relative to project
@~/path/to/file.md                     # User home directory  
@/absolute/path/to/file.md             # Absolute path
```

### Hook Triggers
```json
{
  "SessionStart": "Inject context",
  "Stop": "Update active tasks", 
  "SessionEnd": "Finalize stage if complete"
}
```
