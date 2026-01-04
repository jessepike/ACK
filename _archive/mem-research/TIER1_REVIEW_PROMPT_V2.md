# Tier-1 Memory Kit Specification — Review Prompt v2

**Purpose:** Get critical feedback from AI reviewers (ChatGPT, Gemini, Claude instances)  
**Document:** TIER1_KIT_SPEC.md v2.0.0  
**Date:** 2026-01-03

---

## Instructions

1. Copy the prompt below (everything after the line)
2. Send to each AI reviewer
3. Save responses as `TIER1_REVIEW_[agent].md`
4. Synthesize findings

---

## PROMPT (Copy Everything Below This Line)

---

You are a critical systems architect reviewer. Your job is to **find problems**, not validate ideas.

I need you to review a specification for a memory/context management system for AI coding agents. This is Tier-1 of a two-tier memory architecture — the "curated, stable guidance" layer that uses Claude Code's native CLAUDE.md system.

**Your mindset:** Assume I have blind spots. Find what's wrong, what's risky, what will break in practice.

**Be brutally honest.** I don't want encouragement — I want to know what fails under real usage.

---

## Context

**Problem being solved:**
- AI coding agents are stateless — context lost between sessions
- Agents drift from intent without guardrails
- Manual governance doesn't scale at AI generation speed
- Crash mid-session = lost state, unclear where to resume

**This specification defines:**
- Memory file structure (global vs project vs local)
- YAML frontmatter schema
- Commit governance (when to commit)
- Plan/task workflow (how work gets structured)
- Maintenance strategy (pruning stale content)

---

## SPECIFICATION TO REVIEW

[Paste the contents of TIER1_KIT_SPEC.md here]

---

## YOUR REVIEW TASK

Analyze this specification using the EXACT structure below. Do not skip sections. Be specific.

---

# Critical Review: Tier-1 Memory Kit Spec v2.0.0

## Overall Assessment

**Verdict:** [Strong Foundation / Has Potential But Flawed / Needs Major Rework / Fatally Flawed]

**One-sentence summary:** [Your honest take]

---

## What Actually Works

List 2-3 things that are genuinely strong. Be specific about WHY.

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

## Will This Break in Practice?

What will fail when actually used? Think about:
- Agent compliance (will agents actually follow these rules?)
- Crash scenarios (does recovery actually work?)
- Scale (what happens with 50+ tasks? 10+ phases?)
- Edge cases

### Breakage 1:
**Scenario:**  
**Why it breaks:**  
**Mitigation:**

### Breakage 2:
**Scenario:**  
**Why it breaks:**  
**Mitigation:**

---

## Unvalidated Assumptions

| Assumption | Risk Level | Why It Might Be Wrong |
|------------|------------|----------------------|
| | High/Med/Low | |
| | | |

---

## Governance Holes

Where can this system be bypassed or corrupted?

1. 
2. 
3. 

---

## Complexity vs Value

Is any part over-engineered for a solo dev workflow?

| Component | Complexity | Value | Verdict |
|-----------|------------|-------|---------|
| Frontmatter schema | | | Keep/Simplify/Cut |
| Plan structure | | | Keep/Simplify/Cut |
| Commit governance | | | Keep/Simplify/Cut |
| Static/dynamic sections | | | Keep/Simplify/Cut |
| Type vocabulary | | | Keep/Simplify/Cut |

---

## Questions I'd Ask the Author

1. 
2. 
3. 
4. 
5. 

---

## Recommended Changes (Priority Order)

1. **[Critical]:** 
2. **[Important]:** 
3. **[Nice-to-have]:** 

---

## Confidence Level

**How confident are you in this review?** [High / Medium / Low]

**What would increase your confidence?** 

---

**END OF REVIEW TEMPLATE**

---

**END OF PROMPT**
