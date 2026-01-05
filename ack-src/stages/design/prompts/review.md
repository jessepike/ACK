---
type: prompt
stage: design
prompt: review
description: "Content analysis prompt for Design stage deliverables"
version: 1.0.0
updated: "2026-01-04T00:00:00"
---

# Design Stage Review

Review the architecture, data model, and stack decisions for technical soundness.

## Instructions

You are reviewing three Design stage deliverables to assess whether they're ready to advance to the Setup stage. Focus on **technical soundness and alignment with the brief**.

Read all three documents, then evaluate each area below.

---

## Pre-Review: Brief Alignment

Before reviewing technical details, verify alignment with the brief:

- [ ] **Constraints honored:** Design respects budget, timeline, resource constraints
- [ ] **Scope matched:** Design covers in-scope items, doesn't add out-of-scope features
- [ ] **Success criteria achievable:** Architecture can support stated success metrics

If misaligned, note as blocking issue before continuing.

---

## Architecture Review

### 1. Component Design

- [ ] **Components identified:** All major system parts are defined
- [ ] **Boundaries clear:** Each component has a single, clear responsibility
- [ ] **Coupling appropriate:** Components interact through well-defined interfaces
- [ ] **No orphans:** Every component connects to the overall system

**Questions to answer:**
- Could you explain what each component does in one sentence?
- Are there components doing too much (god objects)?
- Are there unnecessary components that add complexity?

### 2. Data Flow

- [ ] **Flow documented:** Clear how data moves through the system
- [ ] **Entry points defined:** Know where data enters the system
- [ ] **Transformations clear:** Understand what happens to data at each step
- [ ] **Exit points defined:** Know where data leaves the system

**Questions to answer:**
- Can you trace a user action from input to output?
- Are there dead ends or unclear handoffs?
- Is the flow unnecessarily complex?

### 3. API Design (if applicable)

- [ ] **Endpoints defined:** Major API routes/operations listed
- [ ] **Contracts clear:** Request/response shapes documented
- [ ] **Consistency:** Naming conventions and patterns are uniform
- [ ] **Versioning considered:** Strategy for API evolution

### 4. Security Architecture

- [ ] **Authentication planned:** How users prove identity
- [ ] **Authorization planned:** How access control works
- [ ] **Data protection:** Sensitive data handling addressed
- [ ] **Attack vectors considered:** Common threats mitigated

**Questions to answer:**
- What's the authentication flow?
- How is sensitive data protected at rest and in transit?
- Are there obvious security gaps?

---

## Data Model Review

### 1. Entity Design

- [ ] **Core entities identified:** All major data objects defined
- [ ] **Attributes complete:** Each entity has necessary fields
- [ ] **Types appropriate:** Field types match their purpose
- [ ] **Naming consistent:** Entities and fields follow conventions

**Questions to answer:**
- Are entities normalized appropriately (not over or under)?
- Are there missing entities implied by the brief?
- Do entity names clearly describe what they represent?

### 2. Relationships

- [ ] **Relationships defined:** How entities connect is clear
- [ ] **Cardinality correct:** One-to-one, one-to-many, many-to-many appropriate
- [ ] **Referential integrity:** Foreign keys and constraints planned
- [ ] **No orphan entities:** Every entity relates to the system

**Questions to answer:**
- Can you navigate from any entity to related data?
- Are there circular dependencies that could cause issues?
- Are relationship directions logical?

### 3. Query Patterns

- [ ] **Access patterns considered:** How data will be read/written
- [ ] **Indexes planned:** Performance-critical queries identified
- [ ] **Denormalization justified:** If denormalized, rationale provided

### 4. Evolution

- [ ] **Migration strategy:** How schema changes will be handled
- [ ] **Backward compatibility:** Impact of changes considered
- [ ] **Growth planned:** Schema can accommodate expected scale

---

## Stack Review

### 1. Technology Choices

- [ ] **Choices justified:** Each technology has clear rationale
- [ ] **Constraints respected:** Choices fit budget, timeline, expertise
- [ ] **Proven technologies:** Preference for stable, well-supported options
- [ ] **Ecosystem fit:** Technologies work well together

**Questions to answer:**
- Why this technology over alternatives?
- Is there team expertise or learning curve to consider?
- Are there licensing or cost implications?

### 2. Frontend Stack (if applicable)

- [ ] **Framework chosen:** With rationale
- [ ] **State management:** Approach defined
- [ ] **Styling approach:** CSS strategy decided
- [ ] **Build tooling:** Bundler, transpiler, etc.

### 3. Backend Stack (if applicable)

- [ ] **Language/framework chosen:** With rationale
- [ ] **API approach:** REST, GraphQL, RPC, etc.
- [ ] **Background jobs:** If needed, approach defined
- [ ] **Caching strategy:** If needed, approach defined

### 4. Data Stack

- [ ] **Database chosen:** With rationale for type (SQL, NoSQL, etc.)
- [ ] **Hosting/management:** Self-hosted vs. managed
- [ ] **Backup strategy:** Data durability planned
- [ ] **Connection management:** Pooling, limits considered

### 5. Infrastructure

- [ ] **Deployment target:** Where it will run
- [ ] **Scaling approach:** How to handle growth
- [ ] **Monitoring:** Observability strategy
- [ ] **CI/CD compatibility:** Stack works with planned automation

---

## Cross-Cutting Concerns

### 1. Consistency

- [ ] **Architecture ↔ Data Model:** Components align with entities
- [ ] **Architecture ↔ Stack:** Technology supports architectural patterns
- [ ] **Data Model ↔ Stack:** Database choice fits data model needs

### 2. Completeness

- [ ] **No gaps:** Every brief requirement has a design answer
- [ ] **No extras:** Design doesn't add unrequested complexity
- [ ] **Dependencies clear:** External services/APIs identified

### 3. Feasibility

- [ ] **Buildable:** Team can implement this design
- [ ] **Testable:** Design supports testing strategy
- [ ] **Deployable:** Design works with available infrastructure

---

## Review Output

### Summary

| Area | Rating | Notes |
|------|--------|-------|
| Architecture - Components | Strong / Adequate / Weak | [Key observation] |
| Architecture - Data Flow | Strong / Adequate / Weak | [Key observation] |
| Architecture - Security | Strong / Adequate / Weak | [Key observation] |
| Data Model - Entities | Strong / Adequate / Weak | [Key observation] |
| Data Model - Relationships | Strong / Adequate / Weak | [Key observation] |
| Stack - Choices | Strong / Adequate / Weak | [Key observation] |
| Stack - Justification | Strong / Adequate / Weak | [Key observation] |
| Cross-Cutting - Consistency | Strong / Adequate / Weak | [Key observation] |

### Strengths

- [What's working well]
- [What's working well]

### Issues to Address

| Issue | Severity | Document | Recommendation |
|-------|----------|----------|----------------|
| [Issue 1] | Blocking / Important / Minor | architecture.md | [How to fix] |
| [Issue 2] | Blocking / Important / Minor | data-model.md | [How to fix] |
| [Issue 3] | Blocking / Important / Minor | stack.md | [How to fix] |

### Verdict

**[ ] Ready to advance** - Design is sound, proceed to Setup stage

**[ ] Revise and re-review** - Address issues above, then review again

**[ ] Needs significant work** - Fundamental gaps require rethinking

---

## Notes

- All three deliverables must pass review to advance
- A weak rating in one area doesn't necessarily block advancement
- Blocking issues in ANY document block the entire stage
- "Adequate" means good enough to build, not perfect
