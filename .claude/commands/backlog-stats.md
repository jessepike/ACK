# Backlog Stats

Quick summary statistics for the tips backlog.

## Usage

```
/backlog-stats [view]
```

**Views:**
- (default) - Overview dashboard
- `by-source` - Breakdown by source
- `by-category` - Breakdown by category
- `by-age` - Breakdown by age
- `by-status` - Breakdown by status
- `recent` - Last 7 days activity

---

## Default View: Overview Dashboard

Read `/Users/jessepike/code/ack/tips.backlog.md` and output:

```
## Backlog Dashboard

**Total insights**: N
**High priority**: X | **Medium priority**: Y
**Sources**: Z unique sources

### Health Indicators
- Last updated: YYYY-MM-DD (X days ago)
- Last curated: YYYY-MM-DD (Y days ago) or "never"
- Stale items: N (>30 days in backlog)
- Aging items: M (>14 days in backlog)

### Status Breakdown
- Backlog: X
- In-progress: Y
- Implemented: Z
- Rejected: W

### Category Distribution
| Category | High | Medium | Total |
|----------|------|--------|-------|
| WORKFLOW | X | Y | Z |
| PATTERN | ... | ... | ... |
| TECHNIQUE | ... | ... | ... |
| INTEGRATION | ... | ... | ... |
| ARCHITECTURE | ... | ... | ... |
| TOOL | ... | ... | ... |

### Effort/Impact Matrix
|          | Low Effort | Med Effort | High Effort |
|----------|------------|------------|-------------|
| High Impact | X | Y | Z |
| Med Impact | A | B | C |
| Low Impact | D | E | F |

**Quick wins** (low effort + high impact): N items
```

---

## View: `by-source`

```
## Insights by Source

| Source | Count | High | Medium | Latest |
|--------|-------|------|--------|--------|
| source1 | X | Y | Z | YYYY-MM-DD |
| source2 | ... | ... | ... | ... |

**Most productive source**: source1 (X insights)
**Most recent source**: source2 (YYYY-MM-DD)
```

---

## View: `by-category`

```
## Insights by Category

### WORKFLOW (X total)
High priority:
- Title 1
- Title 2

Medium priority:
- Title 3

### PATTERN (Y total)
...

### TECHNIQUE (Z total)
...

### INTEGRATION (W total)
...

### ARCHITECTURE (V total)
...

### TOOL (U total)
...
```

---

## View: `by-age`

```
## Insights by Age

### Fresh (<7 days): X items
- [CATEGORY] Title (added YYYY-MM-DD)
- ...

### Recent (7-14 days): Y items
- ...

### Aging (14-30 days): Z items
- ...

### Stale (>30 days): W items
- ...

**Average age**: N days
**Oldest item**: Title (X days)
**Newest item**: Title (Y days)
```

---

## View: `by-status`

```
## Insights by Status

### Backlog (X items)
High priority: N
Medium priority: M

### In-Progress (Y items)
- [CATEGORY] Title

### Implemented (Z items)
- [CATEGORY] Title (implemented YYYY-MM-DD)

### Rejected (W items)
- [CATEGORY] Title (rejected YYYY-MM-DD - reason)
```

---

## View: `recent`

```
## Recent Activity (Last 7 Days)

### Added
- YYYY-MM-DD: [CATEGORY] Title (from Source)
- ...

### Status Changes
- YYYY-MM-DD: Title → implemented
- ...

### Changelog Entries
- YYYY-MM-DD: Source - X high, Y medium added
- ...

**This week**: X added, Y implemented, Z rejected
```
