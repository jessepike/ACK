# Curate Backlog

Review and maintain the tips backlog, ensuring priorities remain accurate and stale items are addressed.

## Usage

```
/curate-backlog [action] [args]
```

**Actions:**
- `review` (default) - Full curation review
- `promote <title>` - Move item from medium to high priority
- `demote <title>` - Move item from high to medium priority
- `implement <title>` - Mark item as implemented
- `reject <title> <reason>` - Mark item as rejected with reason
- `stale` - List items older than 30 days still in backlog status
- `merge <title1> + <title2>` - Combine two similar items

---

## Action: `review` (Full Curation)

### Step 1: Load Backlog

Read `/Users/jessepike/code/ack/tips.backlog.md` and parse:
- YAML frontmatter
- All insights with their metadata
- Changelog entries

### Step 2: Staleness Analysis

Identify items that are:
- **Stale**: Added > 30 days ago, still `status: backlog`
- **Aging**: Added > 14 days ago, still `status: backlog`

### Step 3: Priority Review

For each HIGH priority item, evaluate:
1. Is this still high impact given current ACK direction?
2. Has this been superseded by another insight?
3. Should this be demoted to medium?

For each MEDIUM priority item, evaluate:
1. Has this become more relevant?
2. Should this be promoted to high?

### Step 4: Duplicate Detection

Scan for items that:
- Have very similar titles
- Cover overlapping concepts
- Could be merged into a single, stronger insight

### Step 5: Present Recommendations

Output a curation report:

```
## Backlog Curation Report

**Date**: {{YYYY-MM-DD}}
**Last curated**: {{previous date or "never"}}

### Staleness
- X items stale (>30 days)
- Y items aging (>14 days)

### Recommended Actions

#### Promotions (medium → high)
- [CATEGORY] Title - reason

#### Demotions (high → medium)
- [CATEGORY] Title - reason

#### Ready to Implement
- [CATEGORY] Title - why it's ready

#### Consider Rejecting
- [CATEGORY] Title - why

#### Potential Merges
- Title1 + Title2 → Suggested merged title

### No Action Needed
- X items reviewed, no changes recommended
```

### Step 6: Await User Decisions

Ask the user which recommendations to apply. Do not make changes without explicit approval.

### Step 7: Apply Changes

For approved changes:
1. Move items between sections as needed
2. Update status fields
3. Update frontmatter counts
4. Add changelog entry for curation

Changelog format for curation:
```markdown
### {{YYYY-MM-DD}} (Curation)
- **Promoted**: List of promoted items
- **Demoted**: List of demoted items
- **Implemented**: List of implemented items
- **Rejected**: List of rejected items with reasons
- **Merged**: List of merged items
```

### Step 8: Update Frontmatter

After changes:
- Update `last_curated` to today's date
- Recalculate `high_priority` and `medium_priority` counts
- Update `total_insights` if items were merged or rejected

---

## Action: `promote <title>`

1. Find the item by title (fuzzy match OK)
2. If in Medium Priority section, move to end of High Priority section
3. Update frontmatter: `high_priority += 1`, `medium_priority -= 1`
4. Add changelog entry

---

## Action: `demote <title>`

1. Find the item by title (fuzzy match OK)
2. If in High Priority section, move to end of Medium Priority section
3. Update frontmatter: `high_priority -= 1`, `medium_priority += 1`
4. Add changelog entry

---

## Action: `implement <title>`

1. Find the item by title
2. Change `- **Status**: backlog` to `- **Status**: implemented`
3. Add `- **Implemented**: {{YYYY-MM-DD}}` field
4. Add changelog entry

---

## Action: `reject <title> <reason>`

1. Find the item by title
2. Change `- **Status**: backlog` to `- **Status**: rejected`
3. Add `- **Rejected**: {{YYYY-MM-DD}} - {{reason}}` field
4. Add changelog entry

---

## Action: `stale`

List all items where:
- `Added` date is > 30 days ago
- `Status` is still `backlog`

Output:
```
## Stale Backlog Items (>30 days)

| Title | Added | Days Old | Priority |
|-------|-------|----------|----------|
| ...   | ...   | ...      | ...      |

Consider: promote, implement, or reject these items.
```

---

## Action: `merge <title1> + <title2>`

1. Find both items by title
2. Present a proposed merged version combining:
   - Best parts of both descriptions
   - Combined applications
   - Higher of the two efforts
   - Higher of the two impacts
3. Await user approval of merged content
4. Remove both original items
5. Add merged item
6. Update frontmatter: `total_insights -= 1`
7. Add changelog entry
