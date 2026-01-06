---
type: artifact
stage: setup
artifact: ci-cd
description: "Continuous integration and deployment pipeline configuration"
version: "1.0.0"
status: draft
---

# [Project Name] - CI/CD Configuration

## Pipeline Overview

- **Platform:** [GitHub Actions / GitLab CI / CircleCI / etc]
- **Trigger Strategy:** [Push / PR / Scheduled / Manual]
- **Deployment Target:** [Vercel / Railway / AWS / etc]

---

## Environments

| Environment | Branch | URL | Auto-Deploy |
|-------------|--------|-----|-------------|
| Development | `develop` | [dev-url] | Yes |
| Staging | `staging` | [staging-url] | Yes |
| Production | `main` | [prod-url] | [Yes/No - Manual] |

---

## Pipeline Stages

### 1. Build

```yaml
# Build stage configuration
steps:
  - Install dependencies
  - Compile/transpile
  - Generate artifacts
```

**Triggers:** [When this stage runs]

### 2. Test

```yaml
# Test stage configuration
steps:
  - Unit tests
  - Integration tests
  - Linting
  - Type checking
```

**Triggers:** [When this stage runs]

### 3. Deploy

```yaml
# Deploy stage configuration
steps:
  - Build production assets
  - Deploy to target environment
  - Run smoke tests
  - Notify team
```

**Triggers:** [When this stage runs]

---

## Workflow Files

### Primary CI Workflow

```yaml
# .github/workflows/ci.yml (or equivalent)
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup [runtime]
        uses: [setup-action]
      - name: Install dependencies
        run: [install-command]
      - name: Run tests
        run: [test-command]
      - name: Build
        run: [build-command]
```

### Deployment Workflow

```yaml
# .github/workflows/deploy.yml (or equivalent)
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to [environment]
        run: [deploy-command]
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

---

## Secrets & Environment Variables

### Required Secrets

| Secret | Purpose | Where to Set |
|--------|---------|--------------|
| `[SECRET_1]` | [Purpose] | Repository settings |
| `[SECRET_2]` | [Purpose] | Repository settings |
| `[DEPLOY_TOKEN]` | [Deployment authentication] | Repository settings |

### Environment Variables

| Variable | Value | Environment |
|----------|-------|-------------|
| `[VAR_1]` | [value] | All |
| `[VAR_2]` | [value] | Production only |

---

## Quality Gates

### Required Checks Before Merge

- [ ] All tests pass
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Code coverage >= [X]%
- [ ] Build succeeds
- [ ] [Additional checks]

### Notifications

| Event | Channel | Recipients |
|-------|---------|------------|
| Build failure | [Slack/Email/etc] | [Team/Individual] |
| Deploy success | [Channel] | [Recipients] |
| Deploy failure | [Channel] | [Recipients] |

---

## Rollback Strategy

### Automatic Rollback
- [ ] Enabled/Disabled
- **Trigger:** [Conditions that trigger rollback]
- **Target:** [Previous version / specific version]

### Manual Rollback

```bash
# Rollback procedure
[rollback-commands]
```

---

## Caching Strategy

| Cache | Key | Paths |
|-------|-----|-------|
| Dependencies | [hash of lockfile] | `node_modules/` |
| Build cache | [cache-key] | `.next/cache/` |

---

## Setup Checklist

### Phase 1: Basic CI
- [ ] Create workflow file(s)
- [ ] Configure triggers
- [ ] Add build step
- [ ] Add test step

### Phase 2: Secrets
- [ ] Add required secrets to repository
- [ ] Verify secrets are accessible

### Phase 3: Deployment
- [ ] Configure deployment target
- [ ] Set up environment-specific configs
- [ ] Test deployment pipeline

### Phase 4: Quality Gates
- [ ] Configure required status checks
- [ ] Set up notifications
- [ ] Document rollback procedure

---

## Open Questions

- [ ] [CI/CD question 1]
- [ ] [CI/CD question 2]
