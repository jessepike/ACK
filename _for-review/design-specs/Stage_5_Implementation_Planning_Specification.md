# Stage 5: Implementation Planning

**Stage:** 5 of 5  
**Name:** Implementation Planning  
**Purpose:** Break down solution into executable tasks with clear sequence, dependencies, and success criteria  
**Dependencies:** Stage 4 (Workflow Configuration) must be complete  
**Outputs:** 5-6 artifacts defining what to build, in what order, and how to measure success

---

## Overview

Stage 5 transforms the solution design into an actionable implementation plan. It defines every task that must be completed, establishes the order of execution, identifies required skills and agents, and creates the roadmap from empty repository to working product.

**Key Question Answered:** "What do we build, in what order, and how do we know we're done?"

**Difference from Previous Stages:**
- Stage 1-2: What and why
- Stage 3: Where and with what tools
- Stage 4: How we work together
- **Stage 5:** Specific tasks, order, and execution plan

**Critical Success Factor:** The implementation plan becomes the **contract** between human and agent. Once locked, deviations require change orders. This prevents scope creep and agent improvisation.

---

## Stage 5 Artifacts

| Artifact | Purpose | Type | Lifecycle |
|----------|---------|------|-----------|
| **phases.md** | Implementation phases breakdown | Markdown | Locked |
| **tasks.md** | Detailed task specifications | Markdown | Locked |
| **dependencies.md** | Task dependencies and critical path | Markdown | Locked |
| **effort-estimates.md** | Time/complexity estimates | Markdown | Locked |
| **skills-and-agents.md** | Required skills and sub-agents | Markdown | Locked |
| **implementation-synthesis.md** | Stage summary (optional) | Markdown | Finalized |

**Locked artifacts:** Changes require change order (CO-XXX) with human approval  
**Generated artifacts:** tasks.json (auto-generated from tasks.md, git-ignored)

---

## Two-Pass Planning Approach

**Stage 5 uses a two-pass approach to ensure completeness:**

### Pass 1: Core Implementation Plan

**Artifacts created:**
1. phases.md - High-level phase breakdown
2. tasks.md - All tasks with acceptance criteria
3. dependencies.md - Task ordering and critical path
4. effort-estimates.md - Complexity and time estimates

**Focus:** WHAT needs to be built and in WHAT ORDER

**Agent role:** Break down solution into granular, testable tasks

**Validation criteria:**
- Every feature from solution design has corresponding tasks
- Each task has clear acceptance criteria
- Dependencies are logical and complete
- Estimates are realistic

### Pass 2: Execution Support

**Artifacts created:**
5. skills-and-agents.md - Skills/agents needed for tasks

**Focus:** HOW tasks will be executed (tooling, automation, delegation)

**Agent role:** Identify which tasks need specialized skills or sub-agents

**Validation criteria:**
- Skills exist or can be created
- Sub-agents have clear responsibilities
- Handoff protocols defined
- No task lacks execution strategy

**Why two passes?**
- Can't know what skills needed until tasks are defined
- Prevents premature optimization of execution
- Allows human review of plan before committing to tooling
- Separates "what to build" from "how to build it"

---

## Artifact 1: phases.md

**Purpose:** Break implementation into logical phases with milestones  
**Location:** `.ipe/implementation/phases.md`  
**Lifecycle:** Locked (changes require change order)

### Template: phases.md

```markdown
---
artifact: phases.md
status: locked
stage: implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
version: 1.0.0
locked-date: YYYY-MM-DD
related: [tasks.md, dependencies.md]
---

# Implementation Phases

## Purpose

Defines the sequence of implementation phases, each with specific goals,
deliverables, and milestones. Provides the high-level roadmap for building
the solution.

---

## Phase Structure

Each phase includes:
- **Goal:** What this phase achieves
- **Deliverables:** Concrete outputs
- **Milestone:** Success criteria for phase completion
- **Tasks:** Reference to tasks in tasks.md
- **Dependencies:** What must be done first
- **Estimated Duration:** Time to complete

---

## Phase 1: MVP Foundation

**Goal:** Establish basic application structure and core infrastructure

**Duration:** 2-3 weeks  
**Milestone:** M1 - Application Runs Locally

**Deliverables:**
- Basic application entry point
- Database connection established
- Core API structure in place
- Health check endpoint functional
- Development environment working

**Key Tasks:**
- TASK-001: Setup application structure
- TASK-002: Configure database connection
- TASK-003: Create basic API routes
- TASK-004: Implement health check
- TASK-005: Setup development workflow

**Success Criteria:**
- Application starts without errors
- Database connections successful
- GET /health returns 200 OK
- Can create and run tests
- Development workflow documented

**Dependencies:**
- Stage 3 (Environment Setup) complete
- Stage 4 (Workflow Config) complete
- No implementation dependencies (first phase)

---

## Phase 2: Core Features

**Goal:** Implement primary user-facing features

**Duration:** 4-6 weeks  
**Milestone:** M2 - Core Functionality Working

**Deliverables:**
- User authentication system
- Primary data models
- CRUD operations for main entities
- API endpoints for core features
- Basic error handling

**Key Tasks:**
- TASK-006: User authentication
- TASK-007: User model and database schema
- TASK-008: Authentication middleware
- TASK-009: Project data model
- TASK-010: Project CRUD operations
- TASK-011: API endpoints for projects
- TASK-012: Input validation
- TASK-013: Error handling middleware

**Success Criteria:**
- Users can register and login
- CRUD operations work for all entities
- API responds correctly to valid/invalid input
- Errors return meaningful messages
- All core features have test coverage

**Dependencies:**
- Phase 1 (MVP Foundation) complete
- TASK-001 through TASK-005 done

---

## Phase 3: Integration & Polish

**Goal:** Integrate components, add quality-of-life features, prepare for deployment

**Duration:** 2-3 weeks  
**Milestone:** M3 - Production Ready

**Deliverables:**
- Component integration complete
- Logging and monitoring
- API documentation
- Deployment configuration
- Production environment setup

**Key Tasks:**
- TASK-014: Integrate authentication with all endpoints
- TASK-015: Add comprehensive logging
- TASK-016: Setup monitoring and alerts
- TASK-017: Generate API documentation
- TASK-018: Configure production deployment
- TASK-019: Load testing and optimization
- TASK-020: Security hardening

**Success Criteria:**
- All features work together seamlessly
- Logs provide debugging information
- Monitoring catches errors
- API documentation complete
- Deployment automated
- Security audit passed

**Dependencies:**
- Phase 2 (Core Features) complete
- TASK-001 through TASK-013 done

---

## Phase Transition Criteria

### Phase 1 → Phase 2

**Required:**
- All Phase 1 tasks marked complete
- Milestone M1 achieved (application runs)
- Tests passing for foundation
- Code reviewed and merged to main

**Validation:**
```bash
# Application starts successfully
python src/main.py

# Health check responds
curl http://localhost:8000/health

# Tests pass
pytest tests/test_foundation.py
```

### Phase 2 → Phase 3

**Required:**
- All Phase 2 tasks marked complete
- Milestone M2 achieved (core features working)
- Test coverage >80% for core features
- Security review complete

**Validation:**
```bash
# All API endpoints respond correctly
pytest tests/test_api.py

# CRUD operations work
pytest tests/test_crud.py

# Authentication works
pytest tests/test_auth.py
```

### Phase 3 → Complete

**Required:**
- All Phase 3 tasks marked complete
- Milestone M3 achieved (production ready)
- Deployment successful to staging
- Documentation complete

**Validation:**
```bash
# Production deployment works
./scripts/deploy-production.sh --dry-run

# API documentation generated
ls docs/api.html

# All tests pass
pytest
```

---

## Phase Dependencies Visualization

```
Phase 1: MVP Foundation
    ↓
    │ (M1: Application Runs)
    ↓
Phase 2: Core Features
    ↓
    │ (M2: Core Functionality Working)
    ↓
Phase 3: Integration & Polish
    ↓
    │ (M3: Production Ready)
    ↓
✅ Implementation Complete
```

---

## Risk Management

### Phase 1 Risks

**Risk:** Database connection issues  
**Mitigation:** Use proven database library, test early  
**Contingency:** Fall back to SQLite for development

**Risk:** Environment setup complexity  
**Mitigation:** Document every step, automate with scripts  
**Contingency:** Provide Docker alternative

### Phase 2 Risks

**Risk:** Authentication implementation complexity  
**Mitigation:** Use established library (e.g., FastAPI OAuth)  
**Contingency:** Simplify to basic auth for MVP

**Risk:** Data model changes during development  
**Mitigation:** Use migrations, version all schema changes  
**Contingency:** Rollback mechanism in place

### Phase 3 Risks

**Risk:** Performance issues at scale  
**Mitigation:** Load testing before production  
**Contingency:** Caching layer, database optimization

**Risk:** Deployment failures  
**Mitigation:** Staging environment, rollback plan  
**Contingency:** Manual deployment if automation fails

---

## Notes

**Phase timing is estimated based on:**
- Solo developer working full-time
- Python/FastAPI stack (known technologies)
- No major technical unknowns
- Standard CRUD application complexity

**Adjust estimates for:**
- Part-time development
- Unfamiliar tech stack
- Complex domain logic
- External dependencies

---

## Version History

**1.0.0** - Initial implementation plan
- 3 phases defined (Foundation → Core → Polish)
- ~20 tasks across all phases
- 8-12 week total timeline
```

---

## Artifact 2: tasks.md

**Purpose:** Detailed specification for every implementation task  
**Location:** `.ipe/implementation/tasks.md`  
**Lifecycle:** Locked (changes require change order)

**CRITICAL:** This is the **source of truth** for implementation. Once locked, agents must follow exactly as specified or request change order.

### Template: tasks.md

```markdown
---
artifact: tasks.md
status: locked
stage: implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
version: 1.0.0
locked-date: YYYY-MM-DD
change-orders: []
related: [phases.md, dependencies.md]
---

# Implementation Tasks

## Purpose

Detailed specification for every task required to implement the solution.
Each task includes acceptance criteria, context, dependencies, and completion
tracking.

**Status:** LOCKED - Changes require change order (CO-XXX)

---

## Task Format

Each task includes:
- **Title:** Brief description
- **Phase:** Which implementation phase
- **Milestone:** Associated milestone
- **Status:** Not Started | In Progress | Blocked | Complete
- **Complexity:** Simple | Medium | Complex | Very Complex
- **Domain:** Category tags (backend, frontend, database, etc.)
- **Dependencies:** Other tasks that must complete first
- **Assigned:** Which agent (MainAgent, TestingAgent, etc.)
- **Skills Required:** Special skills needed
- **Context:** Links to relevant artifacts
- **Description:** What needs to be done
- **Acceptance Criteria:** How to verify completion
- **Completed:** Metadata when done

---

## Phase 1: MVP Foundation

### TASK-001: Setup FastAPI Application Structure

**Phase:** MVP - Foundation  
**Milestone:** M1 - Application Runs Locally  
**Status:** Not Started  
**Complexity:** Medium  
**Domain:** backend, api, infrastructure  
**Dependencies:** None  
**Assigned:** MainAgent  
**Skills Required:** None  
**Context:** 
- [Repository Structure](../environment-setup/repo-structure.md)
- [Technology Stack](../solution-design/stack.md)

**Description:**

Create the basic FastAPI application structure following the repository
layout defined in Stage 3. Implement the application entry point, basic
configuration management, and a health check endpoint to verify the
application can start and respond to requests.

**Acceptance Criteria:**

- [ ] `src/main.py` exists with FastAPI app instance
- [ ] Application imports and initializes without errors
- [ ] Health check endpoint at `/health` returns 200 OK
- [ ] Health check response includes: `{"status": "healthy", "timestamp": <ISO8601>}`
- [ ] Application can be started with: `uvicorn src.main:app --reload`
- [ ] Basic logging configured and working
- [ ] Environment variable loading working (from .env)
- [ ] Application version included in health check response

**Files to Create:**
```
src/main.py              # Application entry point
src/config.py            # Configuration management
src/api/__init__.py      # API module
src/api/health.py        # Health check endpoint
tests/test_health.py     # Health check tests
```

**Example Health Check Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-01-02T10:30:00Z",
  "environment": "development"
}
```

**Testing:**
```bash
# Application starts
uvicorn src.main:app --reload

# Health check works
curl http://localhost:8000/health

# Tests pass
pytest tests/test_health.py -v
```

**Completed:**
- Date: 
- Commit: 
- Notes: 

---

### TASK-002: Configure Database Connection

**Phase:** MVP - Foundation  
**Milestone:** M1 - Application Runs Locally  
**Status:** Not Started  
**Complexity:** Medium  
**Domain:** backend, database, infrastructure  
**Dependencies:** TASK-001  
**Assigned:** MainAgent  
**Skills Required:** None  
**Context:**
- [Database Schema](../solution-design/data-model.md)
- [Environment Configuration](../workflow-config/environment-variants.md)

**Description:**

Establish PostgreSQL database connection using SQLAlchemy. Implement
connection pooling, health checks, and proper error handling. Support
both local development (Docker PostgreSQL) and managed database (production).

**Acceptance Criteria:**

- [ ] SQLAlchemy engine configured with proper pool settings
- [ ] Database connection tested at application startup
- [ ] Connection health check endpoint at `/health/db`
- [ ] Graceful handling of database unavailability
- [ ] Connection pooling configured (min: 5, max: 20 for dev)
- [ ] Database migrations framework (Alembic) initialized
- [ ] Initial migration creates database structure
- [ ] Connection string loaded from environment variable

**Files to Create:**
```
src/database.py          # Database connection and session
src/models/__init__.py   # Models module
alembic.ini              # Alembic configuration
alembic/env.py           # Alembic environment
alembic/versions/        # Migration versions directory
tests/test_database.py   # Database connection tests
```

**Environment Variables:**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev
```

**Testing:**
```bash
# Database connection works
pytest tests/test_database.py

# Health check shows database status
curl http://localhost:8000/health/db

# Migrations run successfully
alembic upgrade head
```

**Completed:**
- Date:
- Commit:
- Notes:

---

### TASK-003: Create Basic API Structure

**Phase:** MVP - Foundation  
**Milestone:** M1 - Application Runs Locally  
**Status:** Not Started  
**Complexity:** Simple  
**Domain:** backend, api  
**Dependencies:** TASK-001  
**Assigned:** MainAgent  
**Skills Required:** None  
**Context:**
- [API Design](../solution-design/architecture.md)
- [Development Workflow](../workflow-config/dev-workflow.md)

**Description:**

Establish the basic API routing structure following RESTful conventions.
Create the router hierarchy for v1 API endpoints, implement CORS middleware,
and set up request/response logging.

**Acceptance Criteria:**

- [ ] API router structure created under `src/api/`
- [ ] v1 API router at `/api/v1/` prefix
- [ ] CORS middleware configured (dev: allow all, prod: restricted)
- [ ] Request logging middleware in place
- [ ] Response time logging implemented
- [ ] API root endpoint at `/` returns API info
- [ ] OpenAPI documentation auto-generated at `/docs`
- [ ] ReDoc documentation at `/redoc`

**Files to Create:**
```
src/api/v1/__init__.py   # v1 API router
src/middleware/          # Middleware module
src/middleware/cors.py   # CORS configuration
src/middleware/logging.py # Request logging
tests/test_api.py        # API structure tests
```

**API Root Response:**
```json
{
  "name": "My Application API",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

**Testing:**
```bash
# API root responds
curl http://localhost:8000/

# OpenAPI docs accessible
curl http://localhost:8000/docs

# CORS headers present
curl -H "Origin: http://localhost:3000" http://localhost:8000/
```

**Completed:**
- Date:
- Commit:
- Notes:

---

## Phase 2: Core Features

### TASK-006: Implement User Authentication

**Phase:** Core Features  
**Milestone:** M2 - Core Functionality Working  
**Status:** Not Started  
**Complexity:** Complex  
**Domain:** backend, security, authentication  
**Dependencies:** TASK-002 (Database), TASK-003 (API Structure)  
**Assigned:** MainAgent  
**Skills Required:** None (standard library usage)  
**Context:**
- [Security Requirements](../solution-design/architecture.md#security)
- [User Model](../solution-design/data-model.md#user-model)

**Description:**

Implement JWT-based user authentication system with registration, login,
and token refresh capabilities. Use bcrypt for password hashing, implement
token expiration, and provide middleware for protecting endpoints.

**Acceptance Criteria:**

- [ ] User registration endpoint: POST `/api/v1/auth/register`
- [ ] User login endpoint: POST `/api/v1/auth/login`
- [ ] Token refresh endpoint: POST `/api/v1/auth/refresh`
- [ ] Passwords hashed with bcrypt (cost factor: 12)
- [ ] JWT tokens include: user_id, email, exp, iat
- [ ] Access tokens expire after 15 minutes
- [ ] Refresh tokens expire after 7 days
- [ ] Authentication middleware validates JWT tokens
- [ ] Protected endpoints return 401 for invalid/missing tokens
- [ ] Registration validates email format and password strength
- [ ] Duplicate email registration returns 409 Conflict

**Files to Create:**
```
src/api/v1/auth.py       # Authentication routes
src/services/auth.py     # Authentication business logic
src/models/user.py       # User database model
src/middleware/auth.py   # JWT validation middleware
src/utils/jwt.py         # JWT token utilities
src/utils/password.py    # Password hashing utilities
tests/test_auth.py       # Authentication tests
tests/test_auth_middleware.py # Middleware tests
```

**API Contracts:**

```python
# POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
# Response: 201 Created
{
  "user_id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe"
}

# POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
# Response: 200 OK
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 900
}
```

**Testing:**
```bash
# Registration works
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!","name":"Test User"}'

# Login returns tokens
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!"}'

# Protected endpoint requires auth
curl http://localhost:8000/api/v1/protected
# Returns 401 without token

# Protected endpoint works with token
curl http://localhost:8000/api/v1/protected \
  -H "Authorization: Bearer eyJ..."
# Returns 200 OK

# Tests pass
pytest tests/test_auth.py -v
```

**Security Considerations:**
- Never log passwords or tokens
- Use secure random for token generation
- Implement rate limiting on auth endpoints
- Store only hashed passwords
- Invalidate refresh tokens on password change

**Completed:**
- Date:
- Commit:
- Notes:

---

## Task Status Summary

**Not Started:** TASK-001, TASK-002, TASK-003, TASK-006, ...  
**In Progress:** None  
**Blocked:** None  
**Complete:** None

**Total Tasks:** 20  
**Progress:** 0/20 (0%)

---

## Deviation Protocol

**If a task cannot be completed as specified:**

1. **STOP immediately** - Do not improvise
2. **Document the blocker** in task comments:
   ```markdown
   <!-- DEVIATION: TASK-XXX
   Date: YYYY-MM-DD
   Issue: [what failed]
   Attempted: [what was tried]
   Needs: [human decision required]
   Proposed: [alternative approach if any]
   -->
   ```
3. **Alert human** via system message
4. **Wait for decision** - Change order or proceed differently
5. **DO NOT** skip to next task or create workarounds

**For minor deviations (tool swap, different library):**
- Quick review process in task comments
- Human approves inline
- Logged but no version bump

**For major deviations (scope change, different approach):**
- Formal change order required (CO-XXX)
- Version bump to tasks.md
- All affected tasks updated

---

## Change Order Format

```markdown
## Change Order: CO-001

**Date:** YYYY-MM-DD  
**Requestor:** Claude / Human  
**Affected Tasks:** TASK-XXX, TASK-YYY

**Reason:**
Tool X is incompatible with Python 3.12

**Proposed Change:**
Replace Tool X with Tool Y (functionally equivalent)

**Impact:**
- TASK-XXX: Update acceptance criteria to use Tool Y
- No scope change
- No timeline impact

**Status:** Approved by [Human] on YYYY-MM-DD

**Implementation:**
- Updated TASK-XXX acceptance criteria
- Version bump: 1.0.0 → 1.1.0
```

---

## Notes

**Task numbering:**
- Sequential across all phases
- No gaps in numbering
- Prefix with TASK-

**Acceptance criteria:**
- Specific and testable
- Include commands to verify
- Cover happy path and edge cases

**Dependencies:**
- Must be explicit
- No circular dependencies
- Validated in dependencies.md

---

## Version History

**1.0.0** - Initial task breakdown
- 20 tasks defined
- 3 phases (Foundation, Core, Polish)
- All acceptance criteria specified
```

---

## Artifact 3: dependencies.md

**Purpose:** Task dependency graph and critical path analysis  
**Location:** `.ipe/implementation/dependencies.md`  
**Lifecycle:** Locked

### Template: dependencies.md

```markdown
---
artifact: dependencies.md
status: locked
stage: implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
version: 1.0.0
locked-date: YYYY-MM-DD
related: [tasks.md, phases.md]
---

# Task Dependencies

## Purpose

Defines dependencies between implementation tasks, identifies the critical
path, and highlights tasks that can be parallelized. Ensures tasks are
executed in the correct order.

---

## Dependency Graph

```
Phase 1: MVP Foundation
┌─────────────┐
│  TASK-001   │ (No dependencies)
│   Setup     │
│ Application │
└──────┬──────┘
       ├─────────────┬─────────────┐
       ↓             ↓             ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│TASK-002  │  │TASK-003  │  │TASK-004  │
│ Database │  │   API    │  │  Health  │
│Connection│  │Structure │  │  Check   │
└─────┬────┘  └─────┬────┘  └──────────┘
      │             │
      └──────┬──────┘
             ↓
      ┌──────────┐
      │TASK-005  │
      │   Dev    │
      │Workflow  │
      └──────────┘

Phase 2: Core Features
       │
       ↓
┌──────────┐
│TASK-006  │ (Depends: TASK-002, TASK-003)
│   User   │
│   Auth   │
└─────┬────┘
      ├─────────────┬─────────────┐
      ↓             ↓             ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│TASK-007  │  │TASK-009  │  │TASK-012  │
│   User   │  │ Project  │  │  Input   │
│  Model   │  │  Model   │  │Validation│
└─────┬────┘  └─────┬────┘  └──────────┘
      ↓             ↓
┌──────────┐  ┌──────────┐
│TASK-008  │  │TASK-010  │
│   Auth   │  │ Project  │
│Middleware│  │   CRUD   │
└──────────┘  └─────┬────┘
                    ↓
             ┌──────────┐
             │TASK-011  │
             │ Project  │
             │   API    │
             └──────────┘

Phase 3: Integration & Polish
       │
       ↓
(All Phase 2 tasks)
       │
       ├──────────┬──────────┬──────────┐
       ↓          ↓          ↓          ↓
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│TASK-014  ││TASK-015  ││TASK-017  ││TASK-018  │
│Integration││ Logging ││   API   ││Deployment│
└──────────┘└──────────┘│   Docs  │└──────────┘
                        └──────────┘
                             ↓
                      ┌──────────┐
                      │TASK-019  │
                      │   Load   │
                      │  Testing │
                      └─────┬────┘
                            ↓
                      ┌──────────┐
                      │TASK-020  │
                      │ Security │
                      │Hardening │
                      └──────────┘
```

---

## Dependency Matrix

| Task | Depends On | Enables | Can Parallelize |
|------|------------|---------|-----------------|
| TASK-001 | None | ALL | - |
| TASK-002 | TASK-001 | TASK-006, TASK-007, TASK-009 | TASK-003, TASK-004 |
| TASK-003 | TASK-001 | TASK-006, TASK-011 | TASK-002, TASK-004 |
| TASK-004 | TASK-001 | - | TASK-002, TASK-003 |
| TASK-005 | TASK-001 | - | TASK-002, TASK-003, TASK-004 |
| TASK-006 | TASK-002, TASK-003 | TASK-007, TASK-008 | - |
| TASK-007 | TASK-006 | TASK-008 | TASK-009 |
| TASK-008 | TASK-007 | TASK-014 | TASK-009, TASK-010 |
| TASK-009 | TASK-002 | TASK-010 | TASK-006, TASK-007 |
| TASK-010 | TASK-009 | TASK-011 | TASK-006, TASK-007, TASK-008 |
| TASK-011 | TASK-010, TASK-003 | TASK-014 | TASK-008, TASK-012 |
| TASK-012 | TASK-003 | - | All Phase 2 |
| TASK-014 | All Phase 2 | TASK-019 | TASK-015, TASK-017 |
| TASK-015 | TASK-014 | TASK-016 | TASK-017, TASK-018 |
| TASK-016 | TASK-015 | - | TASK-017, TASK-018, TASK-019 |
| TASK-017 | All API tasks | - | TASK-015, TASK-018, TASK-019 |
| TASK-018 | TASK-014 | TASK-019 | TASK-015, TASK-017 |
| TASK-019 | TASK-014, TASK-018 | TASK-020 | TASK-015, TASK-017 |
| TASK-020 | TASK-019 | - | - |

---

## Critical Path

**Definition:** Longest sequence of dependent tasks; determines minimum project duration

**Critical Path:**
```
TASK-001 → TASK-002 → TASK-006 → TASK-007 → TASK-008 →
TASK-014 → TASK-019 → TASK-020
```

**Duration:** 8 tasks × average complexity = ~6-8 weeks

**Implications:**
- These tasks cannot be parallelized
- Delays here impact overall timeline
- Should be prioritized for agent attention
- Watch for blockers on critical path tasks

---

## Parallelization Opportunities

### Phase 1 Parallel Tracks

**After TASK-001 completes:**

**Track A (Database):**
- TASK-002 (Database Connection)

**Track B (API):**
- TASK-003 (API Structure)
- TASK-004 (Health Check)

**Track C (Workflow):**
- TASK-005 (Dev Workflow)

**Parallel Duration:** ~3-5 days (instead of 9-15 sequential)

### Phase 2 Parallel Tracks

**After TASK-006 completes:**

**Track A (User Flow):**
- TASK-007 → TASK-008

**Track B (Project Flow):**
- TASK-009 → TASK-010 → TASK-011

**Track C (Validation):**
- TASK-012

**Parallel Duration:** ~10-12 days (instead of 18-21 sequential)

---

## Dependency Rules

### Hard Dependencies

**Must complete before:**
- Database tasks before any data model tasks
- Data models before CRUD operations
- CRUD before API endpoints
- API endpoints before integration

**Reasoning:** Technical impossibility to proceed without

### Soft Dependencies

**Should complete before (but not blocking):**
- Documentation before deployment
- Logging before production
- Tests before code review

**Reasoning:** Quality/workflow reasons, not technical blocks

### Cross-Phase Dependencies

**Phase 1 → Phase 2:**
- ALL Phase 1 tasks must complete
- Milestone M1 achieved

**Phase 2 → Phase 3:**
- ALL Phase 2 tasks must complete
- Milestone M2 achieved

**No task from later phase can start before earlier phase complete**

---

## Blocker Management

### Identifying Blockers

**A task is blocked when:**
- Dependency task not started
- Dependency task failed
- External dependency unavailable
- Waiting for human decision

**Mark in tasks.md:**
```markdown
Status: 🚫 Blocked
<!-- BLOCKED: Waiting for TASK-XXX completion -->
```

### Unblocking Strategy

**When blocked:**
1. Document blocker clearly
2. Alert human if blocker is external
3. Switch to non-dependent task
4. Update dependency graph if needed

**DO NOT:**
- Skip blocked task and continue
- Implement workarounds without approval
- Change dependencies without change order

---

## Dependency Validation

### Pre-Implementation Checks

**Before starting task:**
```bash
# Check dependencies complete
grep "^### TASK-XXX" .ipe/implementation/tasks.md -A 3 | \
  grep "Status: ✅ Complete"

# If not complete → BLOCKED
```

### Circular Dependency Detection

**No task can depend on itself transitively:**
```
TASK-A depends on TASK-B
TASK-B depends on TASK-C
TASK-C depends on TASK-A
# INVALID - circular dependency
```

**Validation:** Build dependency graph, check for cycles

### Missing Dependency Detection

**All referenced tasks must exist:**
```
TASK-006 depends on TASK-002, TASK-003
# Both TASK-002 and TASK-003 must exist in tasks.md
```

---

## Notes

**Dependency changes:**
- Require change order if locked
- Must update dependency graph
- Validate no circular dependencies introduced
- Check critical path impact

**Parallelization:**
- Human can work one track
- Agent can work another track
- Coordinate in tasks.md status updates

---

## Version History

**1.0.0** - Initial dependency graph
- 20 tasks with dependencies
- Critical path identified (8 tasks)
- Parallelization opportunities documented
```

---

## Artifact 4: effort-estimates.md

**Purpose:** Complexity and time estimates for resource planning  
**Location:** `.ipe/implementation/effort-estimates.md`  
**Lifecycle:** Locked

### Template: effort-estimates.md

```markdown
---
artifact: effort-estimates.md
status: locked
stage: implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
version: 1.0.0
locked-date: YYYY-MM-DD
related: [tasks.md, phases.md]
---

# Effort Estimates

## Purpose

Provides complexity ratings and time estimates for all implementation tasks.
Helps plan resources, set expectations, and track progress against plan.

**Estimation Method:** Story points + time ranges based on complexity

---

## Complexity Scale

| Complexity | Story Points | Time Range | Description |
|------------|--------------|------------|-------------|
| **Simple** | 1-2 | 2-4 hours | Straightforward, well-defined, no unknowns |
| **Medium** | 3-5 | 4-8 hours | Some complexity, may need research |
| **Complex** | 8-13 | 1-2 days | Significant complexity, multiple components |
| **Very Complex** | 21+ | 3-5 days | High complexity, many unknowns, R&D needed |

---

## Task Estimates

### Phase 1: MVP Foundation

| Task | Title | Complexity | Points | Estimate | Rationale |
|------|-------|------------|--------|----------|-----------|
| TASK-001 | Setup Application | Medium | 5 | 6-8h | Standard FastAPI setup, some config |
| TASK-002 | Database Connection | Medium | 5 | 6-8h | SQLAlchemy setup, migrations init |
| TASK-003 | API Structure | Simple | 2 | 3-4h | Router setup, middleware config |
| TASK-004 | Health Check | Simple | 1 | 2-3h | Single endpoint, simple logic |
| TASK-005 | Dev Workflow | Medium | 3 | 4-6h | Documentation, scripts, validation |

**Phase 1 Total:** 16 points, 21-29 hours (~3-4 days)

### Phase 2: Core Features

| Task | Title | Complexity | Points | Estimate | Rationale |
|------|-------|------------|--------|----------|-----------|
| TASK-006 | User Authentication | Complex | 13 | 12-16h | JWT, bcrypt, middleware, tests |
| TASK-007 | User Model | Medium | 5 | 6-8h | SQLAlchemy model, migrations |
| TASK-008 | Auth Middleware | Medium | 5 | 6-8h | JWT validation, error handling |
| TASK-009 | Project Model | Medium | 5 | 6-8h | Data model, relationships |
| TASK-010 | Project CRUD | Complex | 8 | 8-12h | All CRUD ops, validation, tests |
| TASK-011 | Project API | Complex | 8 | 8-12h | REST endpoints, serialization |
| TASK-012 | Input Validation | Medium | 5 | 6-8h | Pydantic schemas, error messages |
| TASK-013 | Error Handling | Medium | 3 | 4-6h | Custom exceptions, middleware |

**Phase 2 Total:** 52 points, 56-78 hours (~7-10 days)

### Phase 3: Integration & Polish

| Task | Title | Complexity | Points | Estimate | Rationale |
|------|-------|------------|--------|----------|-----------|
| TASK-014 | Integration | Complex | 8 | 8-12h | Connect all components, test |
| TASK-015 | Logging | Medium | 5 | 6-8h | Structured logging, log levels |
| TASK-016 | Monitoring | Complex | 13 | 12-16h | Metrics, alerts, dashboards |
| TASK-017 | API Docs | Simple | 2 | 3-4h | OpenAPI generation, examples |
| TASK-018 | Deployment | Complex | 13 | 12-16h | CI/CD, production config |
| TASK-019 | Load Testing | Complex | 8 | 8-12h | Test scenarios, optimization |
| TASK-020 | Security Hardening | Complex | 13 | 12-16h | Audit, fixes, validation |

**Phase 3 Total:** 62 points, 61-84 hours (~8-11 days)

---

## Overall Estimates

**Total Story Points:** 130  
**Total Effort:** 138-191 hours  
**Working Days:** 18-24 days (at 8 hours/day)  
**Calendar Time:** 4-6 weeks (accounting for context switches, meetings)

**By Phase:**
- Phase 1: 3-4 days (16 points)
- Phase 2: 7-10 days (52 points)
- Phase 3: 8-11 days (62 points)

---

## Velocity Assumptions

**Estimates assume:**
- Solo developer, full-time focus
- Familiar with tech stack (Python, FastAPI, PostgreSQL)
- No major technical unknowns
- Minimal external blockers
- Standard code review process
- ~80% productive time (20% for meetings, interruptions)

**Adjust for:**
- Part-time work: Double calendar time
- Unfamiliar stack: Add 30-50% to estimates
- Complex domain: Add 20-30% to complex tasks
- High code quality bar: Add 20% for extra testing/review

---

## Risk Factors

### High-Risk Tasks (May Exceed Estimate)

**TASK-006 (User Authentication):**
- Risk: Security requirements may expand
- Mitigation: Use proven libraries, follow OWASP guidelines
- Contingency: +50% time buffer

**TASK-016 (Monitoring):**
- Risk: Metrics requirements may be unclear
- Mitigation: Define metrics early, get approval
- Contingency: +30% time buffer

**TASK-018 (Deployment):**
- Risk: Infrastructure issues, unfamiliar platform
- Mitigation: Test in staging early and often
- Contingency: +40% time buffer

### Low-Risk Tasks (Likely Under Estimate)

**TASK-004 (Health Check):**
- Simple, well-defined
- May complete in 1-2 hours

**TASK-017 (API Docs):**
- FastAPI auto-generates most docs
- May complete in 2-3 hours

---

## Progress Tracking

### Burndown Metrics

**Track daily:**
- Story points completed
- Hours spent vs estimated
- Velocity (points per day)

**Update weekly:**
- Remaining points
- Projected completion date
- Estimate adjustments

**Example tracking:**
```
Day 1-5 (Phase 1):
Completed: TASK-001 (5pts, 7h), TASK-002 (5pts, 9h)
Progress: 10/16 pts (62.5%)
Velocity: 2 pts/day
Remaining Phase 1: 6 pts, ~3 days
```

### Estimate Refinement

**After completing task:**
- Compare actual vs estimate
- Document variance
- Adjust future similar tasks

**Example:**
```
TASK-001:
Estimated: 6-8h
Actual: 7h
Variance: On target
Note: Setup took expected time, config slightly longer
```

---

## Resource Planning

### Full-Time Solo Developer

**Phase 1:** Week 1  
**Phase 2:** Weeks 2-3  
**Phase 3:** Weeks 4-5  
**Buffer:** Week 6

**Total:** 6 weeks to completion

### Part-Time (20h/week)

**Phase 1:** Weeks 1-2  
**Phase 2:** Weeks 3-6  
**Phase 3:** Weeks 7-10  
**Buffer:** Weeks 11-12

**Total:** 12 weeks to completion

### Team (2 developers)

**Phase 1:** 2-3 days (parallel tracks)  
**Phase 2:** 4-5 days (parallel tracks)  
**Phase 3:** 4-5 days (parallel + serial)  
**Buffer:** 2-3 days

**Total:** 3-4 weeks to completion

---

## Notes

**Story points:**
- Fibonacci scale (1, 2, 3, 5, 8, 13, 21)
- Relative sizing within project
- Not directly convertible to hours (use ranges)

**Time estimates:**
- Include coding, testing, documentation
- Include code review time
- Do NOT include meetings, planning
- Based on focused work time

**Velocity:**
- Measure actual vs estimated regularly
- Adjust projections based on velocity
- Account for task switching overhead

---

## Version History

**1.0.0** - Initial estimates
- 130 total story points
- 18-24 day estimate (solo, full-time)
- Risk factors identified
```

---

## Artifact 5: skills-and-agents.md

**Purpose:** Define required skills and sub-agents for task execution  
**Location:** `.ipe/implementation/skills-and-agents.md`  
**Lifecycle:** Locked

**Created in Pass 2** after tasks are defined

### Template: skills-and-agents.md

```markdown
---
artifact: skills-and-agents.md
status: locked
stage: implementation
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
version: 1.0.0
locked-date: YYYY-MM-DD
related: [tasks.md, phases.md]
---

# Skills and Sub-Agents

## Purpose

Defines specialized skills and sub-agents needed to execute implementation
tasks efficiently. Created in Pass 2 after core implementation plan is
established.

**Pass 2 Artifact:** Created after tasks.md is complete

---

## Skills Overview

**Skills extend agent capabilities for specific task types.**

Skills needed for this implementation:
1. **API Testing Skill** - Automated endpoint testing
2. **Database Migration Skill** - Schema versioning and migrations
3. **Documentation Generation Skill** - API docs from code

**Note:** No custom skills required for MVP - using standard tools/libraries

---

## Skill Definitions

### Skill 1: API Testing (Standard Tool)

**Purpose:** Automate API endpoint testing with pytest

**Tasks Using:**
- TASK-001 (Health check tests)
- TASK-003 (API structure tests)
- TASK-006 (Authentication tests)
- TASK-010 (CRUD operation tests)
- TASK-011 (API endpoint tests)

**Tool:** pytest + httpx  
**Location:** Standard Python testing  
**Configuration:** pytest.ini, conftest.py

**Example Usage:**
```python
# tests/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

**Requirements:**
- pytest installed
- Test fixtures configured
- Async client setup

**Status:** Available (standard tool)

---

### Skill 2: Database Migrations (Standard Tool)

**Purpose:** Manage database schema versions with Alembic

**Tasks Using:**
- TASK-002 (Initial database setup)
- TASK-007 (User model migration)
- TASK-009 (Project model migration)

**Tool:** Alembic  
**Location:** alembic/ directory  
**Configuration:** alembic.ini

**Example Usage:**
```bash
# Create new migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1
```

**Requirements:**
- Alembic installed
- Database connection configured
- Models defined before migration

**Status:** Available (standard tool)

---

### Skill 3: Documentation Generation (Standard Tool)

**Purpose:** Auto-generate API documentation from code

**Tasks Using:**
- TASK-017 (API documentation)

**Tool:** FastAPI built-in (OpenAPI/Swagger)  
**Location:** Auto-generated at /docs  
**Configuration:** FastAPI app metadata

**Example Usage:**
```python
# Automatic via FastAPI
app = FastAPI(
    title="My API",
    description="API Documentation",
    version="1.0.0"
)

@app.get("/users", summary="List users")
async def list_users():
    \"\"\"
    Retrieve a list of all users.
    
    Returns:
        List of user objects
    \"\"\"
    return []
```

**Requirements:**
- FastAPI app configured
- Endpoint docstrings written
- Response models defined

**Status:** Available (built-in)

---

## Sub-Agents

**Sub-agents handle specialized workflows and complex multi-step tasks.**

**For this implementation:** No sub-agents required for MVP

**Rationale:**
- All tasks completable by MainAgent
- No complex multi-step workflows requiring delegation
- No specialized domain knowledge needed

**Future consideration:**
- TestingAgent (if test suite becomes very complex)
- DocumentationAgent (if docs require significant writing)
- DeploymentAgent (if deployment becomes multi-step)

---

## Skill Selection Rationale

### Why Standard Tools Only?

**For MVP implementation:**
- Standard Python/FastAPI ecosystem well-supported
- No novel or unique requirements
- Faster development with proven tools
- Lower complexity, easier maintenance

**Custom skills considered but rejected:**
- **Custom auth skill:** Standard FastAPI OAuth sufficient
- **Custom API client generator:** OpenAPI standard works
- **Custom test framework:** pytest + httpx handles all cases

### When to Create Custom Skills

**Create custom skill when:**
- Task repeated across many projects
- Significant boilerplate reduction possible
- Domain-specific logic needed
- Integration with proprietary systems

**Examples (not needed for this project):**
- Salesforce integration skill
- Custom report generation skill
- Proprietary data format parser

---

## Skill Registry Integration

**Global skills registry location:** `~/.ipe/skills/`

**For this project:**
```bash
~/.ipe/skills/
# No custom skills - using standard tools
```

**Project skills:** `.claude/skills/`
```bash
.claude/skills/
# No project-specific skills for MVP
```

---

## Agent Configuration

### MainAgent (Primary)

**Responsibilities:**
- All implementation tasks
- Code writing and testing
- Documentation
- Deployment

**Tools Available:**
- Read, Write, Edit (file operations)
- Bash (command execution)
- pytest (testing)
- alembic (migrations)

**Skills:**
- Standard Python development
- FastAPI framework
- PostgreSQL/SQLAlchemy
- Git/GitHub workflows

**Configuration:** `.claude/claude.md`, `.agent/agent.md`

### No Sub-Agents Defined

**All tasks assigned to MainAgent**

---

## Task-to-Skill Mapping

| Task | Skills/Tools Needed | Notes |
|------|-------------------|-------|
| TASK-001 | FastAPI, pytest | Standard setup |
| TASK-002 | SQLAlchemy, Alembic | Standard ORM |
| TASK-003 | FastAPI routing | Standard framework |
| TASK-004 | pytest | Basic testing |
| TASK-005 | Git, documentation | Standard workflow |
| TASK-006 | FastAPI, JWT, bcrypt | Standard auth libs |
| TASK-007 | SQLAlchemy, Alembic | Standard ORM |
| TASK-008 | FastAPI middleware | Standard framework |
| TASK-009 | SQLAlchemy, Alembic | Standard ORM |
| TASK-010 | SQLAlchemy | Standard ORM |
| TASK-011 | FastAPI, Pydantic | Standard framework |
| TASK-012 | Pydantic | Standard validation |
| TASK-013 | FastAPI | Standard framework |
| TASK-014 | Integration testing | Standard pytest |
| TASK-015 | Python logging | Standard library |
| TASK-016 | Prometheus/Grafana | Standard monitoring |
| TASK-017 | FastAPI/OpenAPI | Built-in docs |
| TASK-018 | Docker, CI/CD | Standard DevOps |
| TASK-019 | Locust/k6 | Standard load testing |
| TASK-020 | OWASP ZAP, bandit | Standard security tools |

**All tasks use standard, well-documented tools**

---

## Skill Installation & Setup

### Prerequisites

**System requirements:**
- Python 3.12+
- PostgreSQL 16+
- Docker (for local development)
- Git

**Python packages:**
```bash
pip install fastapi uvicorn sqlalchemy alembic \
    pytest httpx pydantic bcrypt pyjwt \
    python-dotenv
```

**Development tools:**
```bash
pip install black isort mypy bandit
```

**No custom skill installation required**

---

## Future Skill Needs

**Post-MVP considerations:**

### Potential Custom Skills

**1. API Client Generator**
- Auto-generate client libraries from OpenAPI spec
- Multiple language support
- Tasks: Client distribution, SDK maintenance

**2. Deployment Orchestrator**
- Multi-environment deployment workflow
- Rollback automation
- Tasks: Complex deployment scenarios

**3. Data Migration Tool**
- Legacy data import
- Transform and load automation
- Tasks: One-time migrations, data sync

**Not needed for MVP - defer to later phases**

---

## Notes

**Skill lifecycle:**
- Skills defined in Pass 2 (after tasks)
- Can be updated with change order
- New skills require testing before use

**Agent delegation:**
- Sub-agents created when MainAgent overwhelmed
- Handoff protocol must be defined
- State management between agents critical

**Standard tool preference:**
- Always prefer standard tools when available
- Custom skills only for repeated, unique needs
- Document why custom skill chosen

---

## Version History

**1.0.0** - Initial skill analysis
- No custom skills required
- Standard Python/FastAPI tooling sufficient
- MainAgent handles all tasks
```

---

## Stage 5 Workflow

### Pass 1: Core Implementation Plan

```
1. Human initiates Stage 5
   └─> Reviews Stage 4 completion

2. Agent creates phases.md
   └─> Defines 3-4 high-level phases
   └─> Sets milestones and deliverables

3. Agent creates tasks.md
   └─> Breaks each phase into tasks
   └─> Writes acceptance criteria for each
   └─> Estimates ~15-25 tasks total

4. Agent creates dependencies.md
   └─> Maps task dependencies
   └─> Identifies critical path
   └─> Finds parallelization opportunities

5. Agent creates effort-estimates.md
   └─> Assigns complexity to each task
   └─> Estimates time ranges
   └─> Calculates total effort

6. Human reviews Pass 1 artifacts
   └─> Validates completeness
   └─> Checks against solution design
   └─> Approves or requests revisions

7. Agent finalizes Pass 1 artifacts
   └─> Marks as locked
   └─> Version 1.0.0
```

### Pass 2: Execution Support

```
8. Agent analyzes tasks.md
   └─> Identifies task patterns
   └─> Looks for skill opportunities

9. Agent creates skills-and-agents.md
   └─> Lists required skills
   └─> Defines sub-agents (if needed)
   └─> Maps skills to tasks

10. Human reviews Pass 2
    └─> Approves skill selection
    └─> May request custom skills

11. Agent finalizes Pass 2
    └─> Marks skills-and-agents.md as locked
    └─> Implementation plan complete

12. Generate tasks.json (automated)
    └─> Parse tasks.md
    └─> Create JSON for tools
    └─> Git-ignore generated file
```

---

## Stage 5 Completion Criteria

### All Artifacts Created
- [ ] phases.md exists and locked
- [ ] tasks.md exists and locked
- [ ] dependencies.md exists and locked
- [ ] effort-estimates.md exists and locked
- [ ] skills-and-agents.md exists and locked

### Content Validation
- [ ] All solution design features have tasks
- [ ] Every task has acceptance criteria
- [ ] Dependencies form valid DAG (no cycles)
- [ ] Estimates total to realistic timeline
- [ ] Skills available or creation plan exists

### Quality Checks
- [ ] Tasks are granular (1-2 days max)
- [ ] Acceptance criteria are testable
- [ ] Critical path identified
- [ ] Parallelization opportunities noted
- [ ] Risk factors documented

### Integration Validation
- [ ] Cross-references to Stage 1-4 artifacts valid
- [ ] Tasks align with architecture decisions
- [ ] Repository structure supports tasks
- [ ] Workflow supports task execution

### Human Approval
- [ ] Pass 1 reviewed and approved
- [ ] Pass 2 reviewed and approved
- [ ] Overall plan signed off
- [ ] Ready to begin implementation

---

## Integration with Other Stages

### From Stage 4 (Workflow Configuration)
**Inputs:**
- claude.md (agent behavior rules)
- agent.md (generic agent rules)
- dev-workflow.md (git, PR, deployment process)
- repo-structure.md (file placement rules)

**Usage:**
- Task completion protocol in tasks.md
- Deviation handling in tasks.md
- File placement in acceptance criteria
- Git workflow in task completion

### To Implementation Execution
**Outputs:**
- tasks.md → Daily work queue
- phases.md → Phase completion targets
- dependencies.md → Task sequencing
- skills-and-agents.md → Tool/agent selection

**Enables:**
- Agent knows exactly what to build
- Agent knows in what order
- Agent knows when tasks complete
- Agent knows when to ask for help

---

## Common Mistakes to Avoid

### Don't
❌ Create tasks without acceptance criteria  
❌ Make tasks too large (>2 days)  
❌ Forget to map all solution design features  
❌ Skip dependency analysis  
❌ Estimate without considering parallelization  
❌ Create custom skills before evaluating standard tools  
❌ Lock plan before human review

### Do
✅ Every task has clear, testable acceptance criteria  
✅ Break large tasks into smaller subtasks  
✅ Trace every feature to at least one task  
✅ Build dependency graph before estimating  
✅ Consider both serial and parallel execution  
✅ Prefer standard tools over custom skills  
✅ Get human approval before locking plan

---

## Next Steps

After Stage 5 completion:

1. **CLAUDE.md Update** - Import tasks.md, phases.md
2. **Hook Configuration** - Enable implementation tracking
3. **Begin Implementation** - Start with TASK-001
4. **Track Progress** - Update tasks.md as tasks complete
5. **Monitor Velocity** - Compare actual vs estimates

---

## Appendix: Quick Reference

### File Locations
```
.ipe/implementation/
├── phases.md                  ← Phase breakdown
├── tasks.md                   ← All tasks (LOCKED)
├── dependencies.md            ← Task dependencies
├── effort-estimates.md        ← Complexity/time estimates
├── skills-and-agents.md       ← Skills/agents needed
├── implementation-state.json  ← Current state (updated by hooks)
└── tasks.json                 ← Generated (git-ignored)
```

### Key Concepts
- **Two-pass planning** - Core plan first, skills second
- **Locked status** - Changes require change order
- **Acceptance criteria** - Testable success conditions
- **Critical path** - Longest dependency chain
- **Deviation protocol** - What to do when stuck

### Validation Commands
```bash
# Validate all dependencies exist
python scripts/validate-dependencies.py

# Check for circular dependencies
python scripts/check-cycles.py

# Verify all features have tasks
python scripts/coverage-check.py

# Generate tasks.json from tasks.md
python scripts/generate-tasks-json.py
```

---

**Stage 5 is the bridge from design to code. Lock it carefully, follow it precisely, and use change orders for deviations.**
