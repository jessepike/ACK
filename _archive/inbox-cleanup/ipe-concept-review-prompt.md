# IPE Concept Review - Prompt Package

**Purpose:** Get critical feedback from multiple AI agents (ChatGPT, Gemini, etc.)  
**Document:** concept.md (IPE - Integrated Planning Environment)  
**Date:** 2025-01-01

---

## Instructions

1. Copy the prompt below
2. Attach/paste concept.md content after the prompt
3. Send to each AI agent (ChatGPT, Gemini, Claude, etc.)
4. Save each response as `review-[agent-name].md`
5. Synthesize findings after all reviews complete

---

## PROMPT (Copy Everything Below This Line)

---

You are a critical product reviewer. Your job is to **find problems**, not validate ideas. I need you to tear apart this concept document for a developer tool called IPE (Integrated Planning Environment).

**Your mindset:** Assume I have blind spots. Assume I'm too close to this. Find what I'm missing.

**Be brutally honest.** I don't want encouragement—I want to know what's wrong, what's risky, and what could kill this idea before I invest months building it.

---

## Document to Review

[CONCEPT.MD CONTENT WILL BE PASTED BELOW]

---

## Your Review Task

Analyze this concept document and respond using the EXACT structure below. Do not skip sections. Be specific—vague feedback is useless.

---

# Critical Review: IPE Concept

## Overall Assessment

**Verdict:** [Strong Foundation / Has Potential But Flawed / Needs Major Rework / Fatally Flawed]

**One-sentence summary:** [Your honest take in one sentence]

---

## What Actually Works

List 2-3 things that are genuinely strong. Be specific about WHY they work.

- 
- 
- 

---

## Critical Gaps

What's missing that should be here? What questions does this document fail to answer?

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

Where does the document contradict itself or make claims that don't hold up?

- 
- 
- 

---

## Unvalidated Assumptions

What is this document assuming to be true that might not be? List assumptions and rate risk.

| Assumption | Risk Level | Why It Might Be Wrong |
|------------|------------|----------------------|
| | High/Med/Low | |
| | | |
| | | |

---

## Technical Feasibility Concerns

What might be harder to build than the document implies? What technical risks aren't acknowledged?

1. 
2. 
3. 

---

## Market/Adoption Risks

Why might developers NOT use this even if it works? What adoption barriers exist?

1. 
2. 
3. 

---

## What Could Kill This

If this project fails, what's the most likely reason? List the top 3 existential risks.

1. **Risk:** 
   **Likelihood:** [High/Medium/Low]
   **Mitigation idea:**

2. **Risk:**
   **Likelihood:**
   **Mitigation idea:**

3. **Risk:**
   **Likelihood:**
   **Mitigation idea:**

---

## Competitive Blind Spots

What competitors or alternative approaches does this document ignore or underestimate?

- 
- 

---

## Scope Concerns

Is the scope too big? Too small? What should be cut? What's missing?

**Too ambitious (cut these):**
- 
- 

**Missing (add these):**
- 
- 

---

## Clarity Issues

Where is the document confusing, vague, or using jargon that won't land?

| Section | Issue | Suggested Rewrite |
|---------|-------|-------------------|
| | | |
| | | |

---

## Questions You'd Ask the Author

If you could interrogate the person who wrote this, what would you ask? (These reveal gaps in thinking)

1. 
2. 
3. 
4. 
5. 

---

## Recommended Next Steps

Based on your review, what should the author do BEFORE building anything?

1. 
2. 
3. 

---

## Confidence Level

**How confident are you in this review?** [High / Medium / Low]

**What would increase your confidence?** [What additional info would help]

---

## END OF REVIEW TEMPLATE

---

## CONCEPT.MD CONTENT

[PASTE THE FULL CONCEPT.MD CONTENT HERE]

---

**END OF PROMPT**

---

## After Reviews Complete

Once you have 2-3 reviews from different agents:

1. Create `review-synthesis.md`
2. Look for patterns—what do multiple reviewers flag?
3. Prioritize: Critical issues (all agree) → Important (2+ agree) → Consider (1 flags)
4. Update concept.md with fixes
5. Optionally: Run another review round on v2

---

## Quick Reference: What to Send Where

| Agent | Best For | Notes |
|-------|----------|-------|
| ChatGPT-4 | Market/product critique | Good at user perspective |
| Gemini | Technical feasibility | Strong on implementation concerns |
| Claude | Logical consistency | Good at finding contradictions |
| Perplexity | Competitive analysis | Can search for actual competitors |

---

## Version History

- v1.0 - Initial prompt package (2025-01-01)
