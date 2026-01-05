---
type: artifact
stage: design
artifact: context-schema
description: "Agent context structure and prompt design (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Context Schema

## Overview

<!-- When to use this artifact -->

This document defines the context structure for AI agents in [Project Name]. Use this artifact when building applications that involve LLM-powered agents.

**Agent type:** [Conversational / Task-execution / Autonomous / Hybrid]

**Context strategy:** [Full context / Sliding window / RAG / Hybrid]

---

## Context Structure

### Context Layers

```
┌─────────────────────────────────────────┐
│         System Context (Static)         │
│    Identity, capabilities, constraints  │
├─────────────────────────────────────────┤
│        Domain Context (Semi-static)     │
│    Business rules, domain knowledge     │
├─────────────────────────────────────────┤
│       Session Context (Dynamic)         │
│    Conversation history, state          │
├─────────────────────────────────────────┤
│        Task Context (Per-request)       │
│    Current input, retrieved data        │
└─────────────────────────────────────────┘
```

### Layer Definitions

| Layer | Persistence | Update Frequency | Token Budget |
|-------|-------------|------------------|--------------|
| System | Permanent | Rarely | ~[X] tokens |
| Domain | Per-session | On domain change | ~[X] tokens |
| Session | Per-session | Every turn | ~[X] tokens |
| Task | Per-request | Every request | ~[X] tokens |

---

## System Context

### Agent Identity

```markdown
## Identity

You are [Agent Name], a [type of agent] that [primary function].

## Capabilities

You can:
- [Capability 1]
- [Capability 2]
- [Capability 3]

You cannot:
- [Limitation 1]
- [Limitation 2]

## Behavior Guidelines

- [Guideline 1]
- [Guideline 2]
- [Guideline 3]
```

### Response Format

```markdown
## Response Format

Always respond in the following format:
[Define expected output structure]

Example:
[Provide example response]
```

---

## Domain Context

### Domain Knowledge

```markdown
## Domain: [Domain Name]

### Key Concepts

- **[Concept 1]**: [Definition]
- **[Concept 2]**: [Definition]
- **[Concept 3]**: [Definition]

### Business Rules

1. [Rule 1]
2. [Rule 2]
3. [Rule 3]

### Terminology

| Term | Definition |
|------|------------|
| [Term 1] | [What it means in this domain] |
| [Term 2] | [What it means in this domain] |
```

### Domain-Specific Instructions

```markdown
## [Domain] Instructions

When working in this domain:
- [Instruction 1]
- [Instruction 2]
- [Instruction 3]
```

---

## Session Context

### State Structure

```typescript
interface SessionContext {
  sessionId: string;
  userId?: string;
  startedAt: Date;

  // Conversation tracking
  messageCount: number;
  lastActivity: Date;

  // Task state
  currentTask?: {
    type: string;
    status: 'pending' | 'in_progress' | 'complete';
    data: Record<string, unknown>;
  };

  // Memory
  conversationSummary?: string;
  keyFacts: string[];

  // Preferences
  userPreferences?: {
    [key: string]: unknown;
  };
}
```

### Conversation History

**Strategy:** [Full history / Sliding window / Summarization]

**Window size:** [X] messages or [X] tokens

**Summarization trigger:** [When to summarize]

```markdown
## Conversation History

[Format for including history in prompt]

Previous messages:
{{#each messages}}
{{role}}: {{content}}
{{/each}}
```

---

## Task Context

### Input Structure

```typescript
interface TaskContext {
  // User input
  userMessage: string;

  // Retrieved context (RAG)
  relevantDocuments?: {
    content: string;
    source: string;
    relevance: number;
  }[];

  // Current state
  currentData?: Record<string, unknown>;

  // Available actions
  availableTools?: string[];
}
```

### Dynamic Context Injection

```markdown
## Current Context

### User Request
{{userMessage}}

### Relevant Information
{{#if relevantDocuments}}
{{#each relevantDocuments}}
Source: {{source}}
{{content}}
---
{{/each}}
{{/if}}

### Current State
{{#if currentData}}
{{json currentData}}
{{/if}}
```

---

## Prompt Templates

### Main Prompt Template

```markdown
{{> systemContext}}

{{> domainContext}}

{{> sessionContext}}

{{> taskContext}}

---

Based on the above context, please respond to the user's request.
```

### Tool Use Template

```markdown
## Available Tools

{{#each tools}}
### {{name}}
{{description}}

Parameters:
{{#each parameters}}
- {{name}} ({{type}}): {{description}}
{{/each}}

{{/each}}

## Tool Use Format

To use a tool, respond with:
```json
{
  "tool": "tool_name",
  "parameters": { ... }
}
```
```

### Error Handling Template

```markdown
## Error Handling

If you encounter an error or cannot complete a task:

1. Acknowledge the issue clearly
2. Explain what went wrong (if known)
3. Suggest alternatives or next steps
4. Ask for clarification if needed

Do NOT:
- Make up information
- Pretend the error didn't happen
- Proceed with incomplete data
```

---

## Context Management

### Token Budget

| Component | Max Tokens | Priority |
|-----------|------------|----------|
| System context | [X] | Required |
| Domain context | [X] | Required |
| Session summary | [X] | High |
| Recent messages | [X] | High |
| Retrieved docs | [X] | Medium |
| Full history | [X] | Low (truncate first) |
| **Total budget** | **[X]** | |

### Truncation Strategy

```
1. Remove oldest conversation messages first
2. Summarize if history exceeds threshold
3. Limit retrieved documents by relevance score
4. Never truncate system or domain context
```

### Context Refresh

| Trigger | Action |
|---------|--------|
| Session timeout | Clear session context |
| Domain change | Reload domain context |
| Token overflow | Summarize and truncate |
| Error state | Reset to clean state |

---

## Retrieval (RAG) Configuration

### Embedding Model

**Model:** [text-embedding-ada-002 / etc.]

**Dimensions:** [X]

### Vector Store

**Technology:** [Pinecone / Chroma / pgvector / etc.]

**Index configuration:**
- Metric: [cosine / euclidean / dot product]
- Chunk size: [X] tokens
- Chunk overlap: [X] tokens

### Retrieval Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Top K | [X] | [Why this number] |
| Similarity threshold | [X] | [Why this threshold] |
| Max tokens from retrieval | [X] | [Token budget reason] |

---

## Agent Operations

### Available Operations

| Operation | Description | When Used |
|-----------|-------------|-----------|
| [Operation 1] | [What it does] | [Trigger condition] |
| [Operation 2] | [What it does] | [Trigger condition] |
| [Operation 3] | [What it does] | [Trigger condition] |

### Operation Flow

```
User Input
    ↓
Parse Intent
    ↓
Select Operation ────────┐
    ↓                    │
Gather Context           │
    ↓                    │
Execute ←────────────────┘
    ↓
Format Response
    ↓
Update State
    ↓
Return to User
```

---

## Testing Context

### Test Scenarios

| Scenario | Context Setup | Expected Behavior |
|----------|---------------|-------------------|
| [Scenario 1] | [Context state] | [What should happen] |
| [Scenario 2] | [Context state] | [What should happen] |
| [Scenario 3] | [Context state] | [What should happen] |

### Context Fixtures

```typescript
// Test context fixture
const testContext: FullContext = {
  system: { ... },
  domain: { ... },
  session: { ... },
  task: { ... },
};
```

---

## Open Questions

- [ ] [Context design question]
- [ ] [Prompt engineering decision]
- [ ] [RAG configuration to test]

---

## Related Documents

- [architecture.md](architecture.md) - System architecture
- [stack.md](stack.md) - AI/Agent technology choices
