---
doc_id: "prompt-mem-001"
title: "Tier-1 Memory Kit Spec Review Prompt"
type: "prompt"
status: "active"
version: "1.0.0"
owner: "human"
created: "2026-01-02"
updated: "2026-01-02"
---

# Tier-1 Memory Kit Specification Review

**Purpose:** Get critical feedback from AI agents on the Tier-1 Memory Kit specification  
**Target Document:** `TIER1_KIT_SPEC.md`  
**Date:** 2026-01-02

---

## Instructions

1. Copy the prompt below
2. Attach/paste `TIER1_KIT_SPEC.md` content after the prompt
3. Send to each AI agent (ChatGPT, Gemini, Claude, etc.)
4. Save each response as `review-tier1-[agent-name].md`
5. Synthesize findings after all reviews complete

---

## PROMPT (Copy Everything Below This Line)

---

You are a senior software architect specializing in developer tooling, AI agent systems, and configuration management. Your job is to **critically review** this specification for flaws, gaps, and risks.

**Context:** This spec defines a "Tier-1 Memory Kit" — a structured approach to Claude Code's native memory system (CLAUDE.md files + rules/ directories). The goal is to provide curated, stable guidance that persists across AI coding sessions: conventions, invariants, preferences, and workflow rules.

**Your mindset:** Assume the author has blind spots. Find what's missing, what won't work in practice, and what will cause problems at scale.

**Be specific.** Vague feedback is useless. Point to exact sections, propose concrete fixes.

---

## Document to Review

[TIER1_KIT_SPEC.md CONTENT WILL BE PASTED BELOW]

---

## Your Review Task

Analyze this specification and respond using the EXACT structure below. Do not skip sections.

---

# Critical Review: Tier-1 Memory Kit Specification

## Overall Assessment

**Verdict:** [Strong Foundation / Has Potential But Flawed / Needs Major Rework / Fatally Flawed]

**One-sentence summary:** [Your honest take]

---

## What Works Well

List 2-3 genuinely strong aspects. Be specific about WHY they work.

1. 
2. 
3. 

---

## Critical Gaps

What's missing that should be here?

### Gap 1: [Name]
**What's missing:**  
**Why it matters:**  
**Suggested fix:**

### Gap 2: [Name]
**What's missing:**  
**Why it matters:**  
**Suggested fix:**

### Gap 3: [Name]
**What's missing:**  
**Why it matters:**  
**Suggested fix:**

---

## Logical Inconsistencies

Where does the spec contradict itself or make claims that don't hold up?

| Section | Inconsistency | Suggested Resolution |
|---------|---------------|---------------------|
| | | |
| | | |

---

## Practical Concerns

What will break or cause friction when actually used?

### Concern 1: [Name]
**The problem:**  
**When it will surface:**  
**Mitigation:**

### Concern 2: [Name]
**The problem:**  
**When it will surface:**  
**Mitigation:**

---

## Governance Model Review

Specifically evaluate the governance approach:

| Aspect | Assessment | Issue (if any) |
|--------|------------|----------------|
| Who can modify global | | |
| Who can modify project | | |
| Version increment rules | | |
| Change tracking approach | | |
| Enforcement mechanisms | | |

**Overall governance verdict:** [Too Strict / About Right / Too Loose / Unclear]

---

## Schema/Frontmatter Review

Evaluate the proposed YAML frontmatter schema:

| Field | Necessary? | Issue (if any) |
|-------|------------|----------------|
| doc_id | | |
| title | | |
| type | | |
| status | | |
| version | | |
| owner | | |
| created | | |
| updated | | |
| paths (optional) | | |
| depends_on (optional) | | |

**Missing fields that should exist:**
- 

**Fields that should be removed:**
- 

---

## Token Budget Analysis

The spec claims these budgets:
- Global: ~2,000 tokens
- Project rules: ~5,000 tokens  
- Local: ~1,000 tokens
- Total target: ~20,000 tokens

**Is this realistic?** [Yes / No / Uncertain]

**Concerns:**
- 

---

## Scalability Assessment

How will this approach hold up as:

| Scenario | Assessment | Risk Level |
|----------|------------|------------|
| Projects grow larger | | High/Med/Low |
| More rules accumulate | | |
| Team size increases | | |
| Cross-project sharing needed | | |
| Agent autonomy increases | | |

---

## Alternative Approaches

What alternative designs should be considered?

### Alternative 1: [Name]
**Approach:**  
**Pros:**  
**Cons:**  
**When better:**

### Alternative 2: [Name]
**Approach:**  
**Pros:**  
**Cons:**  
**When better:**

---

## Questions for the Author

If you could interrogate the person who wrote this, what would you ask?

1. 
2. 
3. 
4. 
5. 

---

## Recommended Changes

Prioritized list of changes before implementation:

### Must Fix (Blockers)
1. 
2. 

### Should Fix (Important)
1. 
2. 

### Could Fix (Nice to Have)
1. 
2. 

---

## Comparison to Industry Patterns

How does this compare to similar systems you're aware of?

| System/Pattern | Similarity | What This Spec Could Learn |
|----------------|------------|---------------------------|
| | | |
| | | |

---

## Confidence Level

**How confident are you in this review?** [High / Medium / Low]

**What additional context would improve your review?**
- 

---

## END OF REVIEW TEMPLATE

---

## TIER1_KIT_SPEC.md CONTENT

[PASTE THE FULL TIER1_KIT_SPEC.md CONTENT HERE]

---

**END OF PROMPT**

---

## After Reviews Complete

Once you have 2-3 reviews from different agents:

1. Create `review-tier1-synthesis.md`
2. Look for patterns — what do multiple reviewers flag?
3. Prioritize: Critical (all agree) → Important (2+ agree) → Consider (1 flags)
4. Update `TIER1_KIT_SPEC.md` with fixes
5. Optionally: Run another review round on v2

---

## Quick Reference: Model Strengths

| Agent | Best For | Notes |
|-------|----------|-------|
| Claude Opus | Logical consistency, governance | Strong on structure |
| ChatGPT-4 | Practical concerns, user experience | Good at "what breaks" |
| Gemini | Technical feasibility, alternatives | Strong on implementation |
| Perplexity | Industry comparisons | Can search for patterns |

---

## Review & Change History

**Current Version:** 1.0.0
**Review Status:** accepted

### Changes Since Last Review
- Initial creation
