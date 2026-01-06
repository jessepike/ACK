# Data Model: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "design"
---

## Overview

<!-- 
High-level data model summary:
- Core entities
- Relationships
- Storage strategy
-->

### Core Entities

**Primary entities:**
1. Projects
2. Artifacts
3. Sections (embedded in Artifacts)
4. Messages
5. Snapshots


### Entity Relationship Diagram

```
┌─────────────┐
│  Projects   │
│  - id       │
│  - name     │
│  - stage    │
└──────┬──────┘
       │ 1
       │
       │ *
┌──────┴──────┐         ┌─────────────┐
│  Artifacts  │────────→│  Snapshots  │
│  - id       │  1   *  │  - id       │
│  - content  │         │  - content  │
│  - metadata │         │  - type     │
└──────┬──────┘         └─────────────┘
       │ 1
       │
       │ *
┌──────┴──────┐
│  Messages   │
│  - id       │
│  - role     │
│  - content  │
└─────────────┘
```



## Entity Schemas

<!-- 
Detailed schema for each entity:
- Fields
- Types
- Constraints
- Indexes
-->

### Projects

**Purpose:** Top-level container for ACK workflow

**Schema:**
```typescript
interface Project {
  id: string;                    // UUID
  name: string;                  // "ack-demo"
  description?: string;
  current_stage: StageType;      // 'discovery' | 'design' | ...
  created_by?: string;           // User ID (future)
  created_at: Date;
  updated_at: Date;
}

type StageType = 
  | 'discovery' 
  | 'design' 
  | 'environment' 
  | 'workflow' 
  | 'implementation';
```

**Constraints:**
- `name` required, max 100 chars
- `current_stage` must be valid enum
- 

**Indexes:**
- Primary: `id`
- 


### Artifacts

**Purpose:** Individual documents (concept.md, research.md, etc.)

**Schema:**
```typescript
interface Artifact {
  id: string;                    // UUID
  project_id: string;            // Foreign key → Projects
  
  name: string;                  // "concept.md"
  slug: string;                  // "concept"
  stage: StageType;              // "discovery"
  status: ArtifactStatus;        // "draft" | "finalized"
  
  // HYBRID STORAGE APPROACH
  content: TiptapJSON;           // Full Tiptap document
  section_metadata: SectionMetadata[];
  
  // Denormalized counts
  sections_total: number;
  sections_complete: number;
  
  created_at: Date;
  updated_at: Date;
}

type ArtifactStatus = 'draft' | 'finalized';

interface SectionMetadata {
  slug: string;                  // "what-is-it"
  title: string;                 // "What Is It?"
  is_done: boolean;
  is_collapsed: boolean;
  order: number;
}
```

**Constraints:**
- `project_id` must exist in Projects
- `(project_id, stage, slug)` unique
- `sections_complete <= sections_total`
- 

**Indexes:**
- Primary: `id`
- Composite: `(project_id, stage)`
- 


### Artifact Snapshots

**Purpose:** Versioning for key moments (stage transitions, agent changes)

**Schema:**
```typescript
interface ArtifactSnapshot {
  id: string;
  artifact_id: string;           // Foreign key → Artifacts
  
  snapshot_type: SnapshotType;
  content: TiptapJSON;           // Full content at snapshot time
  section_metadata: SectionMetadata[];
  
  created_by: string;            // 'user' | 'claude' | agent name
  created_at: Date;
  change_description?: string;
}

type SnapshotType = 
  | 'stage_transition'
  | 'agent_change'
  | 'finalization'
  | 'manual';
```

**Constraints:**
- `artifact_id` must exist
- `snapshot_type` must be valid enum
- Immutable (no UPDATEs)

**Indexes:**
- Primary: `id`
- Composite: `(artifact_id, created_at DESC)`


### Messages

**Purpose:** Chat history between user and agents

**Schema:**
```typescript
interface Message {
  id: string;
  project_id: string;            // Foreign key → Projects
  artifact_id?: string;          // Optional context
  
  role: MessageRole;             // 'user' | 'assistant'
  agent_type?: string;           // 'claude' | 'research_agent'
  content: string;               // Message text
  
  metadata?: MessageMetadata;    // Structured data
  created_at: Date;
}

type MessageRole = 'user' | 'assistant';

interface MessageMetadata {
  command?: string;              // "/research", "/validate"
  section_target?: string;       // Section slug if targeting
  tool_calls?: ToolCall[];       // Agent tool usage
  [key: string]: any;
}
```

**Constraints:**
- `project_id` required
- `role` must be 'user' or 'assistant'
- If `role === 'assistant'`, `agent_type` recommended

**Indexes:**
- Primary: `id`
- Composite: `(project_id, created_at DESC)`
- Optional: `(artifact_id, created_at DESC)`



## Data Relationships

<!-- 
How entities relate:
- Foreign keys
- Cascade rules
- Referential integrity
-->

### Relationships Summary

```
Projects (1) ──→ (*) Artifacts
Artifacts (1) ──→ (*) Snapshots
Projects (1) ──→ (*) Messages
Artifacts (1) ──→ (*) Messages (optional)
```

### Cascade Rules

**When Project is deleted:**
- Artifacts: CASCADE DELETE
- Messages: CASCADE DELETE
- Snapshots: CASCADE DELETE (via Artifacts)

**When Artifact is deleted:**
- Snapshots: CASCADE DELETE
- Messages: SET NULL (artifact_id)



## Content Storage Strategy

<!-- 
How is Tiptap content stored?
- JSON structure
- Section extraction
- Performance considerations
-->

### Tiptap JSON Format

**Example artifact content:**
```json
{
  "type": "doc",
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [{ "type": "text", "text": "What Is It?" }]
    },
    {
      "type": "paragraph",
      "content": [{ "type": "text", "text": "ACK is..." }]
    },
    {
      "type": "heading",
      "attrs": { "level": 2 },
      "content": [{ "type": "text", "text": "Problem Being Solved" }]
    }
  ]
}
```

### Section Extraction Logic

**How to parse sections from content:**
```typescript
function extractSections(content: TiptapJSON): SectionMetadata[] {
  const sections: SectionMetadata[] = [];
  let currentOrder = 1;
  
  content.content.forEach(node => {
    if (node.type === 'heading' && node.attrs.level === 2) {
      const title = extractText(node);
      const slug = slugify(title);
      
      sections.push({
        slug,
        title,
        is_done: false,
        is_collapsed: false,
        order: currentOrder++
      });
    }
  });
  
  return sections;
}
```

### Metadata Sync Strategy

**When to update section_metadata:**
1. User adds new H2 heading → Add to metadata
2. User deletes H2 heading → Remove from metadata
3. User reorders sections → Update order field
4. User checks "Done" → Update is_done field


**Sync points:**
- After every Tiptap content change (debounced)
- Before saving to database
- On artifact load (validate sync)



## Query Patterns

<!-- 
Common queries and optimizations:
- Frequent queries
- Performance notes
- Index usage
-->

### Frequent Queries

**1. Load project with all Discovery artifacts:**
```sql
SELECT 
  p.*,
  jsonb_agg(a.*) as artifacts
FROM projects p
LEFT JOIN artifacts a ON p.id = a.project_id
WHERE p.id = $1
  AND a.stage = 'discovery'
GROUP BY p.id;
```

**Performance:** Use index on `(project_id, stage)`


**2. Get artifact with section progress:**
```sql
SELECT 
  id,
  name,
  sections_complete,
  sections_total,
  ROUND((sections_complete::numeric / sections_total::numeric) * 100) as progress_pct
FROM artifacts
WHERE id = $1;
```

**Performance:** Uses denormalized counts (fast)


**3. Stage progress aggregation:**
```sql
SELECT 
  stage,
  SUM(sections_complete) as complete,
  SUM(sections_total) as total
FROM artifacts
WHERE project_id = $1
GROUP BY stage;
```

**Performance:** Index on `project_id`


**4. Recent chat history:**
```sql
SELECT *
FROM messages
WHERE project_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

**Performance:** Index on `(project_id, created_at DESC)`



## Data Validation

<!-- 
How is data validated?
- Database constraints
- Application-level validation
- Type safety
-->

### Database Constraints

**Projects:**
```sql
CHECK (current_stage IN ('discovery', 'design', 'environment', 'workflow', 'implementation'))
```

**Artifacts:**
```sql
CHECK (status IN ('draft', 'finalized'))
CHECK (sections_complete <= sections_total)
UNIQUE (project_id, stage, slug)
```


### Application Validation

**TypeScript types:**
```typescript
// Compile-time safety
type StageType = 'discovery' | 'design' | 'environment' | 'workflow' | 'implementation';

// Runtime validation with Zod
const ArtifactSchema = z.object({
  name: z.string().min(1).max(100),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  sections_total: z.number().int().min(0),
  sections_complete: z.number().int().min(0),
  // ...
}).refine(
  data => data.sections_complete <= data.sections_total,
  "sections_complete cannot exceed sections_total"
);
```



## Migration Strategy

<!-- 
How to handle schema changes:
- Versioning
- Backwards compatibility
- Data migrations
-->

### Schema Versioning

**Approach:**


**Migration naming:**
- `0001_initial_schema.sql`
- `0002_add_artifact_status.sql`
- `0003_add_snapshot_metadata.sql`


### Breaking Changes

**If we need to change content structure:**

Example: Adding tags to artifacts

```sql
-- Migration: 0005_add_tags.sql

-- 1. Add new column (nullable initially)
ALTER TABLE artifacts ADD COLUMN tags JSONB DEFAULT '[]';

-- 2. Backfill data if needed
UPDATE artifacts SET tags = '["untagged"]' WHERE tags = '[]';

-- 3. Make NOT NULL if needed
ALTER TABLE artifacts ALTER COLUMN tags SET NOT NULL;
```


### Data Migration Scripts

**TypeScript migration example:**
```typescript
// scripts/migrations/backfill-section-metadata.ts
async function migrateArtifacts() {
  const artifacts = await supabase
    .from('artifacts')
    .select('id, content')
    .is('section_metadata', null);
  
  for (const artifact of artifacts) {
    const metadata = extractSections(artifact.content);
    
    await supabase
      .from('artifacts')
      .update({
        section_metadata: metadata,
        sections_total: metadata.length
      })
      .eq('id', artifact.id);
  }
}
```



## Data Access Patterns

<!-- 
How different parts of the app access data:
- Read patterns
- Write patterns
- Optimization strategies
-->

### Editor Component

**Reads:**
- Load artifact content on mount
- Subscribe to real-time updates

**Writes:**
- Debounced auto-save (every 3s)
- Update section_metadata on content change
- Update sections_complete on "Done" toggle


### Chat Component

**Reads:**
- Load message history on mount
- Subscribe to new messages

**Writes:**
- Insert user message
- Insert assistant message (streaming)
- Update artifact (if agent modifies)


### Sidebar Component

**Reads:**
- Load all artifacts for current stage
- Subscribe to artifact updates (progress)

**Writes:**
- None (read-only)



---

## Open Questions

<!-- 
Data model uncertainties to resolve:
-->

- [ ] Should we store Tiptap content as JSONB or TEXT?
- [ ] How to handle artifact templates (pre-defined sections)?
- [ ] Should Messages have their own snapshots?
- [ ] How to archive old projects?
- [ ] What's the data retention policy?
- [ ]


## Future Enhancements

<!-- 
Potential data model additions:
-->

- [ ] Comments on specific sections
- [ ] Artifact tags/categories
- [ ] User teams and permissions
- [ ] Audit log for all changes
- [ ] Analytics/metrics table
- [ ]
