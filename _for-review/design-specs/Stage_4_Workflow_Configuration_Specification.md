# Stage 4: Workflow Configuration

**Stage:** 4 of 5  
**Name:** Workflow Configuration  
**Purpose:** Define how development happens - agent behavior, processes, operational rules, and memory management  
**Dependencies:** Stage 3 (Environment Setup) must be complete  
**Outputs:** 6-7 artifacts defining development workflows and agent configuration

---

## Overview

Stage 4 establishes the operational framework for development. It defines how agents behave, how code changes flow through the system, how memory is managed, and how teams operate together.

**Key Question Answered:** "How do we work in this project?"

**Difference from Previous Stages:**
- Stage 1-2: What to build
- Stage 3: Where to build it
- **Stage 4:** How to build it (process, behavior, rules)
- Stage 5: When and in what order

---

## Stage 4 Artifacts

| Artifact | Purpose | Type | Lifecycle |
|----------|---------|------|-----------|
| **claude.md** | Claude Code specific configuration | Markdown | Continuous |
| **agent.md** | Generic agent configuration | Markdown | Continuous |
| **dev-workflow.md** | Branch, PR, commit, deployment process | Markdown | Governed |
| **environment-variants.md** | Local/staging/production configs | Markdown | Governed |
| **context-management.md** | Memory, drift detection, pruning | Markdown | Governed |
| **operations-playbook.md** | Common workflows, troubleshooting | Markdown | Continuous |
| **claude-config.md** | CLAUDE.md structure definition | Markdown | Governed |
| **workflow-synthesis.md** | Stage summary (optional) | Markdown | Finalized |

**Governed artifacts:** Require change order to modify after finalization  
**Continuous artifacts:** Updated regularly, pruned periodically

---

## Critical Distinction: claude.md vs agent.md

### Why Separate Files?

**Claude Code has specific requirements:**
- CLAUDE.md is loaded automatically at startup
- Has specific syntax (@imports, # shortcut)
- Hooks into Claude Code lifecycle
- Used by Claude Code as primary agent

**Other agents have different mechanisms:**
- Agent.md is industry standard (not Claude-specific)
- Used by Cursor, Windsurf, Codex, Gemini, etc.
- Different loading mechanisms
- Different file locations

### File Locations

**Claude Code:**
```
.claude/
├── CLAUDE.md              ← Primary config (auto-generated from claude-config.md)
├── CLAUDE.local.md        ← User-specific overrides (.gitignored)
└── settings.json          ← Hooks, tools, permissions
```

**Other Agents:**
```
.agent/
├── agent.md               ← Generic agent config
└── [agent-specific files]

OR (depending on agent):

.cursor/
├── rules.md

.windsurf/
├── config.md
```

### Content Overlap Strategy

**Shared content (90%):**
- File placement rules
- Task completion protocols
- Code quality standards
- Security requirements
- Project context

**Claude-specific (10%):**
- CLAUDE.md syntax (@imports)
- Claude Code slash commands
- Hook integration references
- MCP server usage

**Implementation:**
```markdown
# claude.md

## Core Rules
@.claude/shared-rules.md   ← Shared with all agents

## Claude-Specific
Use /memory to update project context
Reference claude-mem for implementation history
```

```markdown
# agent.md

## Core Rules
<!-- Include shared-rules.md content here -->

## Agent-Agnostic Instructions
Use your native mechanisms for:
- Memory updates
- Context retrieval
- Tool usage
```

---

## Artifact 1: claude.md

**Purpose:** Claude Code specific agent configuration  
**Location:** `.claude/claude.md`  
**Lifecycle:** Continuous (updated regularly, pruned periodically)

**Note:** This is NOT the same as `.claude/CLAUDE.md` (which is auto-generated). This file defines RULES for Claude Code behavior.

### Template: claude.md

```markdown
---
# Not an IPE artifact - this is Claude Code configuration
# No artifact/status frontmatter required
---

# Claude Code Configuration

**Project:** [Project Name]  
**Last Pruned:** [Date]

---

## [GLOBAL] - Base Rules (Never Remove)

### Task Completion Protocol (NON-NEGOTIABLE)
1. Complete task as specified in tasks.md
2. Mark task complete in tasks.md with:
   - Completion date (YYYY-MM-DD)
   - Git commit SHA
   - Brief completion notes
3. Git commit with message format: `[TASK-XXX] Brief description`
4. Generate progress summary
5. ONLY THEN proceed to next task

### Deviation Protocol
IF task cannot be completed as specified:
1. STOP immediately
2. Document issue in tasks.md as comment:
   ```markdown
   <!-- BLOCKED: TASK-XXX
   Issue: [what failed]
   Attempted: [what was tried]
   Needs: [human decision required]
   -->
   ```
3. Alert human via system message
4. Wait for human decision
5. DO NOT improvise alternative approach
6. DO NOT skip to next task

### Tool Usage Protocol
IF specified tool not working:
1. Retry with correct syntax (check skill/docs once)
2. If still failing, follow Deviation Protocol
3. DO NOT create workaround script without approval
4. DO NOT decide tool is unavailable and move on

### File Placement Rules
BEFORE creating or modifying ANY file:
1. Check location against @.ipe/environment-setup/repo-structure.md
2. If location unclear, ASK human
3. NEVER create files in project root (except entry points)
4. NEVER put tests in src/ directory

**Examples:**
- ✅ `src/api/v1_users.py` (correct)
- ❌ `api/users.py` (missing src prefix)
- ❌ `user_test.py` (tests must be in tests/)

---

## [PROJECT] - Project-Specific Context

### Stack & Architecture
- **Language:** Python 3.12
- **Framework:** FastAPI (async-first)
- **Database:** PostgreSQL 16 with SQLAlchemy
- **Key Patterns:** Dependency injection, async everywhere

### Repository Structure
@.ipe/environment-setup/repo-structure.md

**Critical Files:**
- `src/main.py` - Application entry point
- `src/api/` - API route handlers
- `src/models/` - Database models
- `src/services/` - Business logic
- `tests/` - All tests (mirrors src structure)

### Current Stage
**Stage:** 5 - Implementation  
**Phase:** MVP - Foundation  
**Active Task:** Check tasks.md for current work

---

## [USER] - User Preferences

<!-- User adds personal preferences here -->
<!-- Example: "Prefer detailed commit messages" -->
<!-- Example: "Ask before installing new dependencies" -->

---

## [AGENT-DERIVED] - Context Built by Agents

<!-- Auto-populated by agents during work -->
<!-- Expires after 30 days - prune regularly -->

**Recent Patterns:**
<!-- None yet - add as discovered -->

**Temporary Notes:**
<!-- Add with [STALE after YYYY-MM-DD] markers -->

---

## Claude Code Specific Features

### Memory Management
- Use `/memory` to edit this file
- Use `#` shortcut for quick additions
- Review CLAUDE.md for persistent project context

### Search & Retrieval
- Use mem-search skill for implementation history
- Query: "What did we do last session?"
- Query: "How did we implement authentication?"

### Progressive Disclosure
- Check observation index at session start
- Fetch details on-demand via mem-search
- Access perfect recall via source files

---

## Pruning Triggers

**Auto-alert when:**
- File exceeds 500 lines
- 20+ commits since last pruned
- Agent-derived section >300 lines
- 10+ items marked [STALE]

**Pruning workflow:**
1. Review agent-derived content
2. Remove completed/irrelevant items
3. Archive useful patterns to PROJECT section
4. Update [Last Pruned] date

---

## Integration with IPE

### Stage Artifacts (Always Reference)
@.ipe/discovery/synthesis.md  
@.ipe/solution-design/architecture.md  
@.ipe/environment-setup/repo-structure.md  
@.ipe/workflow-config/dev-workflow.md  
@.ipe/implementation/tasks.md

### Workflow Documents
@.ipe/workflow-config/dev-workflow.md - Git workflow, PR process  
@.ipe/workflow-config/operations-playbook.md - Common tasks

### CLAUDE.md Integration
This file (claude.md) defines BEHAVIOR.  
`.claude/CLAUDE.md` provides CONTEXT (auto-generated).  
Both are loaded at session start.
```

---

## Artifact 2: agent.md

**Purpose:** Generic agent configuration (non-Claude agents)  
**Location:** `.agent/agent.md` or per-agent directories  
**Lifecycle:** Continuous

### Template: agent.md

```markdown
# Agent Configuration

**Project:** [Project Name]  
**Applies To:** All agents (Cursor, Codex, Windsurf, Gemini, etc.)

---

## Core Principles

### 1. Task Completion Protocol
Every task must be:
1. Completed as specified in tasks.md
2. Marked complete with date, commit SHA, notes
3. Git committed with format: `[TASK-XXX] Description`
4. Summarized before moving to next task

### 2. Deviation Handling
If task cannot be completed:
1. Stop immediately
2. Document the blocker
3. Alert human for decision
4. Do not improvise alternatives
5. Do not skip ahead

### 3. File Placement
Before creating any file:
1. Validate location against repo-structure.md
2. Ask if unclear
3. Never create files in root (except entry points)
4. Tests must mirror src structure in tests/

---

## Project Context

### Technology Stack
- Language: Python 3.12
- Framework: FastAPI (async-first)
- Database: PostgreSQL 16
- Testing: pytest + coverage

### Architecture
- Pattern: Microservices
- Communication: Async message queues
- State: Stateless services
- See: .ipe/solution-design/architecture.md

### Repository Structure
See: .ipe/environment-setup/repo-structure.md

**Key Locations:**
- Source code: `src/` only
- Tests: `tests/` (mirrors src)
- Entry point: `src/main.py`
- No code in root except main.py

---

## Workflows

### Git Workflow
See: .ipe/workflow-config/dev-workflow.md

**Summary:**
- Branch: feature/TASK-XXX-description
- Commit: [TASK-XXX] Description
- PR: Title references task
- Merge: Squash to main

### Task Workflow
See: .ipe/implementation/tasks.md

**Summary:**
1. Read task specification
2. Create feature branch
3. Implement with tests
4. Mark complete in tasks.md
5. Commit and push

---

## Agent-Specific Instructions

### For Memory Updates
Use your agent's native mechanism:
- Claude Code: `/memory` command
- Cursor: Update .cursor/rules.md
- Windsurf: Update configuration
- Generic: Edit this file directly

### For Context Retrieval
Use your agent's native search:
- Claude Code: mem-search skill
- Others: Search project files, git history

### For Tool Integration
Use available tools according to your agent's capabilities:
- File operations: Read, Write, Edit
- Execution: Bash, Language-specific runners
- Search: Grep, Glob, Find

---

## Critical Rules (Enforced)

### File Creation
```python
# Before creating ANY file:
def validate_file_location(path: str) -> bool:
    # 1. Check against repo-structure.md rules
    # 2. Verify allowed directory
    # 3. Ask human if unclear
    pass
```

### Task Completion
```python
# After completing ANY task:
def complete_task(task_id: str) -> None:
    # 1. Mark in tasks.md
    # 2. Add completion metadata
    # 3. Git commit with task reference
    # 4. Generate summary
    pass
```

### Error Handling
```python
# When ANY tool fails:
def handle_tool_failure(tool: str, error: str) -> None:
    # 1. Retry once with correct syntax
    # 2. If still fails, STOP
    # 3. Document issue
    # 4. Alert human
    # 5. DO NOT improvise workaround
    pass
```

---

## Shared Rules Reference

For detailed rules shared across all agents:
See: .ipe/workflow-config/shared-rules.md

---

## Maintenance

**Last Updated:** [Date]  
**Next Review:** [Date + 30 days]  

**Pruning needed when:**
- File exceeds 400 lines
- Contains stale context (>30 days old)
- Multiple agents report confusion
```

---

## Artifact 3: dev-workflow.md

**Purpose:** Git workflow, branching, commits, PRs, deployment  
**Location:** `.ipe/workflow-config/dev-workflow.md`  
**Lifecycle:** Governed (requires change order after finalization)

### Template: dev-workflow.md

```markdown
---
artifact: dev-workflow.md
status: draft
stage: workflow-config
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: []
---

# Development Workflow

## Purpose

Defines how code changes flow from development to production, including
branching strategy, commit standards, PR process, and deployment pipeline.

---

## Branching Strategy

### Branch Types

**main**
- Production-ready code
- Protected branch (no direct commits)
- Always deployable
- Requires PR for changes

**feature/TASK-XXX-description**
- Feature development branches
- Created from main
- One branch per task
- Deleted after merge

**hotfix/issue-description**
- Emergency production fixes
- Created from main
- Fast-tracked review
- Merged immediately

**release/vX.Y.Z** (if using release branches)
- Stabilization before release
- No new features
- Bug fixes only
- Merged to main + tagged

### Branch Naming

**Format:** `<type>/<task-or-issue>-<short-description>`

**Examples:**
- `feature/TASK-012-user-authentication`
- `feature/TASK-020-api-endpoints`
- `hotfix/database-connection-leak`
- `release/v1.0.0`

**Rules:**
- Lowercase only
- Hyphens for word separation
- Task ID when applicable
- Descriptive but concise

---

## Commit Standards

### Commit Message Format

```
[TASK-XXX] Brief description (50 chars or less)

Detailed explanation of what changed and why (if needed).
Wrap at 72 characters.

- Bullet points for multiple changes
- Reference related tasks or issues
- Explain non-obvious decisions

Co-authored-by: Name <email>  (if pair programming)
```

**Examples:**

```
[TASK-012] Implement user authentication service

Added FastAPI dependency injection for auth service.
Includes bcrypt password hashing and JWT token generation.

- Created User model with SQLAlchemy
- Added auth routes to API
- Implemented token validation middleware
```

```
[TASK-020] Add GET /users endpoint

Returns paginated list of users with filtering options.
```

```
[HOTFIX] Fix database connection pool exhaustion

Connection pool was not being released after queries.
Added explicit connection.close() in finally blocks.
```

### Commit Frequency

**Commit when:**
- Completing a logical unit of work
- Before switching tasks
- Before ending work session
- After passing tests
- At natural checkpoints

**Do NOT commit:**
- Broken code
- Failing tests
- Commented-out debugging code
- Secrets or credentials
- Large binary files (without LFS)

### Commit Best Practices

```bash
# Stage specific files only
git add src/auth/service.py tests/test_auth.py

# Write descriptive message
git commit -m "[TASK-012] Add password hashing to auth service"

# Push regularly
git push origin feature/TASK-012-user-authentication
```

---

## Pull Request Process

### Creating PRs

**When to create:**
- Task is complete
- All tests passing
- Code reviewed locally
- Branch up to date with main

**PR Template:**

```markdown
## Task
Closes #TASK-XXX

## Changes
- Added user authentication service
- Implemented JWT token generation
- Created auth API endpoints

## Testing
- [x] Unit tests passing
- [x] Integration tests passing
- [x] Manual testing complete

## Checklist
- [x] Code follows style guide
- [x] Tests added/updated
- [x] Documentation updated
- [x] No secrets committed
- [x] Breaking changes noted

## Screenshots (if applicable)
[Add screenshots of UI changes]

## Additional Notes
[Any context reviewers should know]
```

### Review Process

**Reviewer responsibilities:**
1. Code quality and readability
2. Test coverage adequate
3. Follows architecture patterns
4. No security vulnerabilities
5. Documentation updated

**Review timeline:**
- Standard PRs: 24-48 hours
- Hotfixes: Same day
- Large PRs: Split or schedule review session

**Required approvals:**
- 1 approval minimum
- 2 approvals for breaking changes
- All comments resolved

### Merge Strategy

**Squash and merge (default):**
- Keeps main history clean
- Single commit per task
- Preserves PR link in commit

**Merge commit (for releases):**
- Preserves branch history
- Used for release branches
- Shows feature grouping

**Rebase (rarely):**
- Only for keeping feature branch updated
- Not for merging to main

---

## Deployment Pipeline

### Environments

**Local (development)**
- Individual developer machines
- SQLite or local PostgreSQL
- No CI/CD
- Manual testing

**Staging (pre-production)**
- Mirrors production config
- Shared team environment
- Auto-deployed from main
- Integration testing

**Production**
- Live user environment
- Full monitoring/logging
- Manual deployment trigger
- Requires approval

### Deployment Process

**To Staging (automatic):**
```yaml
# Triggered on push to main
on:
  push:
    branches: [main]

steps:
  - Run tests
  - Build container
  - Deploy to staging
  - Run smoke tests
  - Notify team
```

**To Production (manual):**
```yaml
# Triggered manually via GitHub Actions
on:
  workflow_dispatch:
    inputs:
      version:
        required: true

steps:
  - Tag release
  - Run full test suite
  - Build production container
  - Deploy with zero downtime
  - Verify health checks
  - Notify stakeholders
```

### Rollback Procedure

**If deployment fails:**
1. Immediately revert to previous version
2. Document failure reason
3. Create hotfix branch if needed
4. Test fix in staging
5. Re-deploy when ready

**Rollback command:**
```bash
# Via deployment tool
deploy rollback production --to-version v1.2.3

# Or via git
git revert <commit-sha>
git push origin main
```

---

## Code Review Checklist

### Code Quality
- [ ] Code is readable and well-organized
- [ ] Functions are single-purpose
- [ ] Variable names are descriptive
- [ ] No duplicated code
- [ ] Comments explain "why" not "what"

### Testing
- [ ] Unit tests cover new code
- [ ] Integration tests for new features
- [ ] Edge cases tested
- [ ] Tests are readable and maintainable

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities checked
- [ ] Authentication/authorization correct

### Performance
- [ ] No N+1 queries
- [ ] Async patterns used appropriately
- [ ] Database indexes considered
- [ ] Resource cleanup implemented

### Documentation
- [ ] README updated if needed
- [ ] API docs updated
- [ ] Docstrings added
- [ ] CHANGELOG updated

---

## Emergency Procedures

### Production Hotfix

**Process:**
1. Create hotfix branch from main
2. Implement minimal fix
3. Test thoroughly
4. Fast-track PR review
5. Deploy to production immediately
6. Post-mortem after resolution

**Timeline:**
- Critical (service down): <1 hour
- High (data loss risk): <4 hours
- Medium (degraded service): <1 day

### Rollback Decision

**Rollback if:**
- Service unavailable
- Data corruption detected
- Security vulnerability introduced
- Critical functionality broken

**Do NOT rollback if:**
- Minor UI glitch
- Non-critical feature broken
- Performance slightly degraded

---

## Workflow Governance

### Change Control

**This document is GOVERNED after finalization.**

To modify after finalization:
1. Create change order (CO-XXX)
2. Document reason and impact
3. Human approval required
4. Version increment (semver)
5. Update all references

**Typical changes requiring change order:**
- New deployment environment
- Different branching strategy
- Modified review requirements
- Changed merge strategy

### Version History

**1.0.0** - Initial workflow definition
```

---

## Artifact 4: environment-variants.md

**Purpose:** Different environment configurations (local, staging, production)  
**Location:** `.ipe/workflow-config/environment-variants.md`  
**Lifecycle:** Governed

### Template: environment-variants.md

```markdown
---
artifact: environment-variants.md
status: draft
stage: workflow-config
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: [../environment-setup/environment-config.md]
---

# Environment Variants

## Purpose

Defines configuration differences between local development, staging, and 
production environments, including secrets management and environment-specific
behavior.

---

## Environment Definitions

### Local (Development)

**Purpose:** Individual developer machines  
**Data:** Synthetic test data  
**Secrets:** Local .env file (not committed)

**Configuration:**
```bash
# .env.local (example - not committed)
ENVIRONMENT=local
DEBUG=true
LOG_LEVEL=DEBUG

DATABASE_URL=postgresql://localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379

API_KEY=local-test-key
SECRET_KEY=local-insecure-secret-for-dev-only
```

**Characteristics:**
- Fast feedback loops
- Full logging/debugging
- Permissive CORS
- Synthetic data only
- Local database

---

### Staging (Pre-Production)

**Purpose:** Team shared testing environment  
**Data:** Production-like synthetic data  
**Secrets:** Environment variables via deployment platform

**Configuration:**
```bash
# Set via platform (Railway, Render, etc.)
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO

DATABASE_URL=<managed-database-url>
REDIS_URL=<managed-redis-url>

API_KEY=<staging-api-key>
SECRET_KEY=<generated-secure-secret>
```

**Characteristics:**
- Mirrors production config
- Deployed automatically from main
- Shared team access
- Integration testing
- Managed services

---

### Production

**Purpose:** Live user environment  
**Data:** Real user data  
**Secrets:** Secure secret manager (AWS Secrets Manager, etc.)

**Configuration:**
```bash
# Set via secure secret manager
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

DATABASE_URL=<production-database-url>
REDIS_URL=<production-redis-url>

API_KEY=<production-api-key>
SECRET_KEY=<production-secure-secret>
```

**Characteristics:**
- High availability
- Full monitoring/alerting
- Strict security
- Real user data
- Manual deployment gate

---

## Configuration Management

### .env File Structure

**Template: .env.template (committed)**
```bash
# Environment
ENVIRONMENT=local

# Database
DATABASE_URL=postgresql://localhost:5432/myapp_dev

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=changeme
API_KEY=changeme

# External Services
STRIPE_API_KEY=changeme
SENDGRID_API_KEY=changeme

# Feature Flags
FEATURE_NEW_UI=false
```

**Actual: .env (NOT committed)**
```bash
# Copy from .env.template and fill in real values
ENVIRONMENT=local
DATABASE_URL=postgresql://user:pass@localhost:5432/myapp_dev
SECRET_KEY=<generated-local-secret>
# ... etc
```

### Secrets Management

**Local:**
- .env file (in .gitignore)
- Never commit secrets
- Use placeholder values in templates

**Staging/Production:**
- Platform environment variables (Railway, Render)
- OR secret manager (AWS Secrets Manager, Vault)
- Secrets injected at runtime
- Never in code or git history

**Secret Rotation:**
- API keys: Quarterly
- Database passwords: Annually or on exposure
- JWT secrets: On security incident
- Service tokens: Per vendor recommendation

---

## Environment-Specific Behavior

### Feature Flags

```python
# Using environment to control features
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Different behavior per environment
if ENVIRONMENT == "production":
    RATE_LIMIT = 100  # Requests per minute
    CACHE_TTL = 3600  # 1 hour
    ENABLE_METRICS = True
elif ENVIRONMENT == "staging":
    RATE_LIMIT = 1000
    CACHE_TTL = 300  # 5 minutes
    ENABLE_METRICS = True
else:  # local
    RATE_LIMIT = 10000
    CACHE_TTL = 60  # 1 minute
    ENABLE_METRICS = False
```

### Logging Configuration

```python
# Environment-specific logging
import logging

if os.getenv("ENVIRONMENT") == "production":
    logging.basicConfig(
        level=logging.WARNING,
        format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
        handlers=[logging.StreamHandler()]
    )
elif os.getenv("ENVIRONMENT") == "staging":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
else:  # local
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(message)s'
    )
```

### Database Connections

```python
# Environment-specific connection pooling
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "production":
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True
    )
elif ENVIRONMENT == "staging":
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=5
    )
else:  # local
    engine = create_engine(
        DATABASE_URL,
        echo=True  # SQL logging for dev
    )
```

---

## Environment Validation

### Startup Checks

```python
# Validate environment configuration at startup
import os
import sys

REQUIRED_ENV_VARS = [
    "ENVIRONMENT",
    "DATABASE_URL",
    "SECRET_KEY"
]

def validate_environment():
    """Ensure all required environment variables are set"""
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    
    if missing:
        print(f"ERROR: Missing required environment variables: {missing}")
        print("Check .env.template for required configuration")
        sys.exit(1)
    
    # Environment-specific validation
    env = os.getenv("ENVIRONMENT")
    if env == "production":
        # Stricter checks for production
        secret_key = os.getenv("SECRET_KEY")
        if len(secret_key) < 32:
            print("ERROR: Production SECRET_KEY must be at least 32 characters")
            sys.exit(1)

# Run at app startup
validate_environment()
```

### Health Checks

```python
# Environment-specific health checks
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """Basic health check for all environments"""
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT")}

@router.get("/health/detailed")
def detailed_health():
    """Detailed health check (staging/production only)"""
    if os.getenv("ENVIRONMENT") == "local":
        return {"error": "Not available in local environment"}
    
    return {
        "status": "healthy",
        "database": check_database_connection(),
        "redis": check_redis_connection(),
        "external_apis": check_external_services()
    }
```

---

## Migration Between Environments

### Data Seeding

**Local:**
```bash
# Seed with synthetic data
python scripts/seed_local_data.py

# Creates:
# - 100 test users
# - 1000 sample records
# - All features enabled
```

**Staging:**
```bash
# Seed with production-like data
python scripts/seed_staging_data.py

# Creates:
# - Anonymized production snapshot
# - Test accounts for QA
# - Feature flags match production
```

**Production:**
```bash
# No seeding - real data only
# Migrations only
```

### Configuration Sync

**Keep in sync:**
- Environment variable names
- Required vs optional vars
- Default values
- Validation rules

**Track differences:**
- .env.template (source of truth)
- Environment-specific docs
- Deployment configs

---

## Troubleshooting

### "Environment variable not found"

**Symptoms:** App crashes on startup with missing var error

**Solutions:**
1. Check .env file exists
2. Compare against .env.template
3. Verify var names (case-sensitive)
4. Restart app after changes

### "Database connection failed"

**Symptoms:** Can't connect to database

**Solutions:**
- **Local:** Ensure PostgreSQL running (`brew services start postgresql`)
- **Staging/Production:** Check DATABASE_URL format
- **All:** Verify credentials, network access

### "Secrets not loading in production"

**Symptoms:** App uses placeholder values

**Solutions:**
1. Verify secrets exist in secret manager
2. Check IAM permissions for secret access
3. Confirm secret names match code
4. Restart service to reload secrets
```

---

## Artifact 5: context-management.md

**Purpose:** Memory, pruning, drift detection configuration  
**Location:** `.ipe/workflow-config/context-management.md`  
**Lifecycle:** Governed

### Template: context-management.md

```markdown
---
artifact: context-management.md
status: draft
stage: workflow-config
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: [claude-config.md]
---

# Context Management

## Purpose

Defines how project context is maintained, when memory files are pruned,
how drift is detected, and what mechanisms prevent context degradation.

---

## Memory Architecture

### CLAUDE.md (Static Context)
**Location:** `.claude/CLAUDE.md`  
**Source:** Auto-generated from claude-config.md  
**Update Frequency:** On stage completion, task milestones  
**Content:** Decisions, rules, stage status, imports

**See:** claude-config.md for structure definition

### claude.md (Behavior Rules)
**Location:** `.claude/claude.md`  
**Source:** Manually curated  
**Update Frequency:** Continuous (with pruning)  
**Content:** Agent behavior rules, project-specific context

**Lifecycle:**
- **[GLOBAL]** - Never removed
- **[PROJECT]** - Updated per project needs
- **[USER]** - Personal preferences
- **[AGENT-DERIVED]** - Auto-populated, requires pruning

### claude-mem (Implementation History)
**Location:** SQLite database + Chroma vector DB  
**Source:** Automatic via hooks  
**Update Frequency:** Real-time during development  
**Content:** Tool usage observations, implementation timeline

**Retention:** 90 days (configurable)

---

## Pruning Strategy

### Agent Configuration Files

**Triggers for pruning claude.md:**

| Trigger Type | Threshold | Severity |
|--------------|-----------|----------|
| Time | 7 days since last pruned | Warning |
| Commits | 20 commits since last pruned | Warning |
| Size | 500+ lines in agent-derived section | Critical |
| Staleness | 10+ items marked [STALE] | Warning |
| Activity | 50+ edits in 24 hours | Info |

**Pruning workflow:**
```
1. Trigger detected
2. Agent proposes removals:
   - Items >30 days old
   - Resolved issues
   - Completed tasks
   - Deprecated patterns
3. Human reviews and approves
4. Agent executes removal
5. Update "Last Pruned" date
```

**Example agent proposal:**
```markdown
## Pruning Suggestions for claude.md

**Trigger:** 23 commits since last pruned (threshold: 20)

### Suggested Removals (12 items)

☑ "Recent file: temp_test.py" (35 days old)  
☑ "Workaround for database connection" (resolved in TASK-018)  
☑ "Pattern: Old FastAPI syntax" (updated to 0.115)  
☐ "Common pattern: async routes" (keep - still relevant)  

☑ "Note: Investigate Redis timeout" (completed in TASK-025)  
☑ "[STALE after 2025-01-15] Testing auth bypass" (date passed)

### Suggested Updates (3 items)

• Update Python version reference: 3.11 → 3.12  
• Refresh file location examples with current paths  
• Mark old database migration pattern as [DEPRECATED]

**Actions:**
[Apply All] [Review Each] [Cancel]
```

---

## Drift Detection

### Repository Structure Drift

**What is drift?**
Files created outside allowed locations per repo-structure.md

**Detection mechanisms:**

**1. Real-time (via hooks):**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Create",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-structure.sh"
      }]
    }]
  }
}
```

**2. Periodic scan:**
```bash
# Run nightly or on-demand
python scripts/detect-drift.py

# Checks:
# - Files in unexpected locations
# - Missing expected directories
# - Files violating naming conventions
```

**3. Pre-commit validation:**
```bash
# .git/hooks/pre-commit
./scripts/validate-repo-structure.sh

# Blocks commit if violations found
```

**Drift severity levels:**

| Severity | Example | Action |
|----------|---------|--------|
| **Critical** | Source code in root | Block commit |
| **Warning** | Test file in wrong location | Flag for review |
| **Info** | Missing optional directory | Log only |

**Drift handling workflow:**
```
1. Drift detected
2. Generate report:
   - File location
   - Expected location
   - Severity
   - Suggested fix
3. Human decision:
   - Move file (fix drift)
   - Update repo-structure.md (legalize drift)
   - Ignore (temporary exception)
4. Log decision
5. Update drift baseline
```

---

## Context Configuration Settings

**Location:** `.claude-mem/settings.json`

**Available settings:**

```json
{
  "context_injection": {
    "observations_count": 50,
    "show_token_costs": true,
    "show_type_indicators": true,
    "filter_by_type": [],
    "filter_by_concept": [],
    "exclude_types": ["informational"],
    "group_by_date": true,
    "progressive_disclosure": true
  },
  
  "memory_retention": {
    "observations_days": 90,
    "sessions_days": 180,
    "prune_schedule": "weekly"
  },
  
  "drift_detection": {
    "scan_schedule": "daily",
    "auto_fix_enabled": false,
    "severity_threshold": "warning",
    "notification_mode": "ui"
  },
  
  "pruning": {
    "auto_suggest": true,
    "require_approval": true,
    "stale_threshold_days": 30
  }
}
```

### Context Injection Control

**Observations count:**
- **Default:** 50 observations at session start
- **Range:** 10-100
- **Token impact:** ~500 tokens per observation
- **Recommendation:** Start with 50, adjust based on session needs

**Token economics display:**
```markdown
## Recent Observations (Token Estimates)

🔴 TASK-015: Critical auth bug fix (~800 tokens) [critical, bugfix]
🟤 TASK-014: Database schema decision (~600 tokens) [decision]
🔵 TASK-013: API endpoint pattern (~400 tokens) [pattern]
...

**Total index:** ~15,000 tokens
**Details available via mem-search**
```

**Filtering by type:**
```json
{
  "filter_by_type": ["critical", "decision"],
  "exclude_types": ["informational"]
}
```

**Result:** Only critical decisions and decisions shown at session start

**Filtering by concept:**
```json
{
  "filter_by_concept": ["authentication", "database"]
}
```

**Result:** Only observations about auth or database shown

---

## Validation & Quality Gates

### Context Quality Metrics

**Tracked metrics:**
- Token usage per session (target: <100K)
- Observation relevance (measured by retrieval frequency)
- Pruning frequency (target: every 20 commits)
- Drift detection rate (target: <5 violations/week)

**Quality gates:**

```python
def validate_context_quality():
    """Run before stage finalization"""
    
    issues = []
    
    # Check 1: Token budget
    total_tokens = estimate_context_tokens()
    if total_tokens > 100_000:
        issues.append(f"Context exceeds token budget: {total_tokens}")
    
    # Check 2: Stale content
    stale_count = count_stale_items()
    if stale_count > 10:
        issues.append(f"Too many stale items: {stale_count}")
    
    # Check 3: Drift violations
    drift = detect_drift()
    critical_drift = [d for d in drift if d.severity == "critical"]
    if critical_drift:
        issues.append(f"Critical drift violations: {len(critical_drift)}")
    
    return issues
```

### Automated Maintenance

**Daily tasks:**
- Drift scan
- Token usage analysis
- Stale content flagging

**Weekly tasks:**
- Pruning suggestions
- Context quality report
- Memory retention cleanup

**Monthly tasks:**
- Full context audit
- Drift pattern analysis
- Memory optimization review

---

## Integration with IPE Stages

### Stage 1-2: Discovery & Design
**Context focus:** Decisions, research, architecture
**Pruning:** Rarely (foundational knowledge)
**Drift:** N/A (no code yet)

### Stage 3: Environment Setup
**Context focus:** Setup decisions, tool choices
**Pruning:** After setup complete
**Drift:** Baseline repo structure

### Stage 4: Workflow Config
**Context focus:** Process rules, agent behavior
**Pruning:** Define triggers and thresholds
**Drift:** Workflow documentation

### Stage 5: Implementation
**Context focus:** Task completion, implementation details
**Pruning:** Frequent (every 20 commits)
**Drift:** Active monitoring (daily scans)

---

## Troubleshooting

### "Too much context, agent is slow"

**Symptoms:** Long response times, token limit errors

**Solutions:**
1. Reduce `observations_count` setting
2. Filter by type/concept
3. Prune stale agent-derived content
4. Move historical observations to archive

### "Agent keeps forgetting decisions"

**Symptoms:** Re-asking settled questions

**Solutions:**
1. Check CLAUDE.md includes key decisions
2. Verify imports are loading correctly
3. Add to [PROJECT] section of claude.md
4. Query claude-mem for decision history

### "Drift violations not being detected"

**Symptoms:** Files in wrong locations not flagged

**Solutions:**
1. Verify hooks are installed
2. Run manual drift scan
3. Check repo-structure.md is up to date
4. Review drift detection logs

### "Pruning suggestions not appearing"

**Symptoms:** No auto-suggestions despite triggers

**Solutions:**
1. Check pruning settings enabled
2. Verify agent-derived section has content
3. Manually trigger pruning review
4. Check if `require_approval` is true
```

---

## Artifact 6: operations-playbook.md

**Purpose:** Common workflows, troubleshooting, emergency procedures  
**Location:** `.ipe/workflow-config/operations-playbook.md`  
**Lifecycle:** Continuous (living document)

### Template: operations-playbook.md

```markdown
---
artifact: operations-playbook.md
status: draft
stage: workflow-config
created: YYYY-MM-DD [Author]
updated: YYYY-MM-DD [Author]
related: [dev-workflow.md, environment-variants.md]
---

# Operations Playbook

## Purpose

Quick reference for common development tasks, troubleshooting procedures,
and emergency response workflows.

---

## Common Workflows

### Starting a New Task

```bash
# 1. Sync with main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/TASK-XXX-description

# 3. Verify environment
source .env
python --version  # Verify correct version
pip list | grep fastapi  # Check dependencies

# 4. Run tests to establish baseline
pytest

# 5. Begin work
# ... implement task ...

# 6. Commit regularly
git add <files>
git commit -m "[TASK-XXX] Description"
git push origin feature/TASK-XXX-description
```

### Completing a Task

```bash
# 1. Verify implementation complete
# - All acceptance criteria met
# - Tests passing
# - Code reviewed locally

# 2. Update tasks.md
# Mark task as complete with:
# - Completion date
# - Git commit SHA
# - Brief notes

# 3. Final commit
git add .ipe/implementation/tasks.md
git commit -m "[TASK-XXX] Mark task complete"
git push

# 4. Create PR
gh pr create \
  --title "[TASK-XXX] Description" \
  --body "$(cat PR_TEMPLATE.md)"

# 5. Wait for review and merge
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_auth.py

# Specific test function
pytest tests/test_auth.py::test_login_success

# With coverage
pytest --cov=src --cov-report=html

# Watch mode (re-run on changes)
pytest-watch

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Database Operations

```bash
# Create migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Reset database (CAUTION: deletes all data)
alembic downgrade base
alembic upgrade head

# Seed data
python scripts/seed_data.py

# Backup database
pg_dump myapp_dev > backup_$(date +%Y%m%d).sql

# Restore database
psql myapp_dev < backup_20250101.sql
```

### Deployment

```bash
# To staging (automatic on push to main)
git push origin main

# To production (manual trigger)
# Via GitHub Actions:
gh workflow run deploy-production.yml

# Or via deployment platform:
railway up --service myapp-prod

# Verify deployment
curl https://api.myapp.com/health
```

---

## Troubleshooting

### Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'X'`

**Solutions:**
```bash
# Verify virtual environment active
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Must be 3.12+

# Verify package installed
pip list | grep <package-name>

# Clear pip cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall
```

### Database Connection Issues

**Symptom:** `Could not connect to database`

**Solutions:**
```bash
# Check PostgreSQL running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection manually
psql $DATABASE_URL

# Check port not in use
lsof -i :5432

# Restart PostgreSQL
brew services restart postgresql  # macOS
sudo systemctl restart postgresql  # Linux
```

### Test Failures

**Symptom:** Tests failing unexpectedly

**Solutions:**
```bash
# Run with verbose output
pytest -v tests/test_<failing>.py

# Check test database state
pytest --setup-show

# Reset test database
alembic downgrade base
alembic upgrade head

# Clear pytest cache
pytest --cache-clear

# Run single test in isolation
pytest tests/test_auth.py::test_login -v
```

### Git Issues

**Symptom:** Merge conflicts, detached HEAD, etc.

**Solutions:**
```bash
# Merge conflicts
git status  # See conflicted files
# Edit files, resolve conflicts
git add <resolved-files>
git commit

# Detached HEAD
git checkout main
git branch -D <temp-branch>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Recover deleted branch
git reflog
git checkout -b <branch-name> <commit-sha>
```

### Performance Issues

**Symptom:** Slow API responses, high memory usage

**Solutions:**
```bash
# Profile Python code
python -m cProfile -o profile.stats src/main.py
python -m pstats profile.stats

# Check database query performance
# Enable SQLAlchemy logging
export DATABASE_ECHO=1
python src/main.py

# Monitor memory usage
python -m memory_profiler src/main.py

# Check for N+1 queries
# Use SQLAlchemy query logging

# Add database indexes
# See database slow query log
```

---

## Emergency Procedures

### Production Outage

**Response Timeline:**

**0-5 minutes:**
1. Confirm outage (check health endpoint)
2. Check error logs for cause
3. Alert team via Slack
4. Begin rollback if cause unclear

**5-15 minutes:**
1. Rollback to last known good version
2. Verify rollback successful
3. Update status page
4. Communicate with stakeholders

**15-60 minutes:**
1. Identify root cause
2. Develop hotfix if possible
3. Test hotfix in staging
4. Deploy hotfix to production

**Post-incident:**
1. Write post-mortem
2. Update runbooks
3. Implement preventive measures

**Rollback Command:**
```bash
# Immediate rollback
railway rollback --service myapp-prod

# Or via git
git revert HEAD
git push origin main
```

### Data Loss Event

**Response:**

**Immediate:**
1. Stop all writes to database
2. Snapshot current database state
3. Identify extent of data loss
4. Alert team and stakeholders

**Recovery:**
1. Restore from most recent backup
2. Replay transactions if possible
3. Identify missing data
4. Manual data entry if needed

**Prevention:**
1. Implement point-in-time recovery
2. Increase backup frequency
3. Add data validation checks
4. Review access controls

### Security Incident

**Response:**

**Immediate:**
1. Isolate affected systems
2. Collect evidence (logs, snapshots)
3. Revoke compromised credentials
4. Alert security team

**Investigation:**
1. Determine attack vector
2. Identify affected data
3. Assess damage
4. Document timeline

**Remediation:**
1. Patch vulnerabilities
2. Rotate all secrets
3. Notify affected users
4. Implement additional controls

**Post-incident:**
1. Security audit
2. Update policies
3. Training for team
4. Third-party assessment

---

## Runbook Examples

### Runbook: Deploy to Production

**Prerequisites:**
- [ ] All tests passing in staging
- [ ] PR approved and merged
- [ ] Release notes prepared
- [ ] Team notified of deployment window

**Steps:**
1. Tag release: `git tag -a v1.2.3 -m "Release v1.2.3"`
2. Push tag: `git push origin v1.2.3`
3. Trigger deployment workflow
4. Monitor deployment progress
5. Verify health check: `curl https://api.myapp.com/health`
6. Run smoke tests
7. Monitor error rates for 30 minutes
8. Update release notes in GitHub
9. Notify team of successful deployment

**Rollback Plan:**
If any step fails, run: `railway rollback --service myapp-prod`

---

### Runbook: Database Migration

**Prerequisites:**
- [ ] Migration tested in local environment
- [ ] Migration tested in staging
- [ ] Database backup completed
- [ ] Maintenance window scheduled

**Steps:**
1. Backup production database
2. Set application to read-only mode
3. Run migration: `alembic upgrade head`
4. Verify migration success
5. Run data validation queries
6. Restore application to read-write mode
7. Monitor for errors
8. Update documentation

**Rollback Plan:**
1. Set to read-only
2. Run: `alembic downgrade -1`
3. Restore from backup if needed
4. Restore to read-write

---

## Monitoring & Alerts

### Key Metrics

**Application:**
- Response time (p50, p95, p99)
- Error rate
- Request rate
- Active connections

**Database:**
- Query time
- Connection pool usage
- Slow queries
- Replication lag

**Infrastructure:**
- CPU usage
- Memory usage
- Disk usage
- Network I/O

### Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Response time (p95) | >500ms | >2s |
| Error rate | >1% | >5% |
| CPU usage | >70% | >90% |
| Memory usage | >80% | >95% |
| Disk usage | >80% | >95% |

### Alert Channels

**Critical:**
- PagerDuty (immediate)
- Slack #incidents (immediate)
- Email to on-call (immediate)

**Warning:**
- Slack #monitoring (batched)
- Email digest (hourly)

**Info:**
- Dashboard only
- Weekly summary email

---

## Maintenance Windows

### Scheduled Maintenance

**Frequency:** Monthly (first Sunday, 2-4 AM UTC)

**Activities:**
- Database backups
- Log rotation
- Dependency updates
- Certificate renewals
- Performance tuning

**Communication:**
1. Notify users 7 days in advance
2. Update status page
3. Send reminder 24 hours before
4. Post in-progress update
5. Confirm completion

### Emergency Maintenance

**When needed:**
- Security patches
- Critical bugs
- Data integrity issues

**Process:**
1. Alert stakeholders immediately
2. Update status page
3. Perform maintenance
4. Post-mortem after completion
```

---

## Artifact 7: claude-config.md

**Purpose:** Defines CLAUDE.md structure and maintenance (already documented)  
**Location:** `.ipe/workflow-config/claude-config.md`  
**Lifecycle:** Governed

**See:** [IPE_CLAUDE_Memory_Integration.md](IPE_CLAUDE_Memory_Integration.md) for complete specification

**Summary:** Defines how `.claude/CLAUDE.md` is structured, what context gets loaded, token budget management, import strategy, and automated update mechanisms via hooks.

---

## Stage 4 Workflow

### Artifact Creation Sequence

```
1. Start Stage 4
   └─> Review Stage 3 completion

2. Create claude-config.md
   └─> Define CLAUDE.md structure
   └─> Set token budgets
   └─> Plan import strategy

3. Create claude.md
   └─> Define Claude Code behavior
   └─> Set task completion rules
   └─> Add project context

4. Create agent.md
   └─> Define generic agent behavior
   └─> Mirror claude.md rules (agent-agnostic)
   └─> Add agent-specific instructions

5. Create dev-workflow.md
   └─> Define git workflow
   └─> Set commit standards
   └─> Configure PR process
   └─> Plan deployment

6. Create environment-variants.md
   └─> Define local/staging/production
   └─> Configure secrets management
   └─> Set environment-specific behavior

7. Create context-management.md
   └─> Configure pruning triggers
   └─> Define drift detection
   └─> Set context quality gates

8. Create operations-playbook.md
   └─> Document common workflows
   └─> Add troubleshooting guides
   └─> Define emergency procedures

9. Review all artifacts
   └─> Cross-reference consistency
   └─> Validate completeness
   └─> Check for conflicts

10. Finalize governed artifacts
    └─> dev-workflow.md
    └─> environment-variants.md
    └─> context-management.md
    └─> claude-config.md

11. Generate .claude/CLAUDE.md
    └─> From claude-config.md
    └─> Automated via hooks
```

---

## Stage 4 Completion Criteria

### All Artifacts Created
- [ ] claude.md exists and populated
- [ ] agent.md exists and populated
- [ ] dev-workflow.md finalized
- [ ] environment-variants.md finalized
- [ ] context-management.md finalized
- [ ] operations-playbook.md created (can evolve)
- [ ] claude-config.md finalized

### Governed Artifacts Finalized
- [ ] dev-workflow.md marked as finalized
- [ ] environment-variants.md marked as finalized
- [ ] context-management.md marked as finalized
- [ ] claude-config.md marked as finalized
- [ ] All have version 1.0.0

### CLAUDE.md Generated
- [ ] .claude/CLAUDE.md exists
- [ ] Generated from claude-config.md
- [ ] Imports working correctly
- [ ] Token budget validated (<20K)

### Hooks Configured
- [ ] .claude/settings.json exists
- [ ] SessionStart hook configured
- [ ] Stop hook configured (update CLAUDE.md)
- [ ] SessionEnd hook configured (finalize stage)

### Validation Passed
- [ ] All cross-references valid
- [ ] No conflicting rules
- [ ] Artifact schema compliance
- [ ] Token budgets checked

---

## Integration with Other Stages

### From Stage 3 (Environment Setup)
**Inputs:**
- repo-structure.md (file placement rules)
- environment-config.md (setup approach)
- environment-manifest.json (tools available)

**Usage:**
- Reference in claude.md/agent.md
- Import in CLAUDE.md
- Drift detection baseline

### To Stage 5 (Implementation Planning)
**Outputs:**
- Agent behavior rules (claude.md, agent.md)
- Development process (dev-workflow.md)
- Context management (claude-config.md)
- Operations procedures (operations-playbook.md)

**Usage:**
- Inform task breakdown
- Define execution constraints
- Guide skill/agent selection

---

## Common Mistakes to Avoid

### Don't
❌ Duplicate content between claude.md and CLAUDE.md  
❌ Put implementation details in workflow docs  
❌ Make all artifacts governed (some need to evolve)  
❌ Skip pruning trigger definition  
❌ Ignore token budgets  
❌ Forget to generate CLAUDE.md from claude-config.md  
❌ Confuse claude.md (behavior) with CLAUDE.md (context)

### Do
✅ Keep claude.md concise and focused  
✅ Use imports for detailed content  
✅ Define clear pruning triggers  
✅ Test CLAUDE.md generation  
✅ Validate token usage  
✅ Cross-reference between artifacts  
✅ Distinguish behavior rules from context

---

## Next Steps

1. **Review this specification** - Ensure Stage 4 approach aligns with project needs
2. **Begin artifact creation** - Follow sequence above
3. **Generate CLAUDE.md** - Test automated generation
4. **Configure hooks** - Set up automated maintenance
5. **Validate** - Run compliance checks
6. **Move to Stage 5** - Begin implementation planning

---

## Appendix: Quick Reference

### File Locations
```
.ipe/workflow-config/
├── claude-config.md          ← CLAUDE.md structure definition
├── dev-workflow.md           ← Git, PR, deployment workflow
├── environment-variants.md   ← Environment configurations
├── context-management.md     ← Memory, pruning, drift
└── operations-playbook.md    ← Common tasks, troubleshooting

.claude/
├── claude.md                 ← Claude Code behavior rules
├── CLAUDE.md                 ← Auto-generated context (from claude-config.md)
├── CLAUDE.local.md           ← User overrides (.gitignored)
└── settings.json             ← Hooks configuration

.agent/
└── agent.md                  ← Generic agent configuration
```

### Key Concepts
- **Governed artifacts** - Require change order after finalization
- **Continuous artifacts** - Can evolve, need pruning
- **CLAUDE.md** - Context file (auto-generated)
- **claude.md** - Behavior rules (manually curated)
- **Progressive disclosure** - Layered memory retrieval
- **Drift detection** - Monitoring repo structure compliance

### Validation Commands
```bash
# Validate CLAUDE.md
./.claude/hooks/validate-claude-md.sh

# Check token budget
wc -c .claude/CLAUDE.md | awk '{print $1/4 " tokens"}'

# Detect drift
python scripts/detect-drift.py

# Test hooks
./.claude/hooks/update-claude-md.sh
```
