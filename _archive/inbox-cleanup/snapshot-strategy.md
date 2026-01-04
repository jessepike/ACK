# IPE Snapshot Strategy
## Versioning for Key Moments (Hybrid Approach)

## Overview

IPE uses a **hybrid versioning strategy**:
- **Normal editing** → UPDATE artifacts in place (fast, no bloat)
- **Key moments** → CREATE immutable snapshots (safety net, audit trail)

This balances performance with safety, avoiding both:
- ❌ Full immutable versioning (storage explosion from auto-save)
- ❌ Pure in-place updates (no history, no rollback)

---

## Snapshot Types

### 1. Stage Transition Snapshots
**When:** User completes a stage (e.g., "Complete Discovery")
**Why:** Milestone marker, audit trail
**Frequency:** ~5 per project (one per stage)

```typescript
// Example: User clicks "Complete Discovery Stage"
await createSnapshot({
  artifact_id: conceptArtifactId,
  snapshot_type: 'stage_transition',
  content: currentContent,
  section_metadata: currentMetadata,
  created_by: userId,
  change_description: 'Discovery stage completed'
});

// Then transition stage
await updateProject({
  current_stage: 'design',
  updated_at: new Date()
});
```

**Use case:** "Show me what the concept looked like when we finished Discovery"

---

### 2. Agent Change Snapshots
**When:** Before AI agent modifies artifact content
**Why:** Safety net for automated changes, rollback capability
**Frequency:** ~10-30 per artifact (depends on agent usage)

```typescript
// Example: Agent about to update "Value Proposition" section
async function applyAgentChange(artifactId, agentContent, sectionSlug) {
  // 1. Create snapshot BEFORE change
  await createSnapshot({
    artifact_id: artifactId,
    snapshot_type: 'agent_change',
    content: currentContent,
    section_metadata: currentMetadata,
    created_by: 'claude',
    change_description: `Agent updating section: ${sectionSlug}`
  });
  
  // 2. Apply agent's changes
  await updateArtifact({
    id: artifactId,
    content: agentContent,
    updated_at: new Date()
  });
  
  // 3. Return snapshot ID for potential rollback
  return snapshotId;
}
```

**Use case:** 
- "The agent changed this and I don't like it, revert"
- "Show me what the agent changed"
- Diff view: before/after agent modification

---

### 3. Finalization Snapshots
**When:** User marks artifact as "Finalized"
**Why:** Lock down approved content, prevent accidental edits
**Frequency:** ~4 per stage (one per artifact)

```typescript
// Example: User marks concept.md as finalized
await createSnapshot({
  artifact_id: conceptArtifactId,
  snapshot_type: 'finalization',
  content: currentContent,
  section_metadata: currentMetadata,
  created_by: userId,
  change_description: 'Concept finalized and approved'
});

await updateArtifact({
  id: conceptArtifactId,
  status: 'finalized'
});
```

**Use case:** "What was the approved version of concept.md?"

---

### 4. Manual Snapshots
**When:** User explicitly clicks "Save Version"
**Why:** User wants a checkpoint they can name
**Frequency:** ~0-5 per artifact (user-discretionary)

```typescript
// Example: User saves a version with custom description
await createSnapshot({
  artifact_id: artifactId,
  snapshot_type: 'manual',
  content: currentContent,
  section_metadata: currentMetadata,
  created_by: userId,
  change_description: 'Before major refactor of core features section'
});
```

**Use case:** "I want to try something radical, let me save this first"

---

## Storage Estimates

### Typical IPE Project
- 5 stages × 4 artifacts/stage = **20 artifacts**
- 3 agent interactions per artifact = **60 agent snapshots**
- 1 finalization per artifact = **20 finalization snapshots**
- 1 stage transition per stage = **5 stage snapshots**
- 2 manual snapshots per artifact = **40 manual snapshots**

**Total: ~125 snapshots per project**

### Storage Calculation
Assume average artifact size: 50KB (Tiptap JSON)
- 125 snapshots × 50KB = **6.25 MB per project**

**Verdict:** Negligible storage cost, huge safety benefit.

---

## Implementation Patterns

### Pattern 1: Snapshot Before Risky Operation

```typescript
async function performRiskyOperation(operation: () => Promise<void>) {
  // 1. Create snapshot
  const snapshot = await createSnapshot({
    snapshot_type: 'manual',
    change_description: 'Before risky operation'
  });
  
  try {
    // 2. Perform operation
    await operation();
  } catch (error) {
    // 3. Auto-rollback on error
    await restoreSnapshot(snapshot.id);
    throw error;
  }
}
```

### Pattern 2: Diff View for Agent Changes

```typescript
async function getAgentChangeDiff(artifactId: string) {
  // Get most recent agent snapshot
  const snapshot = await supabase
    .from('artifact_snapshots')
    .select('*')
    .eq('artifact_id', artifactId)
    .eq('snapshot_type', 'agent_change')
    .order('created_at', { ascending: false })
    .limit(1)
    .single();
  
  // Get current content
  const current = await supabase
    .from('artifacts')
    .select('content')
    .eq('id', artifactId)
    .single();
  
  // Generate diff
  return generateDiff(snapshot.content, current.content);
}
```

### Pattern 3: Restore to Snapshot

```typescript
async function restoreSnapshot(snapshotId: string) {
  // 1. Fetch snapshot
  const snapshot = await supabase
    .from('artifact_snapshots')
    .select('*')
    .eq('id', snapshotId)
    .single();
  
  // 2. Create new snapshot of current state (before restoring)
  await createSnapshot({
    artifact_id: snapshot.artifact_id,
    snapshot_type: 'manual',
    change_description: 'Before restore operation',
    // ... current content
  });
  
  // 3. Restore snapshot content
  await supabase
    .from('artifacts')
    .update({
      content: snapshot.content,
      section_metadata: snapshot.section_metadata,
      updated_at: new Date()
    })
    .eq('id', snapshot.artifact_id);
}
```

---

## Snapshot Lifecycle

### Creation Flow
```
User Action / Agent Operation
           ↓
   Should snapshot? ──→ No → Proceed
           ↓ Yes
   Create snapshot record
           ↓
   Perform operation
           ↓
   Update artifact
```

### Cleanup Strategy
**Current:** Keep all snapshots forever (storage is cheap)

**Future (optional):**
- Delete snapshots older than 90 days (except finalization/stage_transition)
- Keep only last 10 agent_change snapshots per artifact
- Compress old snapshots (gzip JSON)

---

## Database Queries

### Get snapshot history for artifact
```sql
SELECT 
  id,
  snapshot_type,
  created_by,
  created_at,
  change_description
FROM artifact_snapshots
WHERE artifact_id = ?
ORDER BY created_at DESC;
```

### Get all finalization snapshots for project
```sql
SELECT 
  s.id,
  a.name as artifact_name,
  s.created_at,
  s.created_by
FROM artifact_snapshots s
JOIN artifacts a ON s.artifact_id = a.id
WHERE a.project_id = ?
  AND s.snapshot_type = 'finalization'
ORDER BY s.created_at DESC;
```

### Count snapshots by type
```sql
SELECT 
  snapshot_type,
  COUNT(*) as count
FROM artifact_snapshots s
JOIN artifacts a ON s.artifact_id = a.id
WHERE a.project_id = ?
GROUP BY snapshot_type;
```

---

## UI Considerations

### Version History View
```
┌─────────────────────────────────────────┐
│ Version History: concept.md             │
├─────────────────────────────────────────┤
│ ✓ Discovery stage completed             │
│   Stage Transition • 2 hours ago        │
│                                          │
│ 🤖 Agent updated "Core Features"        │
│   Agent Change • 4 hours ago            │
│                                          │
│ ✓ Concept finalized and approved        │
│   Finalization • 1 day ago              │
│                                          │
│ 💾 Before major refactor                │
│   Manual • 2 days ago                   │
└─────────────────────────────────────────┘
```

### Restore Confirmation
```
┌─────────────────────────────────────────┐
│ ⚠️ Restore to previous version?         │
├─────────────────────────────────────────┤
│ Snapshot: Agent updated "Core Features" │
│ Created: 4 hours ago                    │
│                                          │
│ Current content will be saved as a      │
│ snapshot before restoring.              │
│                                          │
│ [ Cancel ]  [ Restore ]                 │
└─────────────────────────────────────────┘
```

---

## Key Principles

1. **Snapshot before destructive operations** - Especially agent changes
2. **Keep snapshots lightweight** - Don't snapshot on every keystroke
3. **Make snapshots meaningful** - Always include change_description
4. **Enable easy rollback** - One-click restore from UI
5. **Audit trail for compliance** - Track who changed what when

---

## Testing Scenarios

### Scenario 1: Agent Breaks Something
1. Agent modifies "Value Proposition" section
2. User reviews, doesn't like it
3. User clicks "Undo Agent Change"
4. System restores pre-agent snapshot
5. User sees original content back

### Scenario 2: Stage Completion Audit
1. Project manager asks: "What did concept.md look like when Discovery was completed?"
2. Query: Find stage_transition snapshot for Discovery stage
3. Display snapshot content
4. Can compare to current version

### Scenario 3: Accidental Deletion
1. User accidentally deletes entire section
2. User realizes mistake
3. User goes to version history
4. Finds most recent snapshot (auto-created before agent change)
5. Restores it

---

## Future Enhancements

- **Branching:** Create experimental branches from snapshots
- **Collaborative:** Track which user made which changes
- **Compression:** Gzip old snapshots to save space
- **Retention:** Auto-cleanup policy for old snapshots
- **Diff view:** Visual diff between any two snapshots
- **Annotations:** Add comments to snapshots
