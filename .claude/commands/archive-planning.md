# Archive Planning

Archive support artifacts from planning stages to keep the repository clean during development.

## Usage

```
/archive-planning [action]
```

**Actions:**
- (default) - Interactive archive with confirmation
- `preview` - Show what would be archived without changes
- `force` - Archive immediately without confirmation
- `restore` - Restore archived files back to `.ack/`

---

## What This Does

Moves support artifacts from `.ack/` to `~/.ack/archives/{project-name}/`.

**Why archive?**
- Keeps the repo clean during Develop stage
- Prevents agents from reading outdated research/planning docs
- Preserves artifacts for future reference
- Leaves a manifest pointing to archive location

**What gets archived:**
- Support artifacts (research, validation, concept drafts)
- NOT deliverables (those live in `docs/`)

---

## Archive Trigger

This skill is typically run when advancing from Setup to Develop:

```
/advance-stage develop
```

The advance skill offers to run `/archive-planning` automatically.

You can also run it manually at any time during or after development.

---

## Process

### Step 1: Identify Project

Determine project name for archive path:

1. Check `.ack/state.json` for project name
2. Fall back to git repo name: `basename $(git rev-parse --show-toplevel)`
3. Fall back to current directory name

### Step 2: Scan for Support Artifacts

Find all support artifacts in `.ack/`:

| Stage | Support Artifacts |
|-------|-------------------|
| discover | `concept.md`, `research.md`, `validation.md` |
| design | `context-schema.md`, `dependencies.md` |
| setup | `repo-init.md`, `scaffolding.md`, `ci-cd.md`, `testing.md`, `git-workflow.md` |

Also include:
- Any drafts or iterations (e.g., `brief-v1.md`, `concept-draft.md`)
- Working notes or scratch files
- Stage state files (but NOT root `state.json`)

**Exclude from archive:**
- Deliverables (they should already be in `docs/`)
- `.ack/state.json` (needed for tracking)
- `.ack/archives-manifest.md` (reference file)

### Step 3: Show Preview

```markdown
## Archive Preview

**Project:** {project-name}
**Archive location:** ~/.ack/archives/{project-name}/

**Files to archive:**

### From .ack/discover/
- [ ] concept.md (12 KB)
- [ ] research.md (8 KB)
- [ ] validation.md (5 KB)

### From .ack/design/
- [ ] context-schema.md (3 KB)
- [ ] dependencies.md (4 KB)

### From .ack/setup/
- [ ] repo-init.md (2 KB)
- [ ] scaffolding.md (6 KB)
- [ ] ci-cd.md (4 KB)
- [ ] testing.md (5 KB)
- [ ] git-workflow.md (3 KB)

**Total:** 10 files, 52 KB

**Proceed with archive?** (yes/no)
```

If `preview` action, stop here.
If `force` action, skip confirmation.

### Step 4: Create Archive Directory

```bash
mkdir -p ~/.ack/archives/{project-name}/discover
mkdir -p ~/.ack/archives/{project-name}/design
mkdir -p ~/.ack/archives/{project-name}/setup
```

### Step 5: Move Files

Move each support artifact to archive:

```bash
mv .ack/discover/concept.md ~/.ack/archives/{project-name}/discover/
mv .ack/discover/research.md ~/.ack/archives/{project-name}/discover/
# ... etc
```

Preserve directory structure in archive.

### Step 6: Create Archive Manifest

Create `.ack/archives-manifest.md`:

```markdown
---
type: "manifest"
description: "Archive manifest for planning artifacts"
version: "1.0.0"
updated: "{timestamp}"
---

# Archives Manifest

**Project:** {project-name}
**Archived:** {timestamp}
**Archive location:** ~/.ack/archives/{project-name}/

## Archived Files

### Discover Stage
- concept.md
- research.md
- validation.md

### Design Stage
- context-schema.md
- dependencies.md

### Setup Stage
- repo-init.md
- scaffolding.md
- ci-cd.md
- testing.md
- git-workflow.md

## Restore Command

To restore archived files:
```
/archive-planning restore
```

Or manually:
```bash
cp -r ~/.ack/archives/{project-name}/* .ack/
```
```

### Step 7: Clean Up Empty Directories

Remove empty stage directories from `.ack/`:

```bash
rmdir .ack/discover 2>/dev/null || true
rmdir .ack/design 2>/dev/null || true
rmdir .ack/setup 2>/dev/null || true
```

### Step 8: Report Success

```markdown
## Archive Complete

**Archived:** 10 files (52 KB)
**Location:** ~/.ack/archives/{project-name}/

**Manifest:** .ack/archives-manifest.md

The repository is now clean for development.
Deliverables remain in `docs/`.

**To restore:** `/archive-planning restore`
```

---

## Action: `restore`

Restore archived files back to `.ack/`.

### Process

1. Read `.ack/archives-manifest.md` for archive location
2. Show files that will be restored
3. Confirm with user
4. Copy files from archive back to `.ack/`
5. Update manifest with restore timestamp

```markdown
## Restore Preview

**Archive location:** ~/.ack/archives/{project-name}/

**Files to restore:**

### To .ack/discover/
- concept.md
- research.md
- validation.md

### To .ack/design/
- context-schema.md
- dependencies.md

**Proceed with restore?** (yes/no)
```

**Note:** Restore copies files, doesn't move them. Archive remains intact.

---

## What Stays in .ack/

After archiving:

```
.ack/
├── state.json              # Stage tracking (preserved)
├── archives-manifest.md    # Points to archive (created)
└── develop/                # Current stage work (if any)
```

---

## Archive Structure

```
~/.ack/archives/
└── {project-name}/
    ├── discover/
    │   ├── concept.md
    │   ├── research.md
    │   └── validation.md
    ├── design/
    │   ├── context-schema.md
    │   └── dependencies.md
    └── setup/
        ├── repo-init.md
        ├── scaffolding.md
        ├── ci-cd.md
        ├── testing.md
        └── git-workflow.md
```

---

## Why Archive Outside the Project?

**Problem:** Agents work within the project directory. If support artifacts remain in the project (even in `.ack/`), agents might read outdated research and get confused.

**Solution:** Archive to `~/.ack/archives/` which is:
- Outside the project directory
- Not accessible to agents working in the repo
- Still available for human reference
- Easily restorable if needed

---

## Examples

### Preview What Would Be Archived

```
/archive-planning preview
```

Shows list of files without making changes.

### Archive with Confirmation

```
/archive-planning
```

Shows preview, asks for confirmation, then archives.

### Archive Immediately

```
/archive-planning force
```

Archives without asking for confirmation.

### Restore Archived Files

```
/archive-planning restore
```

Copies files from archive back to `.ack/`.

---

## Related Commands

- `/advance-stage develop` - Triggers archive offer automatically
- `/init-project` - Sets up `.ack/` structure initially
- `/validate-stage` - Check stage completion before archiving
