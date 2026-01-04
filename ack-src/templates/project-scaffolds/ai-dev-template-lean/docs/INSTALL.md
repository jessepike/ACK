---
type: template
description: "Install Requirements (Lean)"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# Install Requirements (Lean)

brew bundle

cd python && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

cd node && pnpm install && pnpm dev
