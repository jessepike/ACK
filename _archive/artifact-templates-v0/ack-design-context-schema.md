---
type: artifact
stage: design
artifact: context-schema
description: "Agent context structure, operations, and injection strategy"
version: 1.0.0
updated: "2026-01-04T09:26:12"
status: draft
---

# [Project Name] - Context Schema

## Overview

<!-- How do agents understand system state? -->

**Goal:** Define a structured way for AI agents to:
1. Read current project/system state
2. Target specific resources for updates
3. Understand relationships between entities
4. Make informed suggestions

**Key principle:** [Guiding principle for context design]

---

## Context Structure

<!-- What information is available to agents? -->

### Full Context Schema

```typescript
interface AgentContext {
  [contextKey]: [ContextType];
  [contextKey]: [ContextType];
  [contextKey]: [ContextType];
  [contextKey]: [ContextType];
}
```

### [Context Component 1]

```typescript
interface [ComponentName]Context {
  id: string;
  [field]: [type];
  [field]: [type];

  // [Category of fields]
  [field]: {
    [subfield]: [type];
    [subfield]: [type];
  };
}
```

**Example:**
```json
{
  "[contextKey]": {
    "id": "[example-id]",
    "[field]": "[value]"
  }
}
```


### [Context Component 2]

```typescript
interface [ComponentName]Context {
  id: string;
  [field]: [type];

  // [Description]
  [field]: {
    [subfield]: [type];
    [subfield]: [type];
  }[];

  // [Description]
  [field]?: [type];
}
```

**Example:**
```json
{
  "[contextKey]": {
    "[field]": "[value]",
    "[arrayField]": [
      {
        "[subfield]": "[value]"
      }
    ]
  }
}
```

---

## Context Injection Strategy

<!-- When and how to inject context into agent prompts -->

### Context Levels

**Level 1: Minimal**
- [What's included]
- [What's included]
- Use case: [When to use]

**Level 2: Standard**
- [What's included]
- [What's included]
- [What's included]
- Use case: [When to use]

**Level 3: Full**
- All Level 2 info
- [Additional info]
- [Additional info]
- Use case: [When to use]


### Token Budget Allocation

**Assuming [X]k token context window:**

| Component | Tokens | Allocation |
|-----------|--------|------------|
| System prompt | [X]k | [X]% |
| [Context 1] | [X]k | [X]% |
| [Context 2] | [X]k | [X]% |
| [Context 3] | [X]k | [X]% |
| Agent response | [X]k | [X]% |
| **Reserve** | **[X]k** | **[X]%** |


### Selective Context Loading

**Rules for what to include:**

1. **Always include:**
   - [Required context]
   - [Required context]
   - [Required context]

2. **Include if referenced:**
   - [Conditional context]
   - [Conditional context]

3. **Never include:**
   - [Excluded context]
   - [Excluded context]

---

## Agent Operations

<!-- How do agents modify system state? -->

### Supported Operations

**1. [Operation Name]**
```json
{
  "operation": "[operation_type]",
  "[field]": "[value]",
  "[field]": "[value]",
  "reason": "[Why this change]"
}
```

**2. [Operation Name]**
```json
{
  "operation": "[operation_type]",
  "[field]": "[value]",
  "[field]": [boolean]
}
```

**3. [Operation Name]**
```json
{
  "operation": "[operation_type]",
  "[field]": "[value]",
  "[field]": "[value]",
  "[field]": [number]
}
```

**4. [Operation Name]**
```json
{
  "operation": "[operation_type]",
  "[field]": "[value]",
  "suggestion": "[Suggested change]",
  "rationale": "[Why suggested]"
}
```


### Operation Validation

**Before applying:**
1. [Validation step]
2. [Validation step]
3. [Validation step]
4. [Validation step]

**After applying:**
1. [Post-operation step]
2. [Post-operation step]
3. [Post-operation step]

---

## Agent Targeting Syntax

<!-- How do users reference resources in chat? -->

### Natural Language Examples

**User:** "[Example user input]"
**Agent parses:**
```json
{
  "[field]": "[inferred value]",
  "[field]": "[matched value]"
}
```

**User:** "[Example user input]"
**Agent parses:**
```json
{
  "[field]": "[explicit value]",
  "[field]": "[matched value]"
}
```


### Structured Commands

**Explicit syntax:**
```
@[resource]#[target] [action]
/[resource] [target] [action]
#[target] [action in current context]
```

**Format:**
- `@[slug]#[slug]` - Full reference
- `/[slug] [slug]` - Command format
- `#[slug]` - Target in current context


### Ambiguity Resolution

**Multiple matches:**
```
User: "[ambiguous input]"
Agent: "I found '[target]' in [location 1] and [location 2]. Which would you like to [action]?"
```

**Partial match:**
```
User: "[partial input]"
Agent: "Did you mean '[full match]' in [location]?"
```

---

## Context Refresh Strategy

<!-- When to reload context -->

### Auto-Refresh Triggers

**Refresh full context when:**
1. [Trigger condition]
2. [Trigger condition]
3. [Trigger condition]
4. [Trigger condition]


### Incremental Updates

**Update only changed parts when:**
1. [Condition]
2. [Condition]
3. [Condition]


### Context Staleness Detection

**Warn if:**
- Context is > [X] minutes old during active session
- Agent references outdated [data]
- User made changes not reflected in agent's view

---

## Agent Prompt Templates

<!-- Standard prompts with context injection -->

### Basic Chat Prompt

```markdown
You are an AI assistant helping with [Project Name].

## Current Context
[ContextKey]: {{context.field}}
[ContextKey]: {{context.field}}
[ContextKey]: {{context.field}} ({{context.subfield}}/{{context.subfield}} complete)

## Available [Resources]
{{#each context.resources}}
- [{{#if condition}}✓{{else}} {{/if}}] {{field}} ({{field}})
{{/each}}

## Instructions
- [Instruction 1]
- [Instruction 2]
- [Instruction 3]
- [Instruction 4]

## User Message
{{userMessage}}
```


### [Specialized Agent] Prompt

```markdown
You are a [specialized] agent for [Project Name].

## Task
[TaskType]: {{taskInput}}

## Context
[ContextField]: {{context.field}}
[ContextField]: {{context.field}}

## Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

## Output Format
{
  "[field]": "...",
  "[field]": [...],
  "[field]": "...",
  "operation": {
    "operation": "[operation_type]",
    "[field]": "{{context.field}}",
    "[field]": "..."
  }
}
```

---

## Context Serialization

<!-- How to convert context to/from JSON -->

### Serialization Format

**To JSON:**
```typescript
function serializeContext(context: AgentContext): string {
  return JSON.stringify({
    [field]: {
      [subfield]: context.[field].[subfield],
      // ...
    },
    [field]: {
      // Convert [format] to [format]
      [subfield]: convert(context.[field].[subfield]),
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

---

## Error Handling

<!-- How to handle context errors -->

### Common Errors

**1. [Resource] not found:**
```json
{
  "error": "[ERROR_CODE]",
  "message": "[Resource] '[id]' not found in [location]",
  "suggestions": [
    "[suggestion-1]",
    "[suggestion-2]"
  ]
}
```

**2. [Resource] locked:**
```json
{
  "error": "[ERROR_CODE]",
  "message": "Cannot modify [locked resource]",
  "action": "[Suggested action]"
}
```

**3. Context too large:**
```json
{
  "error": "[ERROR_CODE]",
  "message": "[Resource] content exceeds token limit",
  "action": "[Suggested action]"
}
```

---

## Implementation Checklist

- [ ] Context builder function
- [ ] [Format] converter
- [ ] Operation parser (natural language → structured)
- [ ] Operation validator
- [ ] Operation executor
- [ ] Context refresh logic
- [ ] Prompt template system
- [ ] Error handling for all operations

---

## Open Questions

- [ ] [Context design question]
- [ ] [Multi-resource operation handling]
- [ ] [Context size limits]
- [ ] [Caching strategy]
