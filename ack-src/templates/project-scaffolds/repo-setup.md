---
type: template
description: "Repo Standards (Solo Dev)"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Repo Standards (Solo Dev)

## running cookie cutter project setups
cd <project_slug>
make setup
make dev

--------------------------------

## Example
# Commands you’ll actually run (example)

cd ~/code/clients/dowell/sites
cookiecutter /path/to/cookiecutter-solo-dev
# choose node_nextjs_app, slug dowell-therapy-site

cd ~/code/clients/dowell/apps
cookiecutter /path/to/cookiecutter-solo-dev
# choose node_nextjs_app, slug dowell-therapy-portal

cd ~/code/clients/dowell/agents
cookiecutter /path/to/cookiecutter-solo-dev
# choose python_fastapi_api, slug dowell-automation

# Use one cookiecutter run per repo. For Do Well Therapy you’ll run it 3+ times.

1) Public website (Next.js)
	•	project_type: node_nextjs_app
	•	project_slug: dowell-therapy-site
	•	project_name: Do Well Therapy

2) Staff portal (Next.js)
	•	project_type: node_nextjs_app
	•	project_slug: dowell-therapy-portal
	•	project_name: Do Well Therapy – Staff Portal

3) Agents (pick based on what you’re actually building)

If you want Python agents (FastAPI optional)
	•	project_type: python_fastapi_api
	•	project_slug: dowell-automation
	•	project_name: Do Well Therapy – Automation

---------------------------------------

## Required in every repo
- README.md (what, how to run, how to deploy)
- Makefile: setup/test/lint/dev/build/deploy
- .env.example (no secrets)
- version pins (.node-version/.python-version)
- CI workflow (lint + test + build)

## Default repo structure
- .github/workflows/
- docs/ (architecture, decisions, runbooks, inbox, summaries, tmp)
- infra/
- scripts/
- src/
- tests/
- config/
- public/ (if applicable)

## ADRs
- docs/decisions/0001-<topic>.md

## Security & secrets
- secrets never in git
- platform env vars or secret manager
- dependency updates automated

## Enterprise-class add-ons
- docs/threat-model/
- docs/sla-slo/
- observability/
- security/

## Naming Tips
If a computer touches it → slug
If a human reads it     → project name
If Git hosts it         → repo name (match slug)
If macOS stores it      → directory (match slug)