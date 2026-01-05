---
type: prompt
stage: discover
prompt: review
description: "Content analysis prompt for Discover stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Discover Stage Review

Review the brief for content quality, clarity, and completeness of thinking.

## Instructions

You are reviewing a project brief to assess whether it's ready to advance to the Design stage. Focus on the **quality of thinking**, not just whether sections exist.

Read the brief carefully, then evaluate each area below.

---

## Review Criteria

### 1. Problem Clarity

- [ ] **Problem is specific:** Can state the problem in one clear sentence
- [ ] **Problem is validated:** Evidence provided that problem exists (not assumed)
- [ ] **Users identified:** Clear who has this problem and how it affects them
- [ ] **Timing justified:** Reason given for why this problem matters now

**Questions to answer:**
- Could someone unfamiliar with this domain understand the problem?
- Is the problem statement focused (not a laundry list)?
- Is there evidence beyond "I think this is a problem"?

---

### 2. Solution Fit

- [ ] **Solution addresses problem:** Clear connection between problem and proposed solution
- [ ] **Differentiation clear:** Explained why this approach vs. alternatives
- [ ] **Capabilities justified:** Each capability links to a problem being solved
- [ ] **Not over-scoped:** Solution sized appropriately for the problem

**Questions to answer:**
- Does the solution actually solve the stated problem?
- Is the differentiation genuine or hand-wavy?
- Are we building features that don't connect to stated problems?

---

### 3. Scope Definition

- [ ] **MVP is minimal:** Scope is the smallest thing that solves the core problem
- [ ] **Boundaries clear:** Obvious what's in vs. out of scope
- [ ] **Deferrals reasoned:** Out-of-scope items have clear rationale
- [ ] **Non-goals explicit:** Things that might seem related are explicitly excluded

**Questions to answer:**
- Could the MVP be smaller and still be valuable?
- Are there scope items that don't tie to success criteria?
- Will someone reading this know exactly what we're NOT building?

---

### 4. Success Criteria

- [ ] **Measurable:** Success criteria can be objectively evaluated
- [ ] **Achievable:** Criteria are realistic for the stated scope
- [ ] **Relevant:** Criteria connect to the problem being solved
- [ ] **Prioritized:** Clear which outcomes are must-have vs. nice-to-have

**Questions to answer:**
- Could we argue about whether success was achieved? (Bad - too vague)
- Are we measuring the right things (outcomes) vs. vanity metrics?
- Do must-haves actually represent the minimum bar?

---

### 5. Risk Awareness

- [ ] **Key risks identified:** Major things that could derail the project
- [ ] **Honest assessment:** Likelihood and impact ratings seem realistic
- [ ] **Mitigations actionable:** Not just "hope it doesn't happen"
- [ ] **Assumptions tracked:** Key assumptions are explicit with validation status

**Questions to answer:**
- Are there obvious risks not mentioned?
- Are mitigations real actions or wishful thinking?
- Are high-risk unvalidated assumptions acceptable?

---

### 6. Overall Coherence

- [ ] **Story holds together:** Problem → Solution → Scope → Success flows logically
- [ ] **No contradictions:** Scope matches success criteria, risks match constraints
- [ ] **Appropriate depth:** Detail level matches project complexity
- [ ] **Ready for Design:** Enough clarity to make technical decisions

**Questions to answer:**
- Does reading this give confidence in the direction?
- Are there gaps that would block technical design?
- Would a new team member understand what we're building and why?

---

## Review Output

### Summary

| Area | Rating | Notes |
|------|--------|-------|
| Problem Clarity | Strong / Adequate / Weak | [Key observation] |
| Solution Fit | Strong / Adequate / Weak | [Key observation] |
| Scope Definition | Strong / Adequate / Weak | [Key observation] |
| Success Criteria | Strong / Adequate / Weak | [Key observation] |
| Risk Awareness | Strong / Adequate / Weak | [Key observation] |
| Overall Coherence | Strong / Adequate / Weak | [Key observation] |

### Strengths

- [What's working well]
- [What's working well]

### Issues to Address

| Issue | Severity | Recommendation |
|-------|----------|----------------|
| [Issue 1] | Blocking / Important / Minor | [How to fix] |
| [Issue 2] | Blocking / Important / Minor | [How to fix] |

### Verdict

**[ ] Ready to advance** - Brief is solid, proceed to Design stage

**[ ] Revise and re-review** - Address issues above, then review again

**[ ] Needs significant work** - Fundamental gaps require rethinking

---

## Notes

- This review focuses on **content quality**, not format/structure
- A brief can pass structural validation but fail content review
- "Adequate" means good enough to proceed, not that it's perfect
- Blocking issues must be resolved before advancing
