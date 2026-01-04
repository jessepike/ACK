# READY TO PASTE - IPE Concept Review Prompt

**Instructions:** Copy everything below the line and paste directly into ChatGPT, Gemini, or other AI.

---

You are a critical product reviewer. Your job is to **find problems**, not validate ideas. I need you to tear apart this concept document for a developer tool called IPE (Integrated Planning Environment).

**Your mindset:** Assume I have blind spots. Assume I'm too close to this. Find what I'm missing.

**Be brutally honest.** I don't want encouragement—I want to know what's wrong, what's risky, and what could kill this idea before I invest months building it.

---

## Document to Review

# Project Concept: IPE

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
---

## What Is It?

IPE (Integrated Planning Environment) is the translation layer between human intent and AI execution. It captures your ideas in structured, versioned artifacts that AI coding agents can actually consume—providing the context, guardrails, and governance that stateless agents can't maintain themselves.

The tool provides a 5-stage workflow: Discovery → Solution Design → Environment Setup → Workflow Configuration → Implementation Planning. Each stage produces versioned artifacts that serve as the single source of truth for your project. Critical documents are hashed and require formal change orders to modify. Drift detectors monitor for divergence between what was planned and what's being built—catching misalignment early before it compounds. An embedded chat interface lets you collaborate with AI agents who can read, validate, and update your planning documents while respecting governance boundaries.

What makes IPE different: AI coding agents are remarkably good at writing code and following instructions, but they lack persistent memory and drift without guardrails. The human becomes the bottleneck—the only one holding context, the only validator, the only brake on a system that moves faster than humans can absorb. IPE solves this by capturing clear human intent in structured artifacts, then providing the context injection, orchestration, and governance mechanisms that keep agents aligned. The planning isn't just for you—it's the executable specification that AI agents will operate within.


## Problem Being Solved

AI coding agents are powerful but stateless. They excel at generating code from instructions, but they don't remember previous sessions, don't track evolving decisions, and will confidently drift from your original intent without realizing it. The human developer becomes the sole keeper of context—manually re-explaining the project, catching misalignment, and course-correcting repeatedly.

Meanwhile, these agents work *fast*. They generate code faster than humans can review, absorb, and validate. Without structure, you're either slowing everything down with constant manual oversight or letting quality slip as drift compounds undetected. The asymmetry between agent execution speed and human comprehension speed is unsustainable.

**Key pain points:**

- **Context loss between sessions.** You spend 20 minutes re-explaining project context to AI agents every time you start working. Previous decisions, rejected alternatives, and rationale disappear into chat history. The agent has no "project brain" to query.

- **Agent drift without guardrails.** AI agents follow the instruction in front of them, not the broader intent behind it. Small deviations compound. By the time you notice the implementation has strayed, you're deep in refactoring.

- **No single source of truth.** Planning happens in scattered docs, chat transcripts, and mental models. When an agent asks "what's the architecture?" there's no canonical answer—just fragments you have to reassemble and explain.

- **Speed mismatch.** Agents can produce in minutes what takes humans hours to properly review. You can't maintain quality at AI velocity without systematic validation—and right now, you *are* the system.

- **Manual governance is exhausting.** You're the only validator. Every PR, every generated file needs human review to catch drift. There's no systematic way to check "does this still match what we planned?"

- **No handoff protocol.** When planning is "done," there's no structured export to implementation. Agents can't programmatically consume your intent—they just get whatever context you remember to paste.


## Core Features

### Structured Artifact System

All planning outputs follow consistent schemas with YAML frontmatter, typed sections, and machine-readable structure. Artifacts are version-controlled with full history. Critical documents can be locked, requiring formal change orders to modify. This isn't documentation for humans to read—it's specification for agents to execute within.

### Context Injection Engine

Agents receive relevant project context automatically based on what they're working on. No more copy-pasting background. The system maintains a persistent "project brain" that agents can query, ensuring continuity across sessions and preventing the re-explanation tax.

### Governance Layer

Drift detection monitors implementation against planning artifacts, flagging divergence early. Hash verification ensures document integrity. Change order workflows enforce intentional modifications to locked specs. MVP implements manual validation checkpoints; the vision is automated validator agents monitoring continuously.

### Stage-Based Workflow

Five stages guide projects from concept to implementation-ready: Discovery, Solution Design, Environment Setup, Workflow Configuration, and Implementation Planning. Each stage has defined artifacts, completion criteria, and gate reviews before progression. Structure prevents the "just start coding" trap.

### Agent Orchestration Interface

Slack-style chat panel purpose-built for planning work. Agents can read current artifacts, suggest edits, validate consistency, and update sections—all within governance boundaries. The interface is for planning collaboration, not general-purpose chat.


## Value Proposition

**Maintain velocity without sacrificing quality.** AI agents move fast. IPE provides the structure that lets you keep pace—systematic validation instead of exhaustive manual review, drift detection instead of hoping you catch mistakes, single source of truth instead of scattered context.

**Reduce the re-explanation tax to zero.** Every session starts with full context. Agents know the project history, the decisions made, the alternatives rejected. You stop being the sole keeper of institutional knowledge.

**Catch drift before it compounds.** Small misalignments early become expensive refactors later. Governance mechanisms flag divergence when it's cheap to fix, not after you've built three features on a flawed foundation.

**Translate intent into executable specification.** The gap between "what you want" and "what agents build" is a translation problem. IPE structures your intent in formats agents can consume, with guardrails that keep execution aligned.

**Build a reusable system, not one-off documents.** Artifact templates, workflow patterns, and governance rules carry across projects. Each project improves the system.


## Success Looks Like

**3 months:**
- IPE used to plan and build IPE itself (dogfooding complete)
- 3-6 additional projects actively using IPE, including complex/enterprise-class ones
- Workflow feels natural—I'm not fighting the tool
- Drift detection proving value: catching misalignments I would have missed
- Context re-explanation tax eliminated: sessions start productive immediately

**6 months:**
- Open sourced and public
- Community forming: developers using it, forking it, building upon it
- Patterns documented: which artifact structures work, which need refinement
- Governance layer battle-tested across diverse project types
- Feedback loop established with early adopters

**12 months:**
- IPE is my default workflow for any significant project
- Active community contributing templates, improvements, integrations
- Tool has paid for itself many times over in time saved and mistakes avoided
- Clear signal on whether commercial path makes sense (not a goal, but data in hand)


## Non-Goals

IPE is NOT:

- **An IDE or code editor.** IPE handles pre-implementation planning. Code execution stays in your existing tools (VS Code, Cursor, etc.). IPE's output *feeds* your IDE—it doesn't replace it.

- **Version control.** Git remains your source of truth for code. IPE manages artifact versioning for planning documents, but repo management stays with Git/GitHub.

- **Issue tracking or project management.** We'll build integrations with Linear, Jira, and GitHub Issues in the future, but IPE doesn't replace them. Task management happens in your existing tools.

- **A general-purpose AI chat interface.** The agent chat is purpose-built for planning artifacts—reading, validating, and updating structured documents. It's not a replacement for Claude or ChatGPT for general questions.

- **Everything at once.** IPE fills a specific gap: the translation layer between human intent and AI execution. We're not building an all-in-one platform. We're building the planning and governance layer that's missing.


---

## END OF CONCEPT DOCUMENT

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
