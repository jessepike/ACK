---
type: artifact
stage: design
artifact: dependencies
description: "Package evaluation and dependency analysis (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Dependencies

## Overview

<!-- When to use this artifact -->

This document evaluates and justifies package dependencies for [Project Name]. Use this artifact when significant dependency decisions need documentation.

**Package manager:** [npm / pnpm / yarn / bun]

**Lock file:** [package-lock.json / pnpm-lock.yaml / etc.]

---

## Dependency Summary

| Category | Count | Notes |
|----------|-------|-------|
| Production | [X] | Runtime dependencies |
| Development | [X] | Build/test tooling |
| Peer | [X] | Framework requirements |
| **Total** | **[X]** | |

---

## Production Dependencies

### Core Framework

| Package | Version | Purpose | Alternatives Considered |
|---------|---------|---------|------------------------|
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |

### Data & State

| Package | Version | Purpose | Alternatives Considered |
|---------|---------|---------|------------------------|
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |

### UI Components (if applicable)

| Package | Version | Purpose | Alternatives Considered |
|---------|---------|---------|------------------------|
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |

### Utilities

| Package | Version | Purpose | Alternatives Considered |
|---------|---------|---------|------------------------|
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |
| [package] | ^X.Y.Z | [What it does] | [Why not alternatives] |

---

## Development Dependencies

### Build Tools

| Package | Version | Purpose |
|---------|---------|---------|
| [package] | ^X.Y.Z | [What it does] |
| [package] | ^X.Y.Z | [What it does] |

### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| [package] | ^X.Y.Z | [What it does] |
| [package] | ^X.Y.Z | [What it does] |

### Linting & Formatting

| Package | Version | Purpose |
|---------|---------|---------|
| [package] | ^X.Y.Z | [What it does] |
| [package] | ^X.Y.Z | [What it does] |

### Type Definitions

| Package | Version | Purpose |
|---------|---------|---------|
| @types/[package] | ^X.Y.Z | TypeScript types |
| @types/[package] | ^X.Y.Z | TypeScript types |

---

## Dependency Evaluation

### [Package Name] Evaluation

**Category:** [Core / Data / UI / Utility / etc.]

**Current version:** ^X.Y.Z

**Purpose:** [What this package does for the project]

**Evaluation criteria:**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Maintenance | Active / Slow / Inactive | [Last release date, commit activity] |
| Popularity | High / Medium / Low | [Downloads, GitHub stars] |
| Bundle size | [X kb] | [Acceptable / Concern] |
| Type support | Native / DefinitelyTyped / None | [Quality of types] |
| Documentation | Good / Adequate / Poor | [Quality assessment] |
| Breaking changes | Rare / Occasional / Frequent | [History] |

**Alternatives considered:**

| Alternative | Why Not Chosen |
|-------------|----------------|
| [Package A] | [Reason] |
| [Package B] | [Reason] |
| Build custom | [Reason] |

**Decision:** Use [package] because [primary reason].

---

### [Package Name] Evaluation

**Category:** [Category]

**Current version:** ^X.Y.Z

**Purpose:** [What this package does]

**Evaluation criteria:**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Maintenance | Active / Slow / Inactive | [Notes] |
| Popularity | High / Medium / Low | [Notes] |
| Bundle size | [X kb] | [Notes] |
| Type support | Native / DefinitelyTyped / None | [Notes] |
| Documentation | Good / Adequate / Poor | [Notes] |
| Breaking changes | Rare / Occasional / Frequent | [Notes] |

**Alternatives considered:**

| Alternative | Why Not Chosen |
|-------------|----------------|
| [Package A] | [Reason] |
| [Package B] | [Reason] |

**Decision:** Use [package] because [primary reason].

---

## Bundle Analysis

### Bundle Size Impact

| Package | Size (min+gzip) | Tree-shakeable? | Impact |
|---------|-----------------|-----------------|--------|
| [package] | [X kb] | Yes / No | Low / Medium / High |
| [package] | [X kb] | Yes / No | Low / Medium / High |
| [package] | [X kb] | Yes / No | Low / Medium / High |

**Total estimated bundle impact:** [X kb]

### Size Optimization Strategies

- [ ] Use tree-shaking where available
- [ ] Consider lighter alternatives for heavy packages
- [ ] Lazy load non-critical dependencies
- [ ] Use subpath imports where supported

---

## Security Considerations

### Known Vulnerabilities

| Package | Severity | Status | Mitigation |
|---------|----------|--------|------------|
| [package] | High / Medium / Low | Fixed in vX.Y.Z / No fix | [Action] |

### Security Scanning

**Tool:** [npm audit / Snyk / Dependabot]

**Frequency:** [On PR / Daily / Weekly]

**Policy:**
- Critical: Block merge, fix immediately
- High: Block merge, fix within [X] days
- Medium: Warning, fix within [X] days
- Low: Track, fix in maintenance cycles

---

## Version Policy

### Pinning Strategy

| Category | Strategy | Example |
|----------|----------|---------|
| Core framework | Pin minor | ^X.Y.0 |
| Critical deps | Pin minor | ^X.Y.0 |
| Utilities | Allow minor | ^X.Y.Z |
| Dev deps | Allow minor | ^X.Y.Z |

### Update Policy

| Update Type | Approach | Frequency |
|-------------|----------|-----------|
| Security patches | Immediate | As needed |
| Patch versions | Automatic | Weekly |
| Minor versions | Review & test | Monthly |
| Major versions | Planned upgrade | Quarterly / As needed |

### Renovation/Dependabot Config

```json
{
  "extends": ["config:base"],
  "schedule": ["every weekend"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["breaking-change"]
    }
  ]
}
```

---

## Peer Dependencies

| Package | Required By | Version Range |
|---------|-------------|---------------|
| react | [packages] | ^18.0.0 |
| [package] | [packages] | ^X.Y.Z |

---

## Rejected Packages

Packages evaluated but not included:

| Package | Reason Not Included |
|---------|---------------------|
| [package] | [Reason - too heavy, unmaintained, etc.] |
| [package] | [Reason] |
| [package] | [Reason] |

---

## Custom vs. Package Decision Log

| Functionality | Decision | Rationale |
|---------------|----------|-----------|
| [Feature 1] | Use package | [Why package is better] |
| [Feature 2] | Build custom | [Why custom is better] |
| [Feature 3] | Use package | [Why package is better] |

---

## Open Questions

- [ ] [Dependency decision to make]
- [ ] [Package to evaluate]
- [ ] [Version constraint to verify]

---

## Related Documents

- [stack.md](stack.md) - Technology choices
- [architecture.md](architecture.md) - System architecture
