---
doc_id: "cmd-001"
slug: "railway-debug"
title: "Railway Debug Command"
type: "command"
tier: "tier2"
status: "active"
authority: "guidance"
version: "0.1.0"
review_status: "draft"
created: "2026-01-01"
updated: "2026-01-01"
owner: "human"
depends_on: ["agent-001", "skill-001", "tool-001"]
triggers:
  - /railway-debug
  - railway deploy failing
  - railway deployment failed
  - railway not working
---

# Railway Debug Command

Diagnose and fix Railway deployment issues.

## Workflow

1. **Activate** Railway Expert agent
2. **Load** railway skill
3. **Gather** status and logs via MCP
4. **Analyze** against known failure patterns
5. **Fix** with specific changes
6. **Verify** deployment succeeds

## Execution Steps

### Step 1: Check MCP Connection
Verify Railway MCP is connected and accessible.

### Step 2: Get Deployment Status
```
List recent deployments
Identify failed deployment
Get deployment ID
```

### Step 3: Pull Logs
```
Get build logs if build failed
Get runtime logs if runtime failed
```

### Step 4: Analyze
Match error patterns:
- Build: deps, runtime version, memory
- Runtime: port binding, DB connection, health check
- Network: DNS, SSL, service discovery

### Step 5: Apply Fix
Provide specific fix with code/config changes.

### Step 6: Verify
Trigger redeploy, confirm success.

## Output Format

```markdown
## Railway Debug Report

**Service:** {name}
**Deployment ID:** {id}
**Status:** {failed|crashed|unhealthy}

### Failure Analysis
{what went wrong}

### Log Snippet
```
{relevant 10-20 lines}
```

### Fix Applied
{specific change made}

### Verification
{deployment status after fix}
```

---

## Review & Change History

**Current Version:** 0.1.0
**Review Status:** draft

### Changes Since Last Review
- Initial creation
