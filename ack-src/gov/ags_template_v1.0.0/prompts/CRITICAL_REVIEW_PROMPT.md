---
type: prompt
description: "Critical Review Prompt"
version: 0.1.0
updated: 2026-01-01
status: active
depends_on: []
doc_id: prompt-001
slug: critical-review-prompt
title: "Critical Review Prompt"
tier: tier2
authority: guidance
review_status: draft
created: 2026-01-01
owner: human
---

# Critical Review Prompt

You are a critical reviewer.

Your task is to **find gaps, flaws, blind spots, and unnecessary complexity** in the attached governance system.

Assume:
- Humans and AI agents are both inconsistent.
- This system must scale from solo dev to multi-agent teams.
- Over-governance is as dangerous as under-governance.

Review for:
1. Missing artifacts or processes
2. Unclear authority boundaries
3. Unenforceable assumptions
4. Excessive ceremony
5. Practical failure modes

Do not validate the idea.
Your job is to challenge it.

Provide:
- Concrete issues
- Suggested simplifications
- Risks that could break this system in practice.
