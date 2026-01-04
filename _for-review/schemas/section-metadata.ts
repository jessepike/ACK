// ============================================================================
// IPE Section Metadata Structure
// TypeScript types and examples for the HYBRID storage approach
// ============================================================================

/**
 * Section Metadata Object
 * Stored in artifacts.section_metadata as JSONB array
 * Enables fast queries for progress, done states, collapse states
 */
export interface SectionMetadata {
  slug: string;           // URL-safe identifier: "what-is-it"
  title: string;          // Display title: "What Is It?"
  is_done: boolean;       // Completion checkbox state
  is_collapsed: boolean;  // UI collapse state
  order: number;          // Display order (1-based)
}

/**
 * Artifact with Section Metadata
 * Complete type for the hybrid approach
 */
export interface Artifact {
  id: string;
  project_id: string;
  name: string;
  slug: string;
  stage: 'discovery' | 'design' | 'environment' | 'workflow' | 'implementation';
  status: 'draft' | 'finalized';
  
  // Tiptap JSON content (full document)
  content: object;
  
  // Section metadata (HYBRID approach)
  section_metadata: SectionMetadata[];
  
  // Denormalized progress tracking
  sections_total: number;
  sections_complete: number;
  
  created_at: string;
  updated_at: string;
}

// ============================================================================
// EXAMPLES
// ============================================================================

/**
 * Example: concept.md section metadata
 */
export const CONCEPT_SECTION_METADATA: SectionMetadata[] = [
  {
    slug: 'what-is-it',
    title: 'What Is It?',
    is_done: true,
    is_collapsed: false,
    order: 1
  },
  {
    slug: 'problem-being-solved',
    title: 'Problem Being Solved',
    is_done: true,
    is_collapsed: false,
    order: 2
  },
  {
    slug: 'core-features',
    title: 'Core Features',
    is_done: false,
    is_collapsed: true,
    order: 3
  },
  {
    slug: 'value-proposition',
    title: 'Value Proposition',
    is_done: false,
    is_collapsed: true,
    order: 4
  },
  {
    slug: 'success-looks-like',
    title: 'Success Looks Like',
    is_done: false,
    is_collapsed: true,
    order: 5
  },
  {
    slug: 'non-goals',
    title: 'Non-Goals',
    is_done: false,
    is_collapsed: true,
    order: 6
  }
];

/**
 * Example: Full artifact object
 */
export const EXAMPLE_ARTIFACT: Artifact = {
  id: '550e8400-e29b-41d4-a716-446655440000',
  project_id: '123e4567-e89b-12d3-a456-426614174000',
  name: 'concept.md',
  slug: 'concept',
  stage: 'discovery',
  status: 'draft',
  content: {
    type: 'doc',
    content: [
      // Tiptap JSON nodes...
    ]
  },
  section_metadata: CONCEPT_SECTION_METADATA,
  sections_total: 6,
  sections_complete: 2,
  created_at: '2025-01-01T00:00:00Z',
  updated_at: '2025-01-01T12:00:00Z'
};

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Mark a section as done
 */
export function markSectionDone(
  artifact: Artifact,
  sectionSlug: string
): Artifact {
  const updatedMetadata = artifact.section_metadata.map(section =>
    section.slug === sectionSlug
      ? { ...section, is_done: true }
      : section
  );
  
  const sectionsComplete = updatedMetadata.filter(s => s.is_done).length;
  
  return {
    ...artifact,
    section_metadata: updatedMetadata,
    sections_complete: sectionsComplete
  };
}

/**
 * Toggle section collapse state
 */
export function toggleSectionCollapse(
  artifact: Artifact,
  sectionSlug: string
): Artifact {
  const updatedMetadata = artifact.section_metadata.map(section =>
    section.slug === sectionSlug
      ? { ...section, is_collapsed: !section.is_collapsed }
      : section
  );
  
  return {
    ...artifact,
    section_metadata: updatedMetadata
  };
}

/**
 * Get progress percentage
 */
export function getProgressPercentage(artifact: Artifact): number {
  if (artifact.sections_total === 0) return 0;
  return Math.round((artifact.sections_complete / artifact.sections_total) * 100);
}

/**
 * Get progress display string (e.g., "2/6")
 */
export function getProgressDisplay(artifact: Artifact): string {
  return `${artifact.sections_complete}/${artifact.sections_total}`;
}

/**
 * Check if artifact is complete
 */
export function isArtifactComplete(artifact: Artifact): boolean {
  return artifact.sections_complete === artifact.sections_total;
}

/**
 * Get next incomplete section
 */
export function getNextIncompleteSection(
  artifact: Artifact
): SectionMetadata | null {
  return artifact.section_metadata.find(s => !s.is_done) || null;
}

// ============================================================================
// SUPABASE UPDATE PATTERNS
// ============================================================================

/**
 * Example: Update artifact when section is marked done
 */
export async function updateSectionDoneState(
  supabase: any, // SupabaseClient type
  artifactId: string,
  sectionSlug: string,
  isDone: boolean
) {
  // 1. Fetch current artifact
  const { data: artifact } = await supabase
    .from('artifacts')
    .select('section_metadata, sections_complete, sections_total')
    .eq('id', artifactId)
    .single();
  
  // 2. Update metadata
  const updatedMetadata = artifact.section_metadata.map((s: SectionMetadata) =>
    s.slug === sectionSlug ? { ...s, is_done: isDone } : s
  );
  
  // 3. Recalculate count
  const newComplete = updatedMetadata.filter((s: SectionMetadata) => s.is_done).length;
  
  // 4. Update database
  const { error } = await supabase
    .from('artifacts')
    .update({
      section_metadata: updatedMetadata,
      sections_complete: newComplete
    })
    .eq('id', artifactId);
  
  return { error };
}

/**
 * Example: Update artifact when section is collapsed/expanded
 */
export async function updateSectionCollapseState(
  supabase: any,
  artifactId: string,
  sectionSlug: string,
  isCollapsed: boolean
) {
  // 1. Fetch current metadata
  const { data: artifact } = await supabase
    .from('artifacts')
    .select('section_metadata')
    .eq('id', artifactId)
    .single();
  
  // 2. Update collapse state
  const updatedMetadata = artifact.section_metadata.map((s: SectionMetadata) =>
    s.slug === sectionSlug ? { ...s, is_collapsed: isCollapsed } : s
  );
  
  // 3. Update database (only metadata, no count change)
  const { error } = await supabase
    .from('artifacts')
    .update({ section_metadata: updatedMetadata })
    .eq('id', artifactId);
  
  return { error };
}

// ============================================================================
// VALIDATION
// ============================================================================

/**
 * Validate section metadata structure
 */
export function validateSectionMetadata(metadata: SectionMetadata[]): boolean {
  // Check all required fields exist
  const isValid = metadata.every(section =>
    typeof section.slug === 'string' &&
    typeof section.title === 'string' &&
    typeof section.is_done === 'boolean' &&
    typeof section.is_collapsed === 'boolean' &&
    typeof section.order === 'number'
  );
  
  // Check order sequence is valid (1, 2, 3, ...)
  const orders = metadata.map(s => s.order).sort((a, b) => a - b);
  const hasValidOrder = orders.every((order, index) => order === index + 1);
  
  return isValid && hasValidOrder;
}

/**
 * Validate denormalized counts match metadata
 */
export function validateProgressCounts(artifact: Artifact): boolean {
  const actualTotal = artifact.section_metadata.length;
  const actualComplete = artifact.section_metadata.filter(s => s.is_done).length;
  
  return (
    artifact.sections_total === actualTotal &&
    artifact.sections_complete === actualComplete
  );
}
