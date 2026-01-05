# Init Project

Initialize a new ACK project with the standard working directory structure.

## Usage

```
/init-project [project-name]
```

**Arguments:**
- `project-name` (optional) - Name for the project. Defaults to current directory name.

---

## What This Does

Creates the ACK working directory structure:

```
.ack/
├── discover/           # Stage 1 working directory
├── state.json          # Stage tracking
└── .gitignore          # Ignore working files
```

Also:
- Creates `docs/` for deliverables
- Adds `.ack/` to project `.gitignore`
- Sets initial stage to "discover"

---

## Process

### Step 1: Check Prerequisites

Verify we're in a valid project directory:

```markdown
## Pre-flight Check

- [ ] In a git repository (or will init one)
- [ ] Not already an ACK project (.ack/ doesn't exist)
- [ ] Has write permissions
```

If `.ack/` already exists:
```markdown
## Already Initialized

This project already has an ACK structure at `.ack/`.

**Current stage:** {from state.json}

**Options:**
- Continue working in current stage
- `/advance-stage <stage>` to move forward
- Delete `.ack/` and re-run `/init-project` to start fresh
```

### Step 2: Confirm Project Name

```markdown
## Initialize ACK Project

**Project name:** {project-name}
**Location:** {current directory}

**This will create:**
```
.ack/
├── discover/
└── state.json

docs/
└── (deliverables will go here)
```

**Proceed?** (yes/no)
```

### Step 3: Create Directory Structure

```bash
# Create ACK working directory
mkdir -p .ack/discover

# Create docs directory for deliverables
mkdir -p docs
```

### Step 4: Create State File

Create `.ack/state.json`:

```json
{
  "projectName": "{project-name}",
  "currentStage": "discover",
  "startedAt": "{ISO timestamp}",
  "stageHistory": []
}
```

### Step 5: Create ACK .gitignore

Create `.ack/.gitignore`:

```gitignore
# ACK working files
# These are working documents, not version controlled
# Deliverables go to /docs and ARE version controlled

# Ignore all working files by default
*

# But track these
!.gitignore
!state.json
!archives-manifest.md
```

### Step 6: Update Project .gitignore

Append to project root `.gitignore` (create if doesn't exist):

```gitignore
# ACK working directory
# Working documents during planning (not version controlled)
# Deliverables are in /docs (version controlled)
.ack/discover/
.ack/design/
.ack/setup/
.ack/develop/
```

### Step 7: Create Initial Brief Template

Copy brief template to working directory:

```bash
cp ack-src/stages/discover/templates/brief.md .ack/discover/brief.md
```

Or if ACK templates aren't available, create a minimal brief:

```markdown
---
type: "project_brief"
description: "{project-name} project brief"
version: "0.1.0"
updated: "{timestamp}"
status: draft
---

# {Project Name} - Brief

## Problem Statement

<!-- What problem are we solving? -->

## Target Users

<!-- Who has this problem? -->

## Solution Overview

<!-- How will we solve it? -->

## Success Criteria

<!-- How do we know it worked? -->

## Scope

### In Scope

-

### Out of Scope

-

## Constraints

<!-- Time, budget, technical limitations -->
```

### Step 8: Report Success

```markdown
## ACK Project Initialized

**Project:** {project-name}
**Stage:** Discover

**Created:**
```
.ack/
├── discover/
│   └── brief.md (template)
└── state.json

docs/
└── (empty - deliverables go here)
```

**Next steps:**

1. **Edit the brief:**
   ```
   .ack/discover/brief.md
   ```

2. **Add supporting research (optional):**
   - Copy `concept.md` template for working ideas
   - Copy `research.md` template for market research
   - Copy `validation.md` template for user validation

3. **When ready, review and validate:**
   ```
   /review-stage discover
   /validate-stage discover
   ```

4. **Then advance to Design:**
   ```
   /advance-stage design
   ```

**Templates available at:**
`ack-src/stages/discover/templates/`
```

---

## Options

### Initialize Without Git

If not in a git repo:

```markdown
## No Git Repository

This directory is not a git repository.

**Options:**
1. Initialize git now (`git init`)
2. Continue without git (not recommended)
3. Cancel and navigate to a git repo

**Choice?** (init/continue/cancel)
```

If "init": Run `git init` then continue.

### Initialize in Subdirectory

If user specifies a path:

```
/init-project my-project ./projects/my-project
```

1. Create the directory if it doesn't exist
2. Change to that directory
3. Run normal initialization

---

## Templates Location

The skill looks for ACK templates in this order:

1. `./ack-src/stages/` (if in ACK repo itself)
2. `~/.ack/templates/` (user-installed templates)
3. Built-in minimal templates (fallback)

---

## Project Structure After Init

```
project/
├── .ack/                    # ACK working directory
│   ├── discover/            # Current stage
│   │   └── brief.md         # Working on this
│   ├── state.json           # Stage tracking
│   └── .gitignore           # Ignore working files
├── docs/                    # Deliverables (empty initially)
├── .gitignore               # Updated with ACK entries
└── [existing project files]
```

---

## Full Workflow After Init

```bash
# 1. Initialize
/init-project my-app

# 2. Work on Discover stage
#    Edit .ack/discover/brief.md
#    Optionally add research.md, validation.md

# 3. Review and validate
/review-stage discover
/validate-stage discover

# 4. Advance to Design
/advance-stage design
#    → brief.md moves to docs/
#    → .ack/design/ created

# 5. Work on Design stage
#    Create architecture.md, data-model.md, stack.md

# 6. Continue through stages...
/advance-stage setup
/advance-stage develop

# 7. Archive planning artifacts
/archive-planning
#    → Support files move to ~/.ack/archives/my-app/
```

---

## Reinitializing

To start fresh:

```bash
# Remove existing ACK structure
rm -rf .ack/

# Reinitialize
/init-project
```

**Warning:** This deletes all working documents in `.ack/`. Deliverables in `docs/` are preserved.

---

## Examples

### Basic Initialization

```
/init-project
```

Uses current directory name as project name.

### Named Project

```
/init-project my-awesome-app
```

Sets project name to "my-awesome-app".

### Check Status After Init

```
/validate-stage discover
```

Will show brief.md exists but needs content.

---

## Related Commands

- `/validate-stage discover` - Check if brief is ready
- `/review-stage discover` - Review brief content
- `/advance-stage design` - Move to next stage
- `/archive-planning` - Archive at end of planning
