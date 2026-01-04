---
type: artifact
stage: design
artifact: data-model
description: "Database schema, entity relationships, and data access patterns"
version: 1.0.0
updated: "2026-01-04T09:26:12"
status: draft
---

# [Project Name] - Data Model

## Overview

<!-- High-level data model summary -->

### Core Entities

**Primary entities:**
1. [Entity 1]
2. [Entity 2]
3. [Entity 3]
4. [Entity 4]
5. [Entity 5]


### Entity Relationship Diagram

```
┌─────────────┐
│  [Entity1]  │
│  - id       │
│  - [field]  │
│  - [field]  │
└──────┬──────┘
       │ 1
       │
       │ *
┌──────┴──────┐         ┌─────────────┐
│  [Entity2]  │────────→│  [Entity3]  │
│  - id       │  1   *  │  - id       │
│  - [field]  │         │  - [field]  │
│  - [field]  │         │  - [field]  │
└──────┬──────┘         └─────────────┘
       │ 1
       │
       │ *
┌──────┴──────┐
│  [Entity4]  │
│  - id       │
│  - [field]  │
│  - [field]  │
└─────────────┘
```

---

## Entity Schemas

<!-- Detailed schema for each entity -->

### [Entity 1]

**Purpose:** [What this entity represents]

**Schema:**
```typescript
interface [Entity1] {
  id: string;                    // UUID
  [field]: string;               // [Description]
  [field]?: string;              // [Description]
  [field]: [EnumType];           // [Description]
  created_at: Date;
  updated_at: Date;
}

type [EnumType] =
  | '[value1]'
  | '[value2]'
  | '[value3]';
```

**Constraints:**
- `[field]` required, max [X] chars
- `[field]` must be valid enum
- [Additional constraint]

**Indexes:**
- Primary: `id`
- [Additional index]


### [Entity 2]

**Purpose:** [What this entity represents]

**Schema:**
```typescript
interface [Entity2] {
  id: string;                    // UUID
  [entity1]_id: string;          // Foreign key → [Entity1]

  [field]: string;               // [Description]
  [field]: string;               // [Description]
  [field]: [StatusType];         // [Description]

  // [Storage approach description]
  [field]: [JSONType];           // [Description]
  [field]: [MetadataType][];     // [Description]

  // Denormalized counts
  [count_field]: number;
  [count_field]: number;

  created_at: Date;
  updated_at: Date;
}

type [StatusType] = '[status1]' | '[status2]';

interface [MetadataType] {
  [field]: string;               // [Description]
  [field]: string;               // [Description]
  [field]: boolean;
  [field]: number;
}
```

**Constraints:**
- `[entity1]_id` must exist in [Entity1]
- `([entity1]_id, [field], [field])` unique
- `[count_field] <= [count_field]`

**Indexes:**
- Primary: `id`
- Composite: `([entity1]_id, [field])`


### [Entity 3]

**Purpose:** [What this entity represents]

**Schema:**
```typescript
interface [Entity3] {
  id: string;
  [entity2]_id: string;          // Foreign key → [Entity2]

  [field]: [SnapshotType];
  [field]: [JSONType];           // [Description]
  [field]: [MetadataType][];

  created_by: string;            // '[source1]' | '[source2]' | [agent name]
  created_at: Date;
  [field]?: string;
}

type [SnapshotType] =
  | '[type1]'
  | '[type2]'
  | '[type3]'
  | '[type4]';
```

**Constraints:**
- `[entity2]_id` must exist
- `[field]` must be valid enum
- Immutable (no UPDATEs)

**Indexes:**
- Primary: `id`
- Composite: `([entity2]_id, created_at DESC)`


### [Entity 4]

**Purpose:** [What this entity represents]

**Schema:**
```typescript
interface [Entity4] {
  id: string;
  [entity1]_id: string;          // Foreign key → [Entity1]
  [entity2]_id?: string;         // Optional context

  [field]: [RoleType];           // [Description]
  [field]?: string;              // [Description]
  [field]: string;               // [Description]

  [field]?: [MetadataType];      // Structured data
  created_at: Date;
}

type [RoleType] = '[role1]' | '[role2]';

interface [MetadataType] {
  [field]?: string;              // [Description]
  [field]?: string;              // [Description]
  [field]?: [ToolCall][];        // [Description]
  [key: string]: any;
}
```

**Constraints:**
- `[entity1]_id` required
- `[field]` must be valid enum

**Indexes:**
- Primary: `id`
- Composite: `([entity1]_id, created_at DESC)`
- Optional: `([entity2]_id, created_at DESC)`

---

## Data Relationships

<!-- How entities relate -->

### Relationships Summary

```
[Entity1] (1) ──→ (*) [Entity2]
[Entity2] (1) ──→ (*) [Entity3]
[Entity1] (1) ──→ (*) [Entity4]
[Entity2] (1) ──→ (*) [Entity4] (optional)
```

### Cascade Rules

**When [Entity1] is deleted:**
- [Entity2]: CASCADE DELETE
- [Entity4]: CASCADE DELETE
- [Entity3]: CASCADE DELETE (via [Entity2])

**When [Entity2] is deleted:**
- [Entity3]: CASCADE DELETE
- [Entity4]: SET NULL ([entity2]_id)

---

## Content Storage Strategy

<!-- How is complex content stored? -->

### [Format] JSON Format

**Example content:**
```json
{
  "type": "[root_type]",
  "content": [
    {
      "type": "[node_type]",
      "attrs": { "[attr]": [value] },
      "content": [{ "type": "[leaf_type]", "[field]": "[value]" }]
    },
    {
      "type": "[node_type]",
      "content": [{ "type": "[leaf_type]", "[field]": "[value]" }]
    }
  ]
}
```

### [Metadata] Extraction Logic

**How to parse [metadata] from content:**
```typescript
function extract[Metadata](content: [JSONType]): [MetadataType][] {
  const items: [MetadataType][] = [];
  let currentOrder = 1;

  content.content.forEach(node => {
    if (node.type === '[target_type]' && node.attrs.[attr] === [value]) {
      const [field] = extractText(node);
      const slug = slugify([field]);

      items.push({
        slug,
        [field],
        [field]: false,
        [field]: false,
        order: currentOrder++
      });
    }
  });

  return items;
}
```

### Metadata Sync Strategy

**When to update [metadata]:**
1. User adds new [element] → Add to metadata
2. User deletes [element] → Remove from metadata
3. User reorders [elements] → Update order field
4. User [action] → Update [field]

**Sync points:**
- After every content change (debounced)
- Before saving to database
- On load (validate sync)

---

## Query Patterns

<!-- Common queries and optimizations -->

### Frequent Queries

**1. Load [entity] with related [entities]:**
```sql
SELECT
  e1.*,
  jsonb_agg(e2.*) as [entities]
FROM [entity1] e1
LEFT JOIN [entity2] e2 ON e1.id = e2.[entity1]_id
WHERE e1.id = $1
  AND e2.[field] = '[value]'
GROUP BY e1.id;
```

**Performance:** Use index on `([entity1]_id, [field])`


**2. Get [entity] with calculated fields:**
```sql
SELECT
  id,
  [field],
  [count_field],
  [count_field],
  ROUND(([count_field]::numeric / [count_field]::numeric) * 100) as [calculated]
FROM [entity2]
WHERE id = $1;
```

**Performance:** Uses denormalized counts (fast)


**3. [Aggregation] query:**
```sql
SELECT
  [field],
  SUM([count_field]) as [total1],
  SUM([count_field]) as [total2]
FROM [entity2]
WHERE [entity1]_id = $1
GROUP BY [field];
```

**Performance:** Index on `[entity1]_id`


**4. Recent [items]:**
```sql
SELECT *
FROM [entity4]
WHERE [entity1]_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

**Performance:** Index on `([entity1]_id, created_at DESC)`

---

## Data Validation

<!-- How is data validated? -->

### Database Constraints

**[Entity1]:**
```sql
CHECK ([field] IN ('[value1]', '[value2]', '[value3]'))
```

**[Entity2]:**
```sql
CHECK ([field] IN ('[value1]', '[value2]'))
CHECK ([count_field] <= [count_field])
UNIQUE ([entity1]_id, [field], [field])
```


### Application Validation

**TypeScript types:**
```typescript
// Compile-time safety
type [EnumType] = '[value1]' | '[value2]' | '[value3]';

// Runtime validation with Zod
const [Entity]Schema = z.object({
  [field]: z.string().min(1).max(100),
  [field]: z.string().regex(/^[a-z0-9-]+$/),
  [count_field]: z.number().int().min(0),
  [count_field]: z.number().int().min(0),
  // ...
}).refine(
  data => data.[count_field] <= data.[count_field],
  "[count_field] cannot exceed [count_field]"
);
```

---

## Migration Strategy

<!-- How to handle schema changes -->

### Schema Versioning

**Approach:** [Migration tool/approach]

**Migration naming:**
- `0001_initial_schema.sql`
- `0002_add_[feature].sql`
- `0003_add_[feature].sql`


### Breaking Changes

**Example: Adding [field] to [entity]**

```sql
-- Migration: 000X_add_[field].sql

-- 1. Add new column (nullable initially)
ALTER TABLE [entity] ADD COLUMN [field] [TYPE] DEFAULT '[default]';

-- 2. Backfill data if needed
UPDATE [entity] SET [field] = '[value]' WHERE [field] = '[condition]';

-- 3. Make NOT NULL if needed
ALTER TABLE [entity] ALTER COLUMN [field] SET NOT NULL;
```


### Data Migration Scripts

**TypeScript migration example:**
```typescript
// scripts/migrations/backfill-[feature].ts
async function migrate[Entities]() {
  const items = await db
    .from('[entity]')
    .select('id, [field]')
    .is('[new_field]', null);

  for (const item of items) {
    const [derived] = extract[Data](item.[field]);

    await db
      .from('[entity]')
      .update({
        [new_field]: [derived],
        [count_field]: [derived].length
      })
      .eq('id', item.id);
  }
}
```

---

## Data Access Patterns

<!-- How different parts of the app access data -->

### [Component 1]

**Reads:**
- Load [entity] content on mount
- Subscribe to real-time updates

**Writes:**
- Debounced auto-save (every [X]s)
- Update [metadata] on content change
- Update [counts] on [action]


### [Component 2]

**Reads:**
- Load [entity] history on mount
- Subscribe to new [entities]

**Writes:**
- Insert user [entity]
- Insert [source] [entity] (streaming)
- Update [related entity] (if [source] modifies)


### [Component 3]

**Reads:**
- Load all [entities] for current [context]
- Subscribe to [entity] updates ([field])

**Writes:**
- None (read-only)

---

## Open Questions

- [ ] [Storage format question]
- [ ] [Template/preset handling]
- [ ] [Related entity versioning]
- [ ] [Archive/retention policy]
- [ ] [Data migration strategy]

---

## Future Enhancements

- [ ] [Enhancement 1]
- [ ] [Enhancement 2]
- [ ] [Enhancement 3]
- [ ] [Enhancement 4]
- [ ] [Enhancement 5]
