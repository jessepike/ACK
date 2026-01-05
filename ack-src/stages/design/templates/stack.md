---
type: artifact
stage: design
artifact: stack
description: "Technology choices with rationale"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Technology Stack

## Overview

<!-- Brief summary of stack philosophy -->

This document defines the technology choices for [Project Name] with rationale for each decision.

**Stack philosophy:**
- [Guiding principle 1 - e.g., "Prefer boring technology"]
- [Guiding principle 2 - e.g., "Optimize for developer experience"]
- [Guiding principle 3 - e.g., "Minimize operational complexity"]

---

## Stack Summary

| Layer | Technology | Version |
|-------|------------|---------|
| Language | [TypeScript / Python / Go / etc.] | [X.Y] |
| Frontend | [React / Vue / Svelte / None] | [X.Y] |
| Backend | [Next.js / Express / FastAPI / etc.] | [X.Y] |
| Database | [PostgreSQL / MongoDB / SQLite] | [X.Y] |
| ORM | [Prisma / Drizzle / TypeORM / None] | [X.Y] |
| Hosting | [Vercel / AWS / Railway / etc.] | - |
| CI/CD | [GitHub Actions / GitLab CI / etc.] | - |

---

## Language & Runtime

### Primary Language: [Language]

**Version:** [X.Y.Z]

**Rationale:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Alternatives considered:**

| Alternative | Why Not |
|-------------|---------|
| [Language A] | [Reason] |
| [Language B] | [Reason] |

---

## Frontend

### Framework: [Framework Name]

**Version:** [X.Y.Z]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives considered:**

| Alternative | Why Not |
|-------------|---------|
| [Framework A] | [Reason] |
| [Framework B] | [Reason] |

### State Management: [Library]

**Version:** [X.Y.Z]

**Rationale:**
- [Why this approach]

### Styling: [Approach]

**Technology:** [Tailwind / CSS Modules / Styled Components / etc.]

**Version:** [X.Y.Z]

**Rationale:**
- [Why this approach]

### Build Tool: [Tool]

**Technology:** [Vite / Webpack / Turbopack / etc.]

**Version:** [X.Y.Z]

---

## Backend

### Framework: [Framework Name]

**Version:** [X.Y.Z]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives considered:**

| Alternative | Why Not |
|-------------|---------|
| [Framework A] | [Reason] |
| [Framework B] | [Reason] |

### API Approach: [REST / GraphQL / tRPC]

**Rationale:**
- [Why this approach]

### Authentication: [Approach]

**Technology:** [NextAuth / Passport / Custom JWT / etc.]

**Rationale:**
- [Why this approach]

---

## Database

### Primary Database: [Database]

**Version:** [X.Y.Z]

**Hosting:** [Self-hosted / Managed - Provider]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives considered:**

| Alternative | Why Not |
|-------------|---------|
| [Database A] | [Reason] |
| [Database B] | [Reason] |

### ORM / Query Builder: [Tool]

**Version:** [X.Y.Z]

**Rationale:**
- [Why this tool]

### Caching (if applicable)

**Technology:** [Redis / In-memory / None]

**Rationale:**
- [Why this approach]

---

## AI / Agents (if applicable)

### LLM Provider: [Provider]

**Model:** [Model name]

**Rationale:**
- [Why this provider/model]

### Agent Framework: [Framework]

**Version:** [X.Y.Z]

**Rationale:**
- [Why this framework]

---

## Infrastructure

### Hosting: [Provider]

**Service:** [Specific service - e.g., Vercel, AWS Lambda, EC2]

**Rationale:**
- [Reason 1]
- [Reason 2]

**Alternatives considered:**

| Alternative | Why Not |
|-------------|---------|
| [Provider A] | [Reason] |
| [Provider B] | [Reason] |

### CDN (if applicable)

**Provider:** [Cloudflare / AWS CloudFront / Vercel Edge]

**Rationale:**
- [Why needed / why this provider]

### Domain & DNS

**Registrar:** [Provider]
**DNS:** [Provider]

---

## Development Tools

### Package Manager: [Tool]

**Technology:** [npm / pnpm / yarn / bun]

**Version:** [X.Y.Z]

### Linting: [Tool]

**Technology:** [ESLint / Biome / etc.]

**Config:** [Preset or custom]

### Formatting: [Tool]

**Technology:** [Prettier / Biome / etc.]

### Type Checking: [Tool]

**Technology:** [TypeScript / JSDoc / None]

**Strictness:** [Strict / Standard]

---

## Testing

### Unit Testing: [Framework]

**Technology:** [Vitest / Jest / pytest / etc.]

**Version:** [X.Y.Z]

### Integration Testing: [Framework]

**Technology:** [Same as unit / Different]

### E2E Testing (if applicable): [Framework]

**Technology:** [Playwright / Cypress / None]

**Version:** [X.Y.Z]

---

## CI/CD

### Platform: [Platform]

**Technology:** [GitHub Actions / GitLab CI / CircleCI]

### Pipeline Stages

| Stage | Purpose | Trigger |
|-------|---------|---------|
| Lint | Code quality | All PRs |
| Test | Run tests | All PRs |
| Build | Verify build | All PRs |
| Deploy (staging) | Preview deploy | PRs to main |
| Deploy (prod) | Production | Merge to main |

---

## Monitoring & Observability

### Error Tracking: [Tool]

**Technology:** [Sentry / Bugsnag / None]

**Rationale:**
- [Why this tool]

### Logging: [Approach]

**Technology:** [Console / Structured logging / Log service]

### Analytics (if applicable): [Tool]

**Technology:** [Plausible / PostHog / Google Analytics / None]

---

## Security

### Secrets Management

**Approach:** [Environment variables / Secrets manager]

**Tools:** [Doppler / AWS Secrets Manager / .env files]

### Dependency Scanning

**Tool:** [Dependabot / Snyk / npm audit]

---

## Cost Considerations

| Service | Tier | Estimated Cost |
|---------|------|----------------|
| Hosting | [Tier] | $X/month |
| Database | [Tier] | $X/month |
| [Service] | [Tier] | $X/month |
| **Total** | | **$X/month** |

**Notes:**
- [Cost optimization considerations]
- [Scale implications]

---

## Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [package-1] | ^X.Y.Z | [What it does] |
| [package-2] | ^X.Y.Z | [What it does] |
| [package-3] | ^X.Y.Z | [What it does] |

See [dependencies.md](dependencies.md) for full dependency analysis.

---

## Version Policy

### Update Strategy

- **Security updates:** Apply immediately
- **Patch updates:** Apply within [timeframe]
- **Minor updates:** Evaluate and apply [frequency]
- **Major updates:** Plan and test before applying

### Lock File

- **Tool:** [package-lock.json / pnpm-lock.yaml / etc.]
- **Committed:** Yes
- **CI verification:** Yes

---

## Open Questions

- [ ] [Stack decision to finalize]
- [ ] [Technology to evaluate]
- [ ] [Cost to verify]

---

## Related Documents

- [architecture.md](architecture.md) - System architecture
- [data-model.md](data-model.md) - Database schema
- [dependencies.md](dependencies.md) - Full dependency analysis
- [brief.md](../../discover/templates/brief.md) - Constraints and requirements
