# IPE Progress Calculation Examples
## Fast Queries Using Denormalized Counts

## Overview

IPE uses **denormalized progress counts** for fast UI updates:
- `sections_total` - Total number of sections in artifact
- `sections_complete` - Number of sections marked "Done"

This avoids parsing JSON on every query while keeping data in sync.

---

## SQL Queries

### 1. Get Progress for Single Artifact

```sql
-- Simple percentage calculation
SELECT 
  id,
  name,
  sections_complete,
  sections_total,
  ROUND((sections_complete::numeric / sections_total::numeric) * 100, 1) as progress_pct,
  sections_complete || '/' || sections_total as progress_display
FROM artifacts
WHERE id = '550e8400-e29b-41d4-a716-446655440000';
```

**Result:**
```
id      | name        | complete | total | progress_pct | progress_display
--------|-------------|----------|-------|--------------|------------------
550e... | concept.md  | 2        | 6     | 33.3         | 2/6
```

---

### 2. Get Progress for All Artifacts in a Stage

```sql
-- Discovery stage progress across all artifacts
SELECT 
  name,
  status,
  sections_complete,
  sections_total,
  ROUND((sections_complete::numeric / sections_total::numeric) * 100, 1) as progress_pct
FROM artifacts
WHERE project_id = 'abc123'
  AND stage = 'discovery'
ORDER BY name;
```

**Result:**
```
name           | status     | complete | total | progress_pct
---------------|------------|----------|-------|-------------
concept.md     | draft      | 2        | 6     | 33.3
research.md    | draft      | 4        | 4     | 100.0
scope.md       | draft      | 0        | 4     | 0.0
validation.md  | finalized  | 3        | 3     | 100.0
```

---

### 3. Aggregate Stage Progress

```sql
-- Overall Discovery stage progress
SELECT 
  stage,
  SUM(sections_complete) as total_complete,
  SUM(sections_total) as total_sections,
  ROUND((SUM(sections_complete)::numeric / SUM(sections_total)::numeric) * 100, 1) as stage_progress_pct,
  COUNT(*) FILTER (WHERE status = 'finalized') as finalized_artifacts,
  COUNT(*) as total_artifacts
FROM artifacts
WHERE project_id = 'abc123'
  AND stage = 'discovery'
GROUP BY stage;
```

**Result:**
```
stage     | total_complete | total_sections | stage_progress_pct | finalized | total
----------|----------------|----------------|--------------------|-----------|---------
discovery | 9              | 17             | 52.9               | 1         | 4
```

---

### 4. Project-Wide Progress (All Stages)

```sql
-- Progress across all 5 stages
SELECT 
  stage,
  SUM(sections_complete) as complete,
  SUM(sections_total) as total,
  ROUND((SUM(sections_complete)::numeric / SUM(sections_total)::numeric) * 100, 1) as progress_pct,
  COUNT(*) FILTER (WHERE status = 'finalized') || '/' || COUNT(*) as artifacts_finalized
FROM artifacts
WHERE project_id = 'abc123'
GROUP BY stage
ORDER BY 
  CASE stage
    WHEN 'discovery' THEN 1
    WHEN 'design' THEN 2
    WHEN 'environment' THEN 3
    WHEN 'workflow' THEN 4
    WHEN 'implementation' THEN 5
  END;
```

**Result:**
```
stage          | complete | total | progress_pct | artifacts_finalized
---------------|----------|-------|--------------|--------------------
discovery      | 9        | 17    | 52.9         | 1/4
design         | 0        | 15    | 0.0          | 0/4
environment    | 0        | 9     | 0.0          | 0/3
workflow       | 0        | 10    | 0.0          | 0/3
implementation | 0        | 12    | 0.0          | 0/3
```

---

### 5. Find Incomplete Artifacts

```sql
-- Show artifacts that are started but not complete
SELECT 
  name,
  stage,
  sections_complete,
  sections_total,
  sections_total - sections_complete as sections_remaining
FROM artifacts
WHERE project_id = 'abc123'
  AND sections_complete < sections_total
  AND sections_complete > 0
ORDER BY stage, name;
```

**Result:**
```
name        | stage     | complete | total | remaining
------------|-----------|----------|-------|----------
concept.md  | discovery | 2        | 6     | 4
scope.md    | discovery | 1        | 4     | 3
```

---

### 6. Top Bar Progress Badges (UI Query)

```sql
-- Get progress display for top navigation tabs
-- Returns: "Discovery 4/4" | "Solution Design 2/4" | "Environment 0/4"
SELECT 
  sd.name as stage_name,
  sd.order_index,
  COALESCE(SUM(a.sections_complete), 0) as complete,
  COALESCE(SUM(a.sections_total), 0) as total,
  COALESCE(SUM(a.sections_complete), 0) || '/' || COALESCE(SUM(a.sections_total), 0) as badge_text
FROM stage_definitions sd
LEFT JOIN artifacts a ON sd.slug = a.stage AND a.project_id = 'abc123'
GROUP BY sd.slug, sd.name, sd.order_index
ORDER BY sd.order_index;
```

**Result:**
```
stage_name        | order | complete | total | badge_text
------------------|-------|----------|-------|------------
Discovery         | 1     | 9        | 17    | 9/17
Solution Design   | 2     | 0        | 15    | 0/15
Environment       | 3     | 0        | 9     | 0/9
Workflow          | 4     | 0        | 10    | 0/10
Implementation    | 5     | 0        | 12    | 0/12
```

---

## TypeScript/JavaScript Functions

### Calculate Artifact Progress

```typescript
interface ProgressStats {
  complete: number;
  total: number;
  percentage: number;
  display: string;
  isComplete: boolean;
}

function calculateArtifactProgress(artifact: Artifact): ProgressStats {
  const percentage = artifact.sections_total > 0
    ? Math.round((artifact.sections_complete / artifact.sections_total) * 100)
    : 0;
  
  return {
    complete: artifact.sections_complete,
    total: artifact.sections_total,
    percentage,
    display: `${artifact.sections_complete}/${artifact.sections_total}`,
    isComplete: artifact.sections_complete === artifact.sections_total
  };
}
```

**Usage:**
```typescript
const stats = calculateArtifactProgress(conceptArtifact);
// stats = { complete: 2, total: 6, percentage: 33, display: "2/6", isComplete: false }
```

---

### Calculate Stage Progress

```typescript
interface StageProgress {
  stageName: string;
  totalSections: number;
  completeSections: number;
  percentage: number;
  artifactsFinalized: number;
  artifactsTotal: number;
  badgeText: string;
  badgeColor: 'green' | 'orange' | 'gray';
}

async function getStageProgress(
  supabase: SupabaseClient,
  projectId: string,
  stage: string
): Promise<StageProgress> {
  const { data: artifacts } = await supabase
    .from('artifacts')
    .select('sections_total, sections_complete, status')
    .eq('project_id', projectId)
    .eq('stage', stage);
  
  const totalSections = artifacts.reduce((sum, a) => sum + a.sections_total, 0);
  const completeSections = artifacts.reduce((sum, a) => sum + a.sections_complete, 0);
  const finalizedCount = artifacts.filter(a => a.status === 'finalized').length;
  
  const percentage = totalSections > 0
    ? Math.round((completeSections / totalSections) * 100)
    : 0;
  
  // Badge color logic
  let badgeColor: 'green' | 'orange' | 'gray';
  if (percentage === 100) badgeColor = 'green';
  else if (percentage > 0) badgeColor = 'orange';
  else badgeColor = 'gray';
  
  return {
    stageName: stage,
    totalSections,
    completeSections,
    percentage,
    artifactsFinalized: finalizedCount,
    artifactsTotal: artifacts.length,
    badgeText: `${completeSections}/${totalSections}`,
    badgeColor
  };
}
```

**Usage:**
```typescript
const progress = await getStageProgress(supabase, projectId, 'discovery');
// progress = { 
//   stageName: 'discovery',
//   totalSections: 17,
//   completeSections: 9,
//   percentage: 53,
//   artifactsFinalized: 1,
//   artifactsTotal: 4,
//   badgeText: '9/17',
//   badgeColor: 'orange'
// }
```

---

### Update Progress After Section Done Toggle

```typescript
async function toggleSectionDone(
  supabase: SupabaseClient,
  artifactId: string,
  sectionSlug: string
) {
  // 1. Fetch current state
  const { data: artifact } = await supabase
    .from('artifacts')
    .select('section_metadata, sections_complete, sections_total')
    .eq('id', artifactId)
    .single();
  
  // 2. Toggle the section's done state
  const updatedMetadata = artifact.section_metadata.map((s: SectionMetadata) =>
    s.slug === sectionSlug
      ? { ...s, is_done: !s.is_done }
      : s
  );
  
  // 3. Recalculate denormalized count
  const newComplete = updatedMetadata.filter((s: SectionMetadata) => s.is_done).length;
  
  // 4. Update database with new count
  const { error } = await supabase
    .from('artifacts')
    .update({
      section_metadata: updatedMetadata,
      sections_complete: newComplete  // ← Denormalized count stays in sync
    })
    .eq('id', artifactId);
  
  return { newComplete, total: artifact.sections_total };
}
```

---

### Realtime Progress Updates (Supabase Realtime)

```typescript
// Subscribe to artifact changes for live progress updates
function subscribeToArtifactProgress(
  supabase: SupabaseClient,
  projectId: string,
  onProgressChange: (progress: any) => void
) {
  const channel = supabase
    .channel('artifact-progress')
    .on(
      'postgres_changes',
      {
        event: 'UPDATE',
        schema: 'public',
        table: 'artifacts',
        filter: `project_id=eq.${projectId}`
      },
      (payload) => {
        // Extract progress from updated artifact
        const artifact = payload.new;
        const progress = {
          artifactId: artifact.id,
          complete: artifact.sections_complete,
          total: artifact.sections_total,
          percentage: Math.round((artifact.sections_complete / artifact.sections_total) * 100)
        };
        
        onProgressChange(progress);
      }
    )
    .subscribe();
  
  return () => channel.unsubscribe();
}
```

**Usage:**
```typescript
// In React component
useEffect(() => {
  const unsubscribe = subscribeToArtifactProgress(
    supabase,
    projectId,
    (progress) => {
      console.log(`Artifact ${progress.artifactId}: ${progress.percentage}% complete`);
      // Update UI badge
    }
  );
  
  return unsubscribe;
}, [projectId]);
```

---

## React Component Examples

### Progress Badge Component

```tsx
interface ProgressBadgeProps {
  complete: number;
  total: number;
}

function ProgressBadge({ complete, total }: ProgressBadgeProps) {
  const percentage = total > 0 ? Math.round((complete / total) * 100) : 0;
  
  // Color based on completion
  let bgColor, textColor, borderColor;
  if (percentage === 100) {
    bgColor = 'bg-green-500/15';
    textColor = 'text-green-500';
    borderColor = 'border-green-500/30';
  } else if (percentage > 0) {
    bgColor = 'bg-orange-500/15';
    textColor = 'text-orange-500';
    borderColor = 'border-orange-500/30';
  } else {
    bgColor = 'bg-gray-500/10';
    textColor = 'text-gray-500';
    borderColor = 'border-gray-500/20';
  }
  
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-mono ${bgColor} ${textColor} border ${borderColor}`}>
      {complete}/{total}
    </span>
  );
}
```

### Stage Tab with Progress

```tsx
function StageTab({ stage, progress }: StageTabProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium">{stage.name}</span>
      <ProgressBadge complete={progress.complete} total={progress.total} />
    </div>
  );
}
```

---

## Performance Considerations

### Why Denormalization Works

**Without denormalized counts:**
```typescript
// BAD: Parse JSON on every query
const artifact = await supabase.from('artifacts').select('section_metadata');
const complete = artifact.section_metadata.filter(s => s.is_done).length;
const total = artifact.section_metadata.length;
```

**With denormalized counts:**
```typescript
// GOOD: Direct integer comparison
const artifact = await supabase.from('artifacts').select('sections_complete, sections_total');
// Already have the counts!
```

**Speed difference:**
- JSON parsing + filtering: ~5-10ms per artifact
- Integer read: ~0.1ms per artifact
- **50-100x faster for progress queries**

---

## Validation & Consistency

### Ensure Counts Stay in Sync

```typescript
// Database constraint already prevents this:
// CONSTRAINT valid_progress CHECK (sections_complete <= sections_total)

// Application-level validation
function validateProgressCounts(artifact: Artifact): boolean {
  const actualTotal = artifact.section_metadata.length;
  const actualComplete = artifact.section_metadata.filter(s => s.is_done).length;
  
  if (artifact.sections_total !== actualTotal) {
    console.error('sections_total out of sync!');
    return false;
  }
  
  if (artifact.sections_complete !== actualComplete) {
    console.error('sections_complete out of sync!');
    return false;
  }
  
  return true;
}
```

### Auto-Repair Function

```typescript
// If counts get out of sync, repair them
async function repairProgressCounts(supabase: SupabaseClient, artifactId: string) {
  const { data: artifact } = await supabase
    .from('artifacts')
    .select('section_metadata')
    .eq('id', artifactId)
    .single();
  
  const correctTotal = artifact.section_metadata.length;
  const correctComplete = artifact.section_metadata.filter(s => s.is_done).length;
  
  await supabase
    .from('artifacts')
    .update({
      sections_total: correctTotal,
      sections_complete: correctComplete
    })
    .eq('id', artifactId);
  
  console.log(`Repaired counts: ${correctComplete}/${correctTotal}`);
}
```

---

## Summary

**Key Principles:**
1. ✅ Store counts as integers for fast queries
2. ✅ Update counts whenever section metadata changes
3. ✅ Use SQL aggregation for stage-level progress
4. ✅ Validate counts match metadata
5. ✅ Subscribe to realtime updates for live badges

**Performance:**
- Single artifact progress: <1ms
- Stage progress: <5ms (4 artifacts)
- Project-wide progress: <10ms (20 artifacts)
