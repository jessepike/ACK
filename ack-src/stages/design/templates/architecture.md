---
type: artifact
stage: design
artifact: architecture
description: "System architecture, components, and data flow"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - Architecture

## Overview

<!-- High-level system description -->

[Project Name] is a [type of system] that [what it does]. This document defines the system architecture, component structure, and data flow.

**Architecture style:** [e.g., Monolith, Microservices, Serverless, Modular monolith]

**Key characteristics:**
- [Characteristic 1 - e.g., API-first]
- [Characteristic 2 - e.g., Event-driven]
- [Characteristic 3 - e.g., Stateless services]

---

## System Diagram

<!-- ASCII diagram or description of high-level architecture -->

```
┌─────────────────────────────────────────────────────────┐
│                       Client                            │
│                   (Browser/App)                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                          │
│                  (Authentication)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Service A│  │Service B│  │Service C│
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └─────────────┼───────────┘
                      ▼
              ┌─────────────┐
              │  Database   │
              └─────────────┘
```

---

## Components

### Component 1: [Name]

**Responsibility:** [Single sentence describing what this component does]

**Type:** [Service / Module / Library / External]

**Interfaces:**
- **Inputs:** [What data/requests it receives]
- **Outputs:** [What data/responses it produces]

**Dependencies:**
- [Component it depends on]
- [External service it uses]

**Key considerations:**
- [Important design decision or constraint]

---

### Component 2: [Name]

**Responsibility:** [Single sentence describing what this component does]

**Type:** [Service / Module / Library / External]

**Interfaces:**
- **Inputs:** [What data/requests it receives]
- **Outputs:** [What data/responses it produces]

**Dependencies:**
- [Component it depends on]

**Key considerations:**
- [Important design decision or constraint]

---

### Component 3: [Name]

**Responsibility:** [Single sentence describing what this component does]

**Type:** [Service / Module / Library / External]

**Interfaces:**
- **Inputs:** [What data/requests it receives]
- **Outputs:** [What data/responses it produces]

**Dependencies:**
- [Component it depends on]

**Key considerations:**
- [Important design decision or constraint]

---

## Data Flow

### Primary User Flow

<!-- Describe the main data flow through the system -->

```
1. User [action]
   ↓
2. [Component A] receives request
   ↓
3. [Component A] validates and transforms
   ↓
4. [Component B] processes business logic
   ↓
5. [Component C] persists data
   ↓
6. Response returned to user
```

**Data transformations:**

| Step | Input | Output | Component |
|------|-------|--------|-----------|
| 1 | User request | Validated request | API Gateway |
| 2 | Validated request | Domain object | Service A |
| 3 | Domain object | Persisted entity | Database |

---

### Secondary Flow: [Name]

<!-- Additional important data flows -->

```
1. [Trigger event]
   ↓
2. [Processing steps]
   ↓
3. [Outcome]
```

---

## API Design

### API Style

**Type:** [REST / GraphQL / gRPC / WebSocket]

**Base URL:** `[/api/v1 or similar]`

**Authentication:** [JWT / Session / API Key / OAuth]

### Core Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | `/resource` | List resources | Yes |
| POST | `/resource` | Create resource | Yes |
| GET | `/resource/:id` | Get single resource | Yes |
| PUT | `/resource/:id` | Update resource | Yes |
| DELETE | `/resource/:id` | Delete resource | Yes |

### Request/Response Patterns

**Standard success response:**
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "ISO-8601"
  }
}
```

**Standard error response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }
  }
}
```

---

## State Management

### Application State

**Strategy:** [Redux / Context / Zustand / Server-side sessions]

**State locations:**

| State Type | Location | Persistence |
|------------|----------|-------------|
| User session | [Where] | [How long] |
| UI state | [Where] | [How long] |
| Cache | [Where] | [TTL] |
| Business data | [Where] | [How long] |

### Cache Strategy

**Cache layers:**
- [Layer 1 - e.g., Browser cache]
- [Layer 2 - e.g., CDN]
- [Layer 3 - e.g., Application cache]

**Invalidation strategy:** [How caches are invalidated]

---

## Security Architecture

### Authentication

**Method:** [JWT / Session / OAuth / etc.]

**Flow:**
```
1. User submits credentials
2. [Auth service] validates
3. [Token/session] issued
4. Client stores [token/session]
5. Subsequent requests include [auth header/cookie]
```

### Authorization

**Model:** [RBAC / ABAC / ACL / Custom]

**Roles/Permissions:**

| Role | Permissions |
|------|-------------|
| [Role 1] | [What they can do] |
| [Role 2] | [What they can do] |

### Data Protection

| Data Type | Protection | Storage |
|-----------|------------|---------|
| Passwords | [Hashing algorithm] | Database |
| PII | [Encryption method] | Database |
| Tokens | [How secured] | [Where] |
| API Keys | [How secured] | [Where] |

### Security Considerations

- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] SQL injection prevention (parameterized queries)
- [ ] CSRF protection
- [ ] Rate limiting
- [ ] HTTPS only

---

## Error Handling

### Error Categories

| Category | HTTP Code | Handling |
|----------|-----------|----------|
| Validation errors | 400 | Return field-specific errors |
| Authentication | 401 | Redirect to login |
| Authorization | 403 | Show access denied |
| Not found | 404 | Show not found page |
| Server errors | 500 | Log, show generic message |

### Error Propagation

```
Component Error
    ↓
Caught at boundary
    ↓
Logged with context
    ↓
Transformed to user-safe message
    ↓
Returned to client
```

---

## Scalability Considerations

### Horizontal Scaling

| Component | Scalable? | Strategy |
|-----------|-----------|----------|
| [Component 1] | Yes/No | [How] |
| [Component 2] | Yes/No | [How] |
| Database | Yes/No | [How] |

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time (p50) | [X ms] | [How measured] |
| Response time (p99) | [X ms] | [How measured] |
| Throughput | [X req/s] | [How measured] |
| Availability | [X%] | [How measured] |

---

## External Dependencies

| Dependency | Purpose | Criticality | Fallback |
|------------|---------|-------------|----------|
| [Service 1] | [What for] | Critical/Important/Nice-to-have | [What if unavailable] |
| [Service 2] | [What for] | Critical/Important/Nice-to-have | [What if unavailable] |

---

## Deployment Architecture

### Environments

| Environment | Purpose | URL |
|-------------|---------|-----|
| Development | Local dev | localhost |
| Staging | Pre-production testing | [URL] |
| Production | Live users | [URL] |

### Infrastructure

```
[Describe or diagram infrastructure]

e.g.,
- Hosting: Vercel / AWS / GCP
- Database: Managed PostgreSQL
- CDN: Cloudflare
- Monitoring: [Tool]
```

---

## Open Questions

- [ ] [Architectural question to resolve]
- [ ] [Decision to make]
- [ ] [Assumption to validate]

---

## Related Documents

- [brief.md](../../discover/templates/brief.md) - What we're building
- [data-model.md](data-model.md) - Database schema
- [stack.md](stack.md) - Technology choices
