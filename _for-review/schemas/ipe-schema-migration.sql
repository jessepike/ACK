-- ============================================================================
-- IPE v1.0 - Complete Database Schema
-- Supabase Migration File
-- ============================================================================
-- Run this in Supabase SQL Editor or via migration tool
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
-- Top-level container for IPE projects
-- One project goes through all 5 stages

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  
  -- Stage tracking
  current_stage TEXT NOT NULL DEFAULT 'discovery',
  -- Possible values: 'discovery' | 'design' | 'environment' | 'workflow' | 'implementation'
  
  -- Metadata
  created_by UUID, -- Future: reference to auth.users
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT valid_stage CHECK (
    current_stage IN ('discovery', 'design', 'environment', 'workflow', 'implementation')
  )
);

COMMENT ON TABLE projects IS 'Top-level IPE projects';
COMMENT ON COLUMN projects.current_stage IS 'Current active stage in the IPE workflow';

-- ============================================================================
-- ARTIFACTS TABLE (Hybrid: content + metadata)
-- ============================================================================
-- Documents like concept.md, research.md, stack.md, etc.
-- Uses HYBRID approach: Tiptap JSON content + separate metadata for fast queries

CREATE TABLE artifacts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Basic info
  name TEXT NOT NULL,           -- Display name: 'concept.md', 'research.md'
  slug TEXT NOT NULL,           -- URL-safe identifier: 'concept', 'research'
  stage TEXT NOT NULL,          -- Which stage this belongs to: 'discovery', 'design', etc.
  status TEXT NOT NULL DEFAULT 'draft', -- 'draft' | 'finalized'
  
  -- Content storage (Tiptap JSON document)
  content JSONB NOT NULL DEFAULT '{}',
  
  -- HYBRID APPROACH: Section metadata separate from content
  -- Enables fast queries for progress, done states, collapse states
  section_metadata JSONB NOT NULL DEFAULT '[]',
  -- Format: [{ slug: "what-is-it", title: "What Is It?", is_done: false, is_collapsed: false, order: 1 }]
  
  -- Denormalized progress tracking (for fast queries without parsing JSON)
  sections_total INT NOT NULL DEFAULT 0,
  sections_complete INT NOT NULL DEFAULT 0,
  
  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_status CHECK (status IN ('draft', 'finalized')),
  CONSTRAINT valid_progress CHECK (sections_complete <= sections_total),
  CONSTRAINT unique_artifact_per_stage UNIQUE(project_id, stage, slug)
);

COMMENT ON TABLE artifacts IS 'Individual documents (concept.md, research.md, etc.) with content + metadata';
COMMENT ON COLUMN artifacts.content IS 'Full Tiptap JSON document with all content';
COMMENT ON COLUMN artifacts.section_metadata IS 'Array of section metadata for fast queries (done states, collapse states)';
COMMENT ON COLUMN artifacts.sections_complete IS 'Denormalized count of completed sections for fast progress calculation';

-- Indexes for performance
CREATE INDEX idx_artifacts_project_stage ON artifacts(project_id, stage);
CREATE INDEX idx_artifacts_status ON artifacts(status);
CREATE INDEX idx_artifacts_progress ON artifacts(sections_complete, sections_total);

-- ============================================================================
-- ARTIFACT SNAPSHOTS TABLE (Versioning for key moments)
-- ============================================================================
-- Immutable historical records created at key moments:
-- - Stage transitions
-- - Before agent changes
-- - Finalization events
-- - Manual user snapshots

CREATE TABLE artifact_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  artifact_id UUID NOT NULL REFERENCES artifacts(id) ON DELETE CASCADE,
  
  -- Snapshot classification
  snapshot_type TEXT NOT NULL,
  -- 'stage_transition' - Created when completing a stage
  -- 'agent_change'     - Created before agent modifies content
  -- 'finalization'     - Created when marking artifact as finalized
  -- 'manual'           - User-requested version save
  
  -- Full snapshot of artifact state at this moment
  content JSONB NOT NULL,
  section_metadata JSONB NOT NULL,
  
  -- Attribution
  created_by TEXT NOT NULL, -- 'user' | 'claude' | 'research_agent' | user_id
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Optional change description for audit trail
  change_description TEXT,
  
  CONSTRAINT valid_snapshot_type CHECK (
    snapshot_type IN ('stage_transition', 'agent_change', 'finalization', 'manual')
  )
);

COMMENT ON TABLE artifact_snapshots IS 'Immutable version history captured at key moments';
COMMENT ON COLUMN artifact_snapshots.snapshot_type IS 'Classification of why this snapshot was created';

-- Index for fetching snapshots by artifact
CREATE INDEX idx_snapshots_artifact ON artifact_snapshots(artifact_id, created_at DESC);

-- ============================================================================
-- MESSAGES TABLE (Agent chat interactions)
-- ============================================================================
-- Stores conversation history between user and AI agents

CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  
  -- Optional: link message to specific artifact if context-specific
  artifact_id UUID REFERENCES artifacts(id) ON DELETE SET NULL,
  
  -- Message details
  role TEXT NOT NULL,           -- 'user' | 'assistant'
  agent_type TEXT,              -- 'claude' | 'research_agent' | NULL (for user messages)
  content TEXT NOT NULL,
  
  -- Optional: structured metadata for commands, tool calls, etc.
  metadata JSONB,
  -- Example: { "command": "/validate", "section_target": "what-is-it", "tool_calls": [...] }
  
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  CONSTRAINT valid_role CHECK (role IN ('user', 'assistant'))
);

COMMENT ON TABLE messages IS 'Chat history between user and AI agents';
COMMENT ON COLUMN messages.metadata IS 'Structured data for commands, tool calls, section targeting';

-- Indexes for chat queries
CREATE INDEX idx_messages_project ON messages(project_id, created_at DESC);
CREATE INDEX idx_messages_artifact ON messages(artifact_id, created_at DESC);

-- ============================================================================
-- STAGE DEFINITIONS TABLE (Reference data)
-- ============================================================================
-- Static reference table defining the 5 IPE stages and their expected artifacts

CREATE TABLE stage_definitions (
  slug TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  order_index INT NOT NULL UNIQUE,
  description TEXT,
  
  -- Expected artifacts for this stage (template definitions)
  expected_artifacts JSONB NOT NULL,
  -- Format: [{ slug: "concept", name: "concept.md", required: true, sections_count: 6 }]
  
  CONSTRAINT valid_order CHECK (order_index >= 1 AND order_index <= 5)
);

COMMENT ON TABLE stage_definitions IS 'Reference data for the 5 IPE stages';
COMMENT ON COLUMN stage_definitions.expected_artifacts IS 'Template definitions for artifacts in this stage';

-- Seed data for the 5 IPE stages
INSERT INTO stage_definitions (slug, name, order_index, description, expected_artifacts) VALUES
('discovery', 'Discovery', 1, 'Concept definition and validation research', 
  '[
    {"slug": "concept", "name": "concept.md", "required": true, "sections_count": 6},
    {"slug": "research", "name": "research.md", "required": true, "sections_count": 4},
    {"slug": "validation", "name": "validation.md", "required": true, "sections_count": 3},
    {"slug": "scope", "name": "scope.md", "required": true, "sections_count": 4}
  ]'::jsonb),
('design', 'Solution Design', 2, 'Technology stack, architecture, and data model', 
  '[
    {"slug": "stack", "name": "stack.md", "required": true, "sections_count": 5},
    {"slug": "architecture", "name": "architecture.md", "required": true, "sections_count": 4},
    {"slug": "data-model", "name": "data-model.md", "required": true, "sections_count": 3},
    {"slug": "context-schema", "name": "context-schema.md", "required": true, "sections_count": 3}
  ]'::jsonb),
('environment', 'Environment Setup', 3, 'Repository initialization, tooling, and scaffolding', 
  '[
    {"slug": "repo-init", "name": "repo-init.md", "required": true, "sections_count": 3},
    {"slug": "dependencies", "name": "dependencies.md", "required": true, "sections_count": 2},
    {"slug": "scaffolding", "name": "scaffolding.md", "required": true, "sections_count": 4}
  ]'::jsonb),
('workflow', 'Workflow Configuration', 4, 'Agent rules, development workflow, and operations', 
  '[
    {"slug": "agent-rules", "name": "agent-rules.md", "required": true, "sections_count": 4},
    {"slug": "dev-workflow", "name": "dev-workflow.md", "required": true, "sections_count": 3},
    {"slug": "operations", "name": "operations.md", "required": true, "sections_count": 3}
  ]'::jsonb),
('implementation', 'Implementation Planning', 5, 'Phases, milestones, gates, and task breakdown', 
  '[
    {"slug": "phases", "name": "phases.md", "required": true, "sections_count": 3},
    {"slug": "milestones", "name": "milestones.md", "required": true, "sections_count": 4},
    {"slug": "tasks", "name": "tasks.md", "required": true, "sections_count": 5}
  ]'::jsonb);

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Auto-update updated_at timestamp on UPDATE
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to projects table
CREATE TRIGGER update_projects_updated_at 
  BEFORE UPDATE ON projects
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

-- Apply to artifacts table
CREATE TRIGGER update_artifacts_updated_at 
  BEFORE UPDATE ON artifacts
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VIEWS (For convenience queries)
-- ============================================================================

-- Stage progress overview - aggregate progress across all artifacts in a stage
CREATE VIEW stage_progress AS
SELECT 
  p.id as project_id,
  p.name as project_name,
  p.current_stage,
  a.stage,
  COUNT(a.id) as total_artifacts,
  COUNT(a.id) FILTER (WHERE a.status = 'finalized') as finalized_artifacts,
  SUM(a.sections_total) as total_sections,
  SUM(a.sections_complete) as complete_sections,
  CASE 
    WHEN SUM(a.sections_total) > 0 
    THEN ROUND((SUM(a.sections_complete)::numeric / SUM(a.sections_total)::numeric) * 100, 1)
    ELSE 0 
  END as progress_percentage
FROM projects p
LEFT JOIN artifacts a ON p.id = a.project_id
GROUP BY p.id, p.name, p.current_stage, a.stage;

COMMENT ON VIEW stage_progress IS 'Aggregated progress metrics for each stage in a project';

-- Recent activity feed - combines messages and snapshots
CREATE VIEW recent_activity AS
SELECT 
  'message' as activity_type,
  m.id,
  m.project_id,
  m.artifact_id,
  m.role,
  m.content as activity_content,
  m.created_at
FROM messages m
UNION ALL
SELECT 
  'snapshot' as activity_type,
  s.id,
  a.project_id,
  s.artifact_id,
  s.created_by as role,
  COALESCE(s.change_description, 'Snapshot: ' || s.snapshot_type) as activity_content,
  s.created_at
FROM artifact_snapshots s
JOIN artifacts a ON s.artifact_id = a.id
ORDER BY created_at DESC;

COMMENT ON VIEW recent_activity IS 'Combined activity feed of messages and snapshots';

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) - Placeholder for future auth
-- ============================================================================
-- Uncomment when ready to implement auth

-- ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE artifacts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE artifact_snapshots ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Users can view their own projects"
--   ON projects FOR SELECT
--   USING (auth.uid() = created_by);

-- CREATE POLICY "Users can create projects"
--   ON projects FOR INSERT
--   WITH CHECK (auth.uid() = created_by);

-- (Add more policies as needed)

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
