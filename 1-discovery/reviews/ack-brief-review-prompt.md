---
type: "review"
description: "External review prompt for ACK Project Brief"
version: "1.0.0"
updated: "2026-01-03T00:00:00"
---

# ACK Project Brief - External Review Prompt

## Instructions for Reviewer

You are being asked to critically review a project brief for **ACK (Agent Context Kit)** - a meta-project for managing AI agent context in software development.

Please provide honest, constructive criticism. The goal is to find gaps, contradictions, unclear areas, and potential problems BEFORE implementation begins.

---

## Your Review Should Address

### 1. Problem Validation
- Is the problem clearly defined?
- Does the problem resonate as genuine and significant?
- Are there aspects of the problem that are overlooked or understated?
- Is the root cause correctly identified?

### 2. Solution Coherence
- Does the solution actually address the stated problem?
- Are there simpler alternatives that weren't considered?
- What could go wrong with this approach?
- Are there hidden assumptions that should be explicit?

### 3. Scope & Feasibility
- Is the MVP scope realistic for a solo developer?
- Is anything critical missing from MVP that will cause problems later?
- Is anything in MVP that should be deferred?
- Are the constraints reasonable or artificially limiting?

### 4. Conceptual Clarity
- Are terms used consistently throughout?
- Is the artifact hierarchy clear and logical?
- Does the stage model make sense as a workflow?
- Would a new reader understand this without explanation?

### 5. Risks & Blind Spots
- What are the biggest risks to this project's success?
- What hasn't been considered that should be?
- Where might this approach fail in practice?
- What would cause you to abandon this approach?

### 6. Overall Assessment
- What's the strongest aspect of this brief?
- What's the weakest aspect that needs the most work?
- Would you invest time in building this? Why or why not?

---

## The Project Brief

[PASTE THE CONTENTS OF ack-project-brief.md BELOW THIS LINE]

---

## Context (Optional Background)

**What ACK is trying to solve:**
AI coding agents (Claude Code, Cursor, Copilot) are ephemeral - they start fresh each session with no memory of previous work. This creates problems:
- Re-explaining context every session
- Agents drifting from original intent without realizing
- No consistent structure across projects
- Human becomes bottleneck for context management

**The author's situation:**
- Solo developer managing multiple AI-assisted projects
- Heavy user of Claude Code
- Frustrated by context loss and drift
- Building ACK to solve their own problem first, then share

**What success looks like:**
- Sessions start with context pre-loaded
- Drift detected early, not after deployment
- Reusable patterns across projects
- Higher quality at higher velocity

---

## Response Format

Please structure your review with clear headers matching the sections above. Be direct - diplomatic hedging is less useful than clear critique. If something is good, say so briefly and move on. Spend more words on problems and suggestions.
