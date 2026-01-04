# Extract Insights

Analyze the source provided in `$ARGUMENTS` and extract actionable insights for the ACK project, then append new (non-duplicate) insights to the backlog.

## Step 1: Determine Source Type

- If `$ARGUMENTS` starts with `http://` or `https://` → **URL** (use WebFetch)
- Otherwise → **Local file path** (use Read tool)

## Step 2: Read Existing Backlog

Read `/Users/jessepike/code/ack/tips.backlog.md` and extract:
- YAML frontmatter values (total_insights, high_priority, medium_priority, sources_count)
- All existing insight titles (the `### [CATEGORY] Title` lines) for duplicate detection

## Step 3: Extract Insights

Analyze the source content and extract up to **7 actionable insights** for ACK (AI-assisted development toolkit with memory, governance, and registry components).

For each insight, determine:

| Field | Format |
|-------|--------|
| Category | `WORKFLOW` \| `PATTERN` \| `TECHNIQUE` \| `INTEGRATION` \| `ARCHITECTURE` \| `TOOL` |
| Title | Brief name (5 words max) |
| Description | What it is and how it works (2-3 sentences) |
| Application | Specific way to apply this to ACK (be concrete) |
| Effort | `low` \| `medium` \| `high` |
| Impact | `low` \| `medium` \| `high` |

### Prioritization Criteria

Focus on insights that:
- Reduce friction in AI-assisted development workflows
- Improve context/memory management for AI coding assistants
- Enhance artifact governance or validation
- Streamline project scaffolding or templates
- Enable better human-AI collaboration patterns

### Constraints

- Maximum 7 insights (quality over quantity)
- Skip generic advice—only specific, implementable ideas
- Ignore content unrelated to development tooling, AI assistance, or project management

## Step 4: Filter Duplicates

Compare each extracted insight title against existing backlog titles. Skip insights that:
- Have identical titles
- Cover the same concept (fuzzy match—similar meaning counts as duplicate)

Track which insights were skipped and why.

## Step 5: Append to Backlog

For each **new** insight, append to `tips.backlog.md`:

- **High Impact** → insert at end of `## High Priority` section (before the `---` separator)
- **Medium/Low Impact** → insert at end of `## Medium Priority` section (before the `---` separator)

Use this exact format (note the `Added` field with today's date):
```markdown
### [CATEGORY] Title Here
- **Source**: {{source name or URL}}
- **Added**: {{YYYY-MM-DD}}
- **Description**: Description here.
- **Application**: Application here.
- **Effort**: low | **Impact**: high
- **Status**: backlog
```

## Step 6: Update Frontmatter

Update the YAML frontmatter at the top of the file:
- Increment `total_insights` by number of new insights added
- Increment `high_priority` by number of high-impact insights added
- Increment `medium_priority` by number of medium/low-impact insights added
- Update `last_updated` to today's date (YYYY-MM-DD)
- Increment `sources_count` by 1

## Step 7: Append to Changelog

Add a new entry at the TOP of the `## Changelog` section (newest first):

```markdown
### {{YYYY-MM-DD}}
- **Source**: {{source name or URL}}
- **Added**: X high priority, Y medium priority
- **Skipped**: Z duplicates (brief reason)
- **New insights**: Comma-separated list of new insight titles
```

## Step 8: Report Summary

Output a summary to the user:

```
## Insights Extraction Complete

**Source**: {{source}}
**Date**: {{YYYY-MM-DD}}
**Added**: X high priority, Y medium priority
**Skipped**: Z duplicates

### New Insights Added:
- [CATEGORY] Title 1
- [CATEGORY] Title 2
...

### Skipped (duplicates):
- Title → reason

**Backlog totals**: N high priority, M medium priority (T total)
```
