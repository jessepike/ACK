# Context Schema: ACK

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
stage: "design"
---

## Overview

<!-- 
How do agents understand ACK state?
- What context do agents see?
- How is context structured?
- How do agents reference/modify context?
-->

**Goal:** Define a structured way for AI agents to:
1. Read current project/artifact state
2. Target specific sections for updates
3. Understand relationships between artifacts
4. Make informed suggestions


**Key principle:** Agents should have enough context to be helpful, but not so much they get overwhelmed.



## Context Structure

<!-- 
What information is available to agents?
- Hierarchy
- Metadata
- Content access
-->

### Full Context Schema

```typescript
interface AgentContext {
  project: ProjectContext;
  currentArtifact: ArtifactContext;
  relatedArtifacts: ArtifactContext[];
  chatHistory: MessageContext[];
  systemState: SystemState;
}
```

### Project Context

```typescript
interface ProjectContext {
  id: string;
  name: string;
  description: string;
  current_stage: StageType;
  
  // Stage progress summary
  stages: {
    [stage: string]: {
      artifacts_total: number;
      artifacts_finalized: number;
      sections_complete: number;
      sections_total: number;
      progress_pct: number;
    }
  };
  
  created_at: Date;
  updated_at: Date;
}
```

**Example:**
```json
{
  "project": {
    "id": "abc123",
    "name": "ack-demo",
    "current_stage": "discovery",
    "stages": {
      "discovery": {
        "artifacts_total": 4,
        "artifacts_finalized": 2,
        "sections_complete": 9,
        "sections_total": 17,
        "progress_pct": 52.9
      }
    }
  }
}
```


### Artifact Context

```typescript
interface ArtifactContext {
  id: string;
  name: string;
  slug: string;
  stage: StageType;
  status: 'draft' | 'finalized';
  
  // Section structure (metadata only, not content)
  sections: {
    slug: string;
    title: string;
    is_done: boolean;
    is_collapsed: boolean;
    order: number;
    // Content excerpt for context (first 200 chars)
    preview?: string;
  }[];
  
  // Full content (only for current artifact)
  content?: string;  // Markdown representation
  
  sections_complete: number;
  sections_total: number;
  updated_at: Date;
}
```

**Example:**
```json
{
  "currentArtifact": {
    "name": "concept.md",
    "slug": "concept",
    "status": "draft",
    "sections": [
      {
        "slug": "what-is-it",
        "title": "What Is It?",
        "is_done": true,
        "preview": "ACK (Agent Context Kit) is a planning layer..."
      },
      {
        "slug": "problem-being-solved",
        "title": "Problem Being Solved",
        "is_done": false,
        "preview": null
      }
    ],
    "content": "# Project Concept: ACK\n\n## What Is It?\n\n..."
  }
}
```



## Context Injection Strategy

<!-- 
When and how to inject context into agent prompts:
- Full context vs. selective
- Token budget management
- Context relevance
-->

### Context Levels

**Level 1: Minimal (Free chat)**
- Project name and stage
- Current artifact name
- No content

**Level 2: Standard (Section targeting)**
- Project summary
- Current artifact structure (section list)
- Specific section content if referenced

**Level 3: Full (Deep analysis)**
- All Level 2 info
- Full current artifact content
- Related artifacts (summaries)


### Token Budget Allocation

**Assuming 200k token context window:**

| Component | Tokens | Allocation |
|-----------|--------|------------|
| System prompt | 2k | 1% |
| Project context | 1k | 0.5% |
| Current artifact | 10k | 5% |
| Related artifacts | 5k | 2.5% |
| Chat history | 20k | 10% |
| Agent response | 20k | 10% |
| **Reserve** | **142k** | **71%** |


### Selective Context Loading

**Rules for what to include:**

1. **Always include:**
   - Project name and stage
   - Current artifact name and status
   - Section list (titles + done states)

2. **Include if referenced:**
   - Specific section content
   - Related artifact summaries
   - Previous snapshots

3. **Never include:**
   - Deleted content
   - Other users' private notes
   - System internals



## Agent Operations

<!-- 
How do agents modify ACK state?
- Supported operations
- Operation format
- Validation
-->

### Supported Operations

**1. Update Section Content**
```json
{
  "operation": "update_section",
  "artifact_slug": "concept",
  "section_slug": "what-is-it",
  "content": "Updated content here...",
  "reason": "Clarified definition based on research"
}
```

**2. Mark Section Done**
```json
{
  "operation": "mark_section_done",
  "artifact_slug": "concept",
  "section_slug": "problem-being-solved",
  "is_done": true
}
```

**3. Create New Section**
```json
{
  "operation": "create_section",
  "artifact_slug": "concept",
  "after_section": "core-features",
  "title": "Technical Requirements",
  "content": "...",
  "order": 4
}
```

**4. Suggest Edit**
```json
{
  "operation": "suggest_edit",
  "artifact_slug": "research",
  "section_slug": "competitive-analysis",
  "suggestion": "Add comparison of pricing models",
  "rationale": "User asked about pricing validation"
}
```


### Operation Validation

**Before applying:**
1. Verify artifact exists
2. Verify section exists (for updates)
3. Check artifact is not finalized (unless override)
4. Validate content structure
5. Create snapshot


**After applying:**
1. Update section_metadata
2. Recalculate sections_complete
3. Log operation in messages
4. Trigger UI update



## Agent Targeting Syntax

<!-- 
How do users reference sections in chat?
- Natural language
- Structured syntax
- Ambiguity resolution
-->

### Natural Language Examples

**User:** "Update the problem statement"
**Agent parses:**
```json
{
  "artifact": "concept",  // inferred from context
  "section": "problem-being-solved"  // matched by title
}
```

**User:** "Fix the competitive analysis in research.md"
**Agent parses:**
```json
{
  "artifact": "research",  // explicit
  "section": "competitive-analysis"  // matched
}
```


### Structured Commands

**Explicit syntax:**
```
@concept#what-is-it update the definition
/research competitive-analysis add Cursor pricing
```

**Format:**
- `@artifact_slug#section_slug` - Full reference
- `/artifact_slug section_slug` - Command format
- `#section_slug` - Section in current artifact


### Ambiguity Resolution

**Multiple artifacts have "Overview" section:**
```
User: "Update the overview"
Agent: "I found 'Overview' in concept.md and research.md. Which would you like to update?"
```

**Section title partial match:**
```
User: "Update the problem section"
Agent: "Did you mean 'Problem Being Solved' in concept.md?"
```



## Context Refresh Strategy

<!-- 
When to reload context:
- On artifact change
- On stage transition
- On agent request
-->

### Auto-Refresh Triggers

**Refresh full context when:**
1. User switches artifacts
2. User switches stages
3. Agent completes update operation
4. User explicitly asks for refresh


### Incremental Updates

**Update only changed parts when:**
1. Section done state changes
2. New message added
3. Progress counts update


### Context Staleness Detection

**Warn if:**
- Context is > 5 minutes old during active session
- Agent references outdated section count
- User made changes not reflected in agent's view



## Agent Prompt Templates

<!-- 
Standard prompts with context injection:
-->

### Basic Chat Prompt

```markdown
You are an AI assistant helping with ACK (Agent Context Kit).

## Current Context
Project: {{project.name}}
Stage: {{project.current_stage}}
Artifact: {{currentArtifact.name}} ({{currentArtifact.sections_complete}}/{{currentArtifact.sections_total}} complete)

## Available Sections
{{#each currentArtifact.sections}}
- [{{#if is_done}}✓{{else}} {{/if}}] {{title}} ({{slug}})
{{/each}}

## Instructions
- Help the user work on their ACK artifacts
- Reference sections using their titles
- Suggest updates using structured operations
- Ask for clarification if ambiguous

## User Message
{{userMessage}}
```


### Research Agent Prompt

```markdown
You are a research agent for ACK projects.

## Task
Research: {{researchQuery}}

## Context
Current artifact: {{currentArtifact.name}}
Target section: {{targetSection}}

## Instructions
1. Search for relevant information
2. Synthesize findings
3. Format as markdown
4. Suggest update to {{targetSection}}

## Output Format
{
  "findings": "...",
  "sources": [...],
  "suggested_content": "...",
  "operation": {
    "operation": "update_section",
    "artifact_slug": "{{currentArtifact.slug}}",
    "section_slug": "{{targetSection}}",
    "content": "..."
  }
}
```



## Context Serialization

<!-- 
How to convert context to/from JSON:
-->

### Serialization Format

**To JSON:**
```typescript
function serializeContext(context: AgentContext): string {
  return JSON.stringify({
    project: {
      name: context.project.name,
      stage: context.project.current_stage,
      // ... 
    },
    artifact: {
      // Convert Tiptap JSON to Markdown
      content: tiptapToMarkdown(context.currentArtifact.content),
      // ...
    }
  }, null, 2);
}
```

**From JSON:**
```typescript
function deserializeOperation(json: string): AgentOperation {
  const parsed = JSON.parse(json);
  
  // Validate operation
  const validated = AgentOperationSchema.parse(parsed);
  
  return validated;
}
```



## Error Handling

<!-- 
How to handle context errors:
-->

### Common Errors

**1. Section not found:**
```json
{
  "error": "SECTION_NOT_FOUND",
  "message": "Section 'xyz' not found in artifact 'concept'",
  "suggestions": [
    "what-is-it",
    "problem-being-solved"
  ]
}
```

**2. Artifact finalized:**
```json
{
  "error": "ARTIFACT_FINALIZED",
  "message": "Cannot modify finalized artifact 'concept'",
  "action": "Ask user to un-finalize or create snapshot"
}
```

**3. Context too large:**
```json
{
  "error": "CONTEXT_TOO_LARGE",
  "message": "Artifact content exceeds token limit",
  "action": "Summarizing content or requesting specific sections"
}
```



---

## Implementation Checklist

<!-- 
What needs to be built:
-->

- [ ] Context builder function (AgentContext assembly)
- [ ] Tiptap → Markdown converter
- [ ] Operation parser (natural language → structured)
- [ ] Operation validator
- [ ] Operation executor
- [ ] Context refresh logic
- [ ] Prompt template system
- [ ] Error handling for all operations


## Open Questions

- [ ] Should agents see chat history from other artifacts?
- [ ] How to handle multi-artifact operations (e.g., "compare concept and research")?
- [ ] What's the max context size before we need summarization?
- [ ] Should we cache serialized context?
- [ ]
