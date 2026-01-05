---
type: artifact
stage: setup
artifact: ci-cd
description: "CI/CD pipeline configuration (support artifact)"
version: 1.0.0
updated: "YYYY-MM-DDTHH:MM:SS"
status: draft
---

# [Project Name] - CI/CD Configuration

## Purpose

<!-- Document CI/CD pipeline setup and configuration -->

This document captures the continuous integration and deployment pipeline configuration for [Project Name].

**CI/CD Platform:** [GitHub Actions / GitLab CI / CircleCI / etc.]

**Deployment Target:** [Vercel / Railway / AWS / etc.]

---

## Pipeline Overview

### Trigger Events

| Event | Branches | Actions |
|-------|----------|---------|
| Push | `main` | Build, Test, Deploy to production |
| Push | `develop` | Build, Test, Deploy to staging |
| Pull Request | `*` | Build, Test, Lint |
| Manual | `main` | Deploy to production |

### Pipeline Stages

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Lint   │───▶│  Build  │───▶│  Test   │───▶│ Deploy  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## GitHub Actions Configuration

### Main Workflow

**File:** `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  # Add other environment variables

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  build:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  deploy-staging:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
      - uses: actions/checkout@v4
      # Add deployment steps

  deploy-production:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4
      # Add deployment steps
```

---

### PR Checks Workflow

**File:** `.github/workflows/pr-checks.yml`

```yaml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
      - name: Check coverage threshold
        run: |
          # Add coverage threshold check
```

---

## Environment Configuration

### Secrets Required

| Secret | Used In | Purpose |
|--------|---------|---------|
| `DEPLOY_TOKEN` | Deploy jobs | Authentication for deployment |
| `DATABASE_URL` | Test/Deploy | Database connection string |
| [Secret name] | [Where used] | [Purpose] |

### Environment Variables

| Variable | Staging | Production |
|----------|---------|------------|
| `NODE_ENV` | staging | production |
| `API_URL` | [staging URL] | [production URL] |
| [Variable] | [Value] | [Value] |

---

## Deployment Configuration

### Staging Environment

**URL:** [Staging URL]

**Deploy trigger:** Push to `develop` branch

**Configuration:**
- [Config item 1]
- [Config item 2]

### Production Environment

**URL:** [Production URL]

**Deploy trigger:** Push to `main` branch

**Configuration:**
- [Config item 1]
- [Config item 2]

---

## Platform-Specific Setup

### Vercel

**File:** `vercel.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": null,
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/$1" }
  ]
}
```

### Railway

**File:** `railway.toml`

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Docker

**File:** `Dockerfile`

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Quality Gates

### Required Checks

| Check | Blocking | Threshold |
|-------|----------|-----------|
| Lint | Yes | No errors |
| Type check | Yes | No errors |
| Unit tests | Yes | All pass |
| Coverage | Yes | [X]% minimum |
| Build | Yes | Successful |

### Branch Protection Rules

**main branch:**
- [ ] Require pull request reviews (1 approval)
- [ ] Require status checks to pass
- [ ] Require branches to be up to date
- [ ] No direct pushes

**develop branch:**
- [ ] Require status checks to pass
- [ ] Allow direct pushes from maintainers

---

## Notifications

### Build Notifications

| Event | Channel | Recipients |
|-------|---------|------------|
| Build failure | [Slack/Email/etc.] | [Team/individuals] |
| Deploy success | [Channel] | [Recipients] |
| Deploy failure | [Channel] | [Recipients] |

---

## Monitoring

### Health Checks

| Endpoint | Expected | Frequency |
|----------|----------|-----------|
| `/health` | 200 OK | Every 30s |
| `/api/health` | 200 OK | Every 30s |

### Post-Deploy Verification

- [ ] Health endpoint responds
- [ ] Critical API endpoints work
- [ ] Database connectivity confirmed
- [ ] External integrations functional

---

## Rollback Procedures

### Automatic Rollback

**Trigger:** Health check failure within 5 minutes of deploy

**Action:** Revert to previous deployment

### Manual Rollback

```bash
# Via deployment platform
[Platform-specific rollback command]

# Via git
git revert HEAD
git push origin main
```

---

## CI/CD Checklist

### Initial Setup

- [ ] CI platform account created
- [ ] Repository connected
- [ ] Secrets configured
- [ ] Environments created (staging, production)

### Pipeline Configured

- [ ] Lint job works
- [ ] Build job works
- [ ] Test job works
- [ ] Deploy jobs configured

### Quality Gates

- [ ] Branch protection enabled
- [ ] Required checks configured
- [ ] Coverage thresholds set

### Monitoring

- [ ] Notifications configured
- [ ] Health checks working
- [ ] Rollback tested

---

## Related Documents

- [repo-init.md](repo-init.md) - Repository setup
- [testing.md](testing.md) - Test strategy
- [git-workflow.md](git-workflow.md) - Branch strategy
