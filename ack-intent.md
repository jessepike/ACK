---
type: "intent"
description: "North Star outcome and success criteria for ACK"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# Agent Context Kit (ACK) Intent

## The Problem

AI agents are stateless, fast, and drift-prone. They lose context between sessions, diverge from original intent without realizing it, and generate code faster than humans can review. The human becomes the bottleneck—the only keeper of context, the only validator, the only brake on a system moving too fast to govern manually.

## The Outcome

A structured workflow that captures human intent in machine-readable artifacts, persists context across sessions, orchestrates agents, and automates drift detection. Agents work within guardrails, humans direct. Quality scales with velocity.

## Success Criteria

- **Zero re-explanation tax**: Sessions start with full context automatically loaded
- **Drift caught early**: Divergence flagged during generation, not after deployment
- **Artifacts as specification**: Planning documents are executable by AI, not just readable by humans
- **Reusable patterns**: Each project improves the system; templates propagate consistency and learning

## Constraints

- **File-first**: Artifacts are markdown + YAML, version-controlled with git
- **Incremental adoption**: Each stage must be independently usable and interelated
- **Solo developer optimized**: Built for one person managing multiple projects, not teams

## Non-Negotiables

- **Context is explicit**: No implicit knowledge. If an agent needs it, it's written down.
- **Governance is automated**: Validation scripts enforce rules. Humans make decisions, not check boxes.
- **Memory persists**: What was decided, why it was decided, and what was rejected—all captured.
- **Stages are sequential**: You don't skip Discovery to jump to Implementation.
