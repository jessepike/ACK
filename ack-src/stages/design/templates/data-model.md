---
type: artifact
stage: design
artifact: data-model
description: "Database schema, entities, and relationships"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Data Model

## Overview

<!-- Brief description of the data model -->

This document defines the database schema for [Project Name], including entities, relationships, and data access patterns.

**Database type:** [PostgreSQL / MySQL / MongoDB / SQLite / etc.]

**ORM/Query builder:** [Prisma / Drizzle / TypeORM / Mongoose / Raw SQL]

---

## Entity Relationship Diagram

<!-- ASCII ERD or description -->

```
┌──────────────┐       ┌──────────────┐
│    User      │       │    Post      │
├──────────────┤       ├──────────────┤
│ id (PK)      │───┐   │ id (PK)      │
│ email        │   │   │ title        │
│ name         │   └──▶│ author_id(FK)│
│ created_at   │       │ content      │
└──────────────┘       │ created_at   │
                       └──────────────┘
                              │
                              │ 1:N
                              ▼
                       ┌──────────────┐
                       │   Comment    │
                       ├──────────────┤
                       │ id (PK)      │
                       │ post_id (FK) │
                       │ user_id (FK) │
                       │ content      │
                       └──────────────┘
```

---

## Entities

### Entity: User

**Description:** [What this entity represents]

**Table name:** `users`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto-gen | Unique identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| `name` | VARCHAR(100) | NOT NULL | Display name |
| `password_hash` | VARCHAR(255) | NOT NULL | Hashed password |
| `role` | ENUM | NOT NULL, DEFAULT 'user' | User role |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update timestamp |

**Indexes:**
- `idx_users_email` on `email` (unique)
- `idx_users_role` on `role`

**Notes:**
- [Any special considerations for this entity]

---

### Entity: [Entity 2 Name]

**Description:** [What this entity represents]

**Table name:** `[table_name]`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto-gen | Unique identifier |
| `[field_1]` | [TYPE] | [CONSTRAINTS] | [Description] |
| `[field_2]` | [TYPE] | [CONSTRAINTS] | [Description] |
| `[field_3]` | [TYPE] | [CONSTRAINTS] | [Description] |
| `[foreign_key]` | UUID | FK → [table.id] | Reference to [entity] |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update timestamp |

**Indexes:**
- `idx_[table]_[field]` on `[field]`

**Notes:**
- [Any special considerations]

---

### Entity: [Entity 3 Name]

**Description:** [What this entity represents]

**Table name:** `[table_name]`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto-gen | Unique identifier |
| `[field_1]` | [TYPE] | [CONSTRAINTS] | [Description] |
| `[field_2]` | [TYPE] | [CONSTRAINTS] | [Description] |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW | Last update timestamp |

**Indexes:**
- [Index definitions]

**Notes:**
- [Any special considerations]

---

## Relationships

### User → [Entity 2] (One-to-Many)

**Description:** [What this relationship represents]

**Implementation:**
- Foreign key `user_id` on `[entity_2]` table
- Cascade on delete: [Yes/No - what happens]

```sql
-- Example
ALTER TABLE posts
ADD CONSTRAINT fk_posts_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

---

### [Entity 2] → [Entity 3] (One-to-Many)

**Description:** [What this relationship represents]

**Implementation:**
- Foreign key `[entity_2]_id` on `[entity_3]` table
- Cascade on delete: [Yes/No - what happens]

---

### [Entity A] ↔ [Entity B] (Many-to-Many)

**Description:** [What this relationship represents]

**Junction table:** `[entity_a]_[entity_b]`

| Field | Type | Constraints |
|-------|------|-------------|
| `[entity_a]_id` | UUID | FK → [entity_a].id, PK |
| `[entity_b]_id` | UUID | FK → [entity_b].id, PK |
| `created_at` | TIMESTAMP | DEFAULT NOW |

---

## Enums / Types

### Enum: [Name]

**Used in:** [Which entities use this]

| Value | Description |
|-------|-------------|
| `value_1` | [What it means] |
| `value_2` | [What it means] |
| `value_3` | [What it means] |

```sql
CREATE TYPE [enum_name] AS ENUM ('value_1', 'value_2', 'value_3');
```

---

## Query Patterns

### Common Queries

| Query | Frequency | Index Support |
|-------|-----------|---------------|
| Get user by email | High | `idx_users_email` |
| List posts by user | High | `idx_posts_user_id` |
| [Query description] | [Frequency] | [Index] |

### Complex Queries

#### [Query Name]

**Purpose:** [What this query does]

**Used by:** [Which component/feature]

```sql
-- Example query
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON p.user_id = u.id
GROUP BY u.id
ORDER BY post_count DESC
LIMIT 10;
```

**Performance notes:** [Any optimization considerations]

---

## Data Integrity

### Constraints

| Constraint | Table | Description |
|------------|-------|-------------|
| `chk_[name]` | [table] | [What it validates] |
| `unq_[name]` | [table] | [Uniqueness constraint] |

### Triggers (if any)

| Trigger | Table | Event | Action |
|---------|-------|-------|--------|
| `trg_[name]` | [table] | [INSERT/UPDATE/DELETE] | [What it does] |

---

## Migration Strategy

### Initial Migration

**Migration name:** `001_initial_schema`

**Actions:**
1. Create `users` table
2. Create `[entity_2]` table
3. Create `[entity_3]` table
4. Add foreign key constraints
5. Create indexes

### Future Migrations

| Migration | Purpose | Breaking? |
|-----------|---------|-----------|
| `002_[name]` | [What changes] | Yes/No |
| `003_[name]` | [What changes] | Yes/No |

### Rollback Strategy

- Each migration has a corresponding down migration
- Test rollbacks in staging before production
- [Any specific rollback considerations]

---

## Seed Data

### Required Seed Data

| Table | Data | Purpose |
|-------|------|---------|
| `[table]` | [What data] | [Why needed] |

### Development Seed Data

| Table | Records | Purpose |
|-------|---------|---------|
| `users` | [X] test users | Local development |
| `[table]` | [X] records | Testing features |

---

## Data Retention

| Data Type | Retention | Deletion Method |
|-----------|-----------|-----------------|
| User data | [Duration] | [Soft/Hard delete] |
| Logs | [Duration] | [Archival strategy] |
| [Other] | [Duration] | [Method] |

---

## Performance Considerations

### Indexing Strategy

- Primary keys: UUID (or auto-increment integer)
- Foreign keys: Always indexed
- Search fields: Indexed based on query patterns
- Composite indexes: [Where needed]

### Denormalization

| Denormalized Field | Location | Reason |
|--------------------|----------|--------|
| [Field] | [Table] | [Performance reason] |

### Partitioning (if needed)

| Table | Partition Strategy | Partition Key |
|-------|-------------------|---------------|
| [Table] | [Range/List/Hash] | [Field] |

---

## Open Questions

- [ ] [Data modeling question]
- [ ] [Schema decision to make]
- [ ] [Performance consideration]

---

## Related Documents

- [architecture.md](architecture.md) - System architecture
- [stack.md](stack.md) - Database technology choice
- [brief.md](../../discover/templates/brief.md) - Business requirements
