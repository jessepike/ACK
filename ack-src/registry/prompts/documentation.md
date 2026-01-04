---
doc_id: "prompt-006"
slug: "documentation"
title: "Documentation Prompt"
type: "prompt"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: []
---

# Documentation Prompt

Generate clear, useful documentation.

## Documentation Types

### README
```markdown
# Project Name

One-line description.

## Quick Start
[Minimum steps to run]

## Features
[Bullet list]

## Installation
[Step by step]

## Usage
[Common use cases with examples]

## Configuration
[Environment variables, config files]

## Contributing
[How to contribute]

## License
[License type]
```

### Function/Module
```typescript
/**
 * Brief description of what it does.
 * 
 * @param name - Description of parameter
 * @returns Description of return value
 * @throws {ErrorType} When this happens
 * 
 * @example
 * const result = functionName('input')
 * // result: expected output
 */
```

### API Endpoint
```markdown
## POST /api/users

Create a new user.

### Request
```json
{
  "email": "user@example.com",
  "name": "User Name"
}
```

### Response
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### Errors
| Code | Description |
|------|-------------|
| 400 | Invalid input |
| 409 | Email already exists |
```

## Rules

1. Lead with what it does, not how
2. Include runnable examples
3. Document the "why" for non-obvious decisions
4. Keep it current
5. Write for the reader who knows nothing

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
