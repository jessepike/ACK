# IPE Artifact Schema Specification

---

**Version:** 1.0  
**Created:** 2024-12-31  
**Status:** Foundational Specification

---

## Overview

This document defines the foundational schema for all IPE (Integrated Planning Environment) artifacts. This schema is **built into IPE** and applies uniformly across all stages and all projects. It ensures consistency, enables automation, and supports the governance model.

**Scope:** IPE planning artifacts only (concept.md, stack.md, etc.)
**Out of Scope:** Project-specific documentation schemas (defined in context-schema.md)

---

## Design Principles

**Consistency:** All artifacts follow the same structure
**Simplicity:** Minimal required fields, maximum clarity
**Traceability:** Full audit trail and version control
**Human-readable:** Markdown-first, git-friendly
**Agent-parseable:** Structured frontmatter enables automation

---

## 1. YAML Frontmatter

### Required Fields

Every IPE artifact MUST include these fields:

```yaml
---
status: not-started | draft | complete | finalized
stage: discovery | solution-design | environment-setup | workflow-config | implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: []
---
```

### Optional Fields

```yaml
version: X.Y.Z  # Required when status=finalized, otherwise omitted
tags: []        # User-defined labels for categorization
priority: low | medium | high | critical
```

### Field Specifications

#### status

**Type:** Enum  
**Required:** Yes  
**Default:** `not-started`

**Values:**
- `not-started` - Artifact created (pre-templated) but no content added
- `draft` - User has added/edited content
- `complete` - All required sections marked complete, awaiting finalization
- `finalized` - Human approved, locked, versioned (source of record)

**Transitions:**
```
not-started → draft       (automatic on first edit)
draft → complete          (when all sections checked)
complete → finalized      (explicit user action)
finalized → draft         (only via change order, bumps version)
```

**Visual Indicators:**
- `not-started`: Red text
- `draft`: Orange text  
- `complete`: Green text
- `finalized`: Green text + lock icon

#### stage

**Type:** Enum  
**Required:** Yes

**Values:**
- `discovery`
- `solution-design`
- `environment-setup`
- `workflow-config`
- `implementation`

**Usage:** Indicates which IPE stage this artifact belongs to. Determines directory location and available templates.

#### created

**Type:** ISO Date + Author  
**Required:** Yes  
**Format:** `YYYY-MM-DD [AuthorName]`

**Examples:**
```yaml
created: 2024-12-31 [Human]
created: 2024-12-31 [Claude]
created: 2024-12-31 [ResearchAgent]
```

**Rules:**
- Date is artifact file creation date
- Author is entity that created the artifact
- Immutable (never changes)

#### updated

**Type:** ISO Date + Author  
**Required:** Yes  
**Format:** `YYYY-MM-DD [AuthorName]`

**Examples:**
```yaml
updated: 2024-12-31 [Human]
updated: 2024-12-31 [Claude]
```

**Rules:**
- Date is last modification date
- Author is entity that made last modification
- Updates on every save
- Can be different from creator

#### related

**Type:** Array of filenames  
**Required:** Yes (can be empty)  
**Format:** `[filename.md, other-file.md]`

**Examples:**
```yaml
related: []
related: [concept.md]
related: [concept.md, research.md, stack.md]
```

**Rules:**
- References other IPE artifacts
- Filenames only (no paths)
- Can reference artifacts in same or previous stages
- Cannot reference future stages
- Used for dependency tracking and cross-references

#### version

**Type:** Semver (X.Y.Z)  
**Required:** Only when `status=finalized`  
**Format:** `X.Y.Z`

**Examples:**
```yaml
version: 1.0.0  # Initial finalization
version: 1.1.0  # Minor change
version: 2.0.0  # Breaking change
```

**Versioning Rules (Semver):**
- **Major (X):** Breaking changes that invalidate downstream work
- **Minor (Y):** Non-breaking additions or modifications
- **Patch (Z):** Corrections, clarifications, typo fixes

**Version Lifecycle:**
1. Artifact in `draft` or `complete`: No version field
2. Human finalizes → version becomes `1.0.0`
3. Change order applied → version increments per semver rules
4. Version never decreases

#### tags

**Type:** Array of strings  
**Required:** No  
**Format:** `[tag1, tag2]`

**Examples:**
```yaml
tags: [mvp, critical, needs-review]
tags: [backend, database]
```

**Usage:** User-defined labels for filtering, searching, categorization

#### priority

**Type:** Enum  
**Required:** No  
**Values:** `low | medium | high | critical`

**Usage:** Helps users triage work across artifacts

---

## 2. Section Structure

### Section Definition

Sections are Markdown H2 headers (`##`) that divide artifact content into logical, independently completable units.

```markdown
## Section Name

Content here...
```

### Section Rules

**Header Level:**
- Sections MUST use H2 (`##`)
- Subsections within content can use H3-H6
- Only H2 headers are "completable sections"

**Completion:**
- Each section has independent completion state
- User manually marks sections complete
- No automatic completion
- Visual indicator: ○ (incomplete) or ● (complete)

**Collapsibility:**
- All sections can collapse/expand
- Default: collapsed on document open
- Current section auto-expands when editing

**Templates:**
- Each artifact type has predefined section headers
- Sections include guidance comments when empty
- Users can add custom sections
- Template sections should be addressed (can be marked N/A)

**Example Template Section:**

```markdown
## Problem Being Solved
<!-- What pain point does this address? Be specific about who experiences this problem and when. -->

```

### Content Rules Within Sections

**Allowed Markdown:**
- Paragraphs
- Headers (H3-H6)
- Lists (ordered, unordered)
- Code blocks (fenced with language identifier)
- Links (internal, external)
- Tables
- Blockquotes
- Horizontal rules

**Restricted Elements:**
- No embedded HTML (security)
- No inline scripts
- No external resource embedding (images referenced, not embedded)

**Code Blocks:**
```markdown
```javascript
// Code example
const example = "supported";
```
```

- Language identifier required for syntax awareness
- No syntax highlighting in editor (minimal IDE overlap)
- Proper rendering in preview mode

---

## 3. Cross-Reference Format

### YAML Frontmatter References

**In `related` field:**

```yaml
related: [concept.md, research.md]
```

**Rules:**
- Filename only (no path)
- IPE resolves to correct stage directory
- Validates existence on save
- Creates bidirectional links

### Markdown Content References

**Standard markdown links:**

```markdown
See [concept definition](concept.md) for background.

Based on [research findings](research.md#market-landscape).
```

**Rules:**
- Standard markdown link syntax
- Relative paths (filename only for same stage)
- Can include section anchors (#section-name)
- Broken link detection in validation

**Future Enhancement (Backlog):**

Wiki-style links:
```markdown
See [[concept.md]] for background.
```

Auto-linking and preview on hover.

---

## 4. File Naming Conventions

### Artifact Filenames

**Format:** `artifact-name.md`

**Rules:**
- Lowercase only
- Hyphens for word separation (no underscores, spaces)
- Alphanumeric characters only (a-z, 0-9, -)
- `.md` extension required
- Max 50 characters
- Descriptive, not generic

**Valid Examples:**
```
concept.md
stack-decisions.md
api-architecture.md
discovery-synthesis.md
context-schema.md
```

**Invalid Examples:**
```
Concept.md           # Capital letters
stack decisions.md   # Spaces
stack_decisions.md   # Underscores
concept.MD           # Uppercase extension
file1.md            # Generic name
very-long-artifact-name-that-exceeds-fifty-characters.md  # Too long
```

### Change Order Filenames

**Format:** `CO-XXX-artifact-name-vX.X.X-to-vX.X.X.md`

**Example:**
```
CO-001-concept-v1.0.0-to-v1.1.0.md
CO-042-stack-decisions-v2.1.0-to-v3.0.0.md
```

**Rules:**
- Sequential numbering (CO-001, CO-002, etc.)
- Includes artifact name
- Includes version transition
- Stored in `.change-orders/` directory

---

## 5. Directory Structure

### Project Layout

```
project-root/
├── .ipe/
│   ├── config.json              # IPE project metadata
│   ├── validation-rules.yml     # Custom validation configuration
│   └── state.json               # Current project state (active stage, etc.)
│
├── discovery/
│   ├── concept.md
│   ├── research.md
│   ├── validation.md
│   ├── scope.md
│   ├── discovery-synthesis.md
│   ├── reviews/
│   │   ├── claude-opus-review.md
│   │   ├── gemini-review.md
│   │   └── chatgpt-review.md
│   └── .change-orders/
│       ├── index.md
│       └── CO-001-concept-v1.0.0-to-v1.1.0.md
│
├── solution-design/
│   ├── stack.md
│   ├── architecture.md
│   ├── data-model.md
│   ├── context-schema.md
│   ├── technical-spec-synthesis.md
│   └── .change-orders/
│       └── index.md
│
├── environment-setup/
│   └── [artifacts TBD]
│
├── workflow-config/
│   └── [artifacts TBD]
│
├── implementation/
│   └── [artifacts TBD]
│
├── resources/                    # Shared across all stages
│   ├── competitor-analysis.pdf
│   ├── market-report.md
│   └── diagrams/
│
└── README.md                     # Project overview
```

### Directory Rules

**Stage Directories:**
- One directory per stage
- Named exactly as stage enum value (lowercase, hyphenated)
- Contains only artifacts for that stage
- Includes `.change-orders/` subdirectory

**`.ipe/` Directory:**
- Hidden directory (git-tracked)
- Contains IPE project configuration
- Not user-editable (managed by IPE)

**`resources/` Directory:**
- Shared assets across all stages
- Any file type allowed
- Organized by subdirectories as needed
- Referenced from artifacts but not IPE artifacts themselves

**`.change-orders/` Subdirectory:**
- One per stage directory
- Contains change order history for that stage's artifacts
- `index.md` provides chronological timeline
- Individual CO files named per convention

---

## 6. Version Control Integration

### Git Workflow

**IPE projects are git repositories:**
- All artifacts tracked in version control
- Change orders create git commits
- Full audit trail through git history

### Change Order Process

**When finalized artifact needs modification:**

1. **Create Change Order Document**
   - Agent/user creates CO-XXX.md in `.change-orders/`
   - Populates template with reason, impact analysis
   - Status: `draft`

2. **Make Changes**
   - Edit artifact content
   - Update `updated` field in frontmatter
   - Increment `version` field per semver rules

3. **Git Commit**
   - Stage modified artifact
   - Create commit with standard message format
   - Capture commit SHA

4. **Update Change Order**
   - Add git commit SHA(s) to change order
   - Document exact changes made
   - Update audit trail
   - Status: `applied`

5. **File Change Order**
   - Save change order document
   - Update `.change-orders/index.md`
   - Commit change order files

### Git Commit Message Format

**Standard format for change orders:**

```
[IPE] Change Order #XXX: artifact-name vX.X.X → vX.X.X

[Reason for change - one line summary]

Files changed:
- stage/artifact-name.md
```

**Example:**

```
[IPE] Change Order #001: concept v1.0.0 → v1.1.0

Adjusted scope based on API rate limit constraints

Files changed:
- discovery/concept.md
```

### Change Order Template

See full template in Section 8.

---

## 7. Validation Rules

### Artifact Validation

**On save, IPE validates:**

**Frontmatter:**
- All required fields present
- Field values match allowed enums
- Dates in correct format
- Version follows semver (if present)

**Cross-References:**
- Files referenced in `related` exist
- Markdown links point to valid files
- No forward references (to future stages)

**Content:**
- Sections follow template (warnings for missing)
- No malicious content (HTML, scripts)
- Code blocks have language identifiers

**File System:**
- Filename follows conventions
- File in correct stage directory
- No duplicate filenames

### Stage Completion Validation

**Before marking stage complete:**

**Discovery-specific:**
- All 4 core artifacts finalized
- Synthesis document generated
- Agent validation passed
- No broken references

**Per-stage rules:**
- Defined in stage specifications
- Configurable in `.ipe/validation-rules.yml`

### Agent Validation

**Automated checks:**
- Gap analysis (missing critical elements)
- Consistency review (conflicting statements)
- Completeness check (all sections addressed)
- Quality threshold (meets standards)

**Configurable:**
```yaml
# .ipe/validation-rules.yml
validation_rules:
  - check: gap_analysis
    enabled: true
  - check: consistency_review
    enabled: true
  # User can add custom rules
```

---

## 8. Change Order Schema

### Change Order Document Structure

```yaml
---
change-order-id: CO-XXX
artifact: stage/artifact-name.md
previous-version: X.X.X
new-version: X.X.X
date: YYYY-MM-DDTHH:MM:SSZ
author: AuthorName
git-commits: 
  - sha: abc123def
  - sha: 456ghi789
status: draft | applied
---

# Change Order CO-XXX

## Artifact
**File:** `stage/artifact-name.md`  
**Version:** X.X.X → X.X.X  
**Date:** YYYY-MM-DD  
**Author:** AuthorName

## Reason for Change
[Human-provided rationale for modification]

## Changes Made
[Detailed description of modifications]

### Section: [section-name]
- Before: [original content/approach]
- After: [new content/approach]
- Rationale: [why this change]

## Impact Analysis
- **Affects:** [list of related artifacts that may need review]
- **Dependencies:** [artifacts that depend on this one]
- **Breaking:** [Yes/No - does this invalidate downstream work?]
- **Mitigation:** [if breaking, how to address]

## Git Commits
- [abc123d](link-to-commit) - [commit message]
- [456ghi7](link-to-commit) - [commit message]

## Review
- **Requested by:** [Human]
- **Executed by:** [Agent/Human]
- **Approved by:** [Human]
- **Approval Date:** YYYY-MM-DDTHH:MM:SSZ
- **Notes:** [Optional review comments]

## Audit Trail
- YYYY-MM-DD HH:MM - Change order created
- YYYY-MM-DD HH:MM - Changes applied to artifact
- YYYY-MM-DD HH:MM - Git commit [sha] created
- YYYY-MM-DD HH:MM - Change order approved and applied
```

### Change Order Index

**File:** `.change-orders/index.md`

**Format:**

```markdown
# Change Order History - [stage-name]

## artifact-name.md

**v1.2.0** (Current)
- [CO-002](CO-002-artifact-v1.1.0-to-v1.2.0.md) - 2024-12-31 - Brief description

**v1.1.0**
- [CO-001](CO-001-artifact-v1.0.0-to-v1.1.0.md) - 2024-12-30 - Brief description

**v1.0.0** (Initial)
- 2024-12-29 - Original finalization

## other-artifact.md

[Similar timeline]
```

---

## 9. Status Icons & Visual System

### Section Completion Icons

**Style:** Minimalist circles

**States:**
- `○` Empty circle (light gray) - Incomplete
- `●` Filled circle (status-color) - Complete

**Colors:**
- Incomplete: `#808080` (gray)
- Complete: `#4caf50` (green)

### Artifact Status Indicators

**In file browser:**

**not-started:**
- No icon
- Red text (#f44336)

**draft:**
- Small gray dot
- Orange text (#ff9800)

**complete:**
- Small filled dot
- Green text (#4caf50)

**finalized:**
- Small lock icon (🔒)
- Green text (#4caf50)

### Stage Status Indicators

**In stage tabs:**

**Active:**
- Blue background (#007acc)
- White text
- Bold font

**Completed:**
- Green checkmark (✓)
- Gray background
- Green count

**In Progress:**
- Orange count
- Gray background

**Not Started:**
- Red count
- Gray background

---

## 10. Template System

### Artifact Templates

**Each artifact type has a template:**

**Template location:** Built into IPE (not user-editable for core templates)

**Template structure:**

```yaml
---
# Metadata filled by IPE on creation
status: not-started
stage: [auto-populated]
created: [auto-populated]
updated: [auto-populated]
related: []
---

# [Artifact Title]

## Section One
<!-- Guidance: What goes in this section -->

## Section Two
<!-- Guidance: What to consider here -->

## Section Three
<!-- Guidance: Key questions to answer -->
```

**Templates include:**
- All required YAML frontmatter (auto-populated)
- Predefined section headers
- Guidance comments (HTML comments, not visible in render)
- Empty content areas

**User interaction:**
- Click section to expand
- Read guidance
- Replace/remove guidance comment with actual content
- Mark section complete when done

### Custom Templates (Future)

Users can create custom artifact types with their own templates.

**Location:** `.ipe/templates/custom/`

**Not MVP** - Backlog feature

---

## 11. Data Types & Validation

### Field Type Specifications

| Field | Type | Format | Validation |
|-------|------|--------|------------|
| status | enum | String | Must be one of: not-started, draft, complete, finalized |
| stage | enum | String | Must be one of: discovery, solution-design, environment-setup, workflow-config, implementation |
| created | datetime+author | `YYYY-MM-DD [Author]` | Valid ISO date, author in brackets |
| updated | datetime+author | `YYYY-MM-DD [Author]` | Valid ISO date, author in brackets, >= created date |
| related | array | `[file1.md, file2.md]` | Valid filenames, files must exist, no forward references |
| version | semver | `X.Y.Z` | Valid semver, required when finalized, auto-increments |
| tags | array | `[tag1, tag2]` | Optional, strings only |
| priority | enum | String | Optional, one of: low, medium, high, critical |

### Validation Error Handling

**On validation failure:**

**UI:**
- Red border around invalid field
- Error message tooltip
- Prevent save until resolved

**Examples:**
- "Status 'Done' is not valid. Use: not-started, draft, complete, or finalized"
- "File 'missing.md' referenced in 'related' does not exist"
- "Updated date cannot be before created date"
- "Version required when status is 'finalized'"

---

## 12. Migration & Backwards Compatibility

### Schema Version

**IPE tracks its own schema version:**

```json
// .ipe/config.json
{
  "ipe_version": "1.0.0",
  "schema_version": "1.0.0",
  "project_name": "IPE-demo",
  "created": "2024-12-31"
}
```

### Future Schema Changes

**Breaking changes:**
- Increment major version (2.0.0)
- Provide migration tool
- Warn users before upgrading

**Non-breaking changes:**
- Add optional fields (minor version)
- Extend enum values (minor version)
- Improve validation (patch version)

**Migration strategy:**
- Detect old schema version
- Offer to migrate
- Create backup before migration
- Log all changes

---

## 13. Extension Points

### Custom Fields (Future)

**Users may want project-specific metadata:**

```yaml
---
# Standard IPE fields
status: draft
stage: discovery

# Custom fields (future)
custom:
  client: "Acme Corp"
  budget: "$50k"
  deadline: "2025-Q2"
---
```

**Not MVP** - Custom fields in backlog

### Plugin System (Future)

**Allow third-party extensions:**
- Custom validation rules
- Additional artifact types
- Integration with external tools
- Custom synthesis formats

**Not MVP** - Backlog feature

---

## Appendix A: Complete Example Artifact

```yaml
---
status: finalized
stage: discovery
created: 2024-12-30 [Human]
updated: 2024-12-31 [Claude]
related: [research.md, validation.md]
version: 1.1.0
tags: [mvp, core]
priority: critical
---

# Concept Definition

## What Is It?
<!-- One sentence elevator pitch -->

IPE (Integrated Planning Environment) is a planning layer that orchestrates AI-augmented development from concept to implementation-ready state.

## Problem Being Solved
<!-- What pain point does this address? -->

AI-augmented solo developers lack a unified environment for pre-implementation planning. The IDE handles code execution, but critical upstream work—research, architecture decisions, context management, agent orchestration, tooling selection—happens in scattered CLIs, docs, and mental models.

This fragmentation causes:
- Context loss between planning and implementation
- Inconsistent project scaffolding and documentation
- Manual agent/tool configuration per project
- No systematic handoff from planning to IDE

## Core Features
<!-- 3-5 essential capabilities -->

- Living documentation with version control and change management
- Agent orchestration interface for human + AI collaboration
- Context architecture with structured artifact schemas
- Environment manifest tracking of tooling and configs
- Implementation planning with hierarchical task breakdown

## Value Proposition
<!-- Why would someone use this? -->

Reduces concept-to-implementation time by 40% through systematic planning workflows and reusable patterns. Eliminates manual project setup. Provides clear audit trail for all technical decisions.

## Target User
<!-- Who is this for? Be specific. -->

Solo AI-augmented developers who:
- Build with AI coding tools (Claude Code, Cursor, etc.)
- Manage multiple projects with complex context requirements
- Need reproducible project scaffolding patterns
- Want systematic agent coordination across development phases

## Success Looks Like
<!-- How do you know this worked? -->

- Developer has complete technical specification before writing code
- All planning decisions documented with rationale
- Zero context loss transitioning to implementation
- Reusable templates for future projects

## Out of Scope (MVP)
<!-- What are we explicitly NOT doing? -->

- Not building: IDE replacement, code execution, deployment
- Not supporting: Team collaboration, real-time multi-user editing
- Not handling: Post-development operations (monitoring, incidents)
- Not optimizing for: Non-technical stakeholders, waterfall processes
```

---

## Appendix B: Validation Checklist

**Before finalizing any artifact:**

- [ ] All required YAML fields present and valid
- [ ] Status transitions followed correctly
- [ ] All template sections addressed (or marked N/A)
- [ ] Cross-references valid and bidirectional
- [ ] Filename follows conventions
- [ ] File in correct stage directory
- [ ] No broken links
- [ ] Code blocks have language identifiers
- [ ] Content free of HTML/scripts
- [ ] Human review completed
- [ ] Agent validation passed (if applicable)

---

**End of IPE Artifact Schema Specification**
