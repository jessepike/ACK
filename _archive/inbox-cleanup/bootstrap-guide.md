# Using IPE to Build IPE
## Meta-Bootstrapping Guide

## Why This Approach?

**Benefits of eating our own dog food:**
1. ✅ **Validates workflow** - If it's painful to use, we'll feel it immediately
2. ✅ **Creates real templates** - Artifacts become reusable templates
3. ✅ **Identifies gaps** - "We need a field for X" surfaces naturally
4. ✅ **Generates documentation** - The artifacts you create ARE the docs
5. ✅ **Tests assumptions** - Theory meets practice early

**What we'll build while building:**
- Section templates for each artifact type
- Agent prompt patterns
- Workflow documentation
- Real examples for users

---

## The Plan: 3-Week Bootstrap

### Week 1: Manual Discovery (No Code)
**Goal:** Create Discovery artifacts manually, capture templates

**Deliverables:**
- [ ] concept.md (complete, finalized)
- [ ] research.md (complete, finalized)
- [ ] validation.md (complete, finalized)
- [ ] scope.md (complete, finalized)

**Process:**
1. Write artifacts in plain markdown
2. Track pain points (where you want agent help)
3. Note section templates that work
4. Document workflow decisions

**Output:**
- 4 finalized markdown files
- Template definitions for each artifact
- List of "I wish I had an agent for X"

---

### Week 2: Build Editor (Implement Learnings)
**Goal:** Build Tiptap editor using Week 1 content as test data

**Deliverables:**
- [ ] Next.js app with 3-panel layout
- [ ] Tiptap editor with section nodes
- [ ] Supabase schema deployed
- [ ] File tree navigation
- [ ] Section collapse/expand
- [ ] Done checkbox functionality

**Process:**
1. Use Week 1 markdown files as seed data
2. Implement section structure you validated
3. Build UI for the templates you created
4. Test with real content (your IPE artifacts)

**Output:**
- Working editor that can display/edit Discovery artifacts
- Validated data model
- Working progress tracking

---

### Week 3: Add Agents (Automate Pain Points)
**Goal:** Build agent capabilities for the pain points identified in Week 1

**Deliverables:**
- [ ] Chat panel functionality
- [ ] Agent can read artifact context
- [ ] Agent can update specific sections
- [ ] Agent commands (@mention, /commands)
- [ ] Snapshot creation before agent changes

**Process:**
1. Review Week 1 pain point list
2. Implement agent features for top 3 pain points
3. Test on Solution Design stage (Stage 2)
4. Validate snapshot/rollback works

**Output:**
- Working agent integration
- Tested on real use case (designing IPE)
- Proven snapshot safety net

---

## Week 1 Detailed: Manual Discovery

### Day 1-2: concept.md

**Sections to complete:**
1. **What Is It?** - Define IPE in 2-3 paragraphs
2. **Problem Being Solved** - Context switching, stale docs, PM/Eng friction
3. **Core Features** - Living docs, agent orchestration, context-aware validation
4. **Value Proposition** - Reduce switching by 60%, real-time feasibility checks
5. **Success Looks Like** - Measurable outcomes
6. **Non-Goals** - What IPE is NOT

**Template capture:**
```markdown
# concept.md Template

## Section: What Is It?
- Length: 2-3 paragraphs
- Content: Product definition, core purpose
- Agent help: None needed, user writes this

## Section: Problem Being Solved
- Length: 1 paragraph context + bulleted pain points
- Content: Current state problems
- Agent help: Research similar tools' problem statements

## Section: Core Features
- Length: 3-5 features with descriptions
- Content: Key capabilities
- Agent help: Suggest features based on problem statement

... (continue for all sections)
```

**Pain points to note:**
- "I wish an agent could research competitive positioning"
- "I want an agent to suggest success metrics based on features"
- "I need help validating if these features are feasible"

---

### Day 3-4: research.md

**Sections to complete:**
1. **Market Landscape** - Who else is in this space?
2. **Competitive Analysis** - Direct competitors (Cursor, Cline)
3. **Differentiation** - What makes IPE unique?
4. **Market Opportunity** - TAM/SAM sizing

**Template capture:**
```markdown
# research.md Template

## Section: Market Landscape
- Length: 2-3 paragraphs + table
- Content: Market categories, key players
- Agent help: "Search for AI-augmented dev tools and summarize"

## Section: Competitive Analysis
- Length: Comparison table + 2-3 paragraphs
- Content: Feature comparison, strengths/weaknesses
- Agent help: "Fetch latest docs for Cursor, Cline, summarize features"
```

**Pain points to note:**
- "Agent should auto-fetch competitor docs"
- "Agent should build comparison tables"
- "I need agent to track market changes over time"

---

### Day 5-6: validation.md

**Sections to complete:**
1. **User Interviews** - Who did you talk to?
2. **Problem Validation** - Do they have this pain?
3. **Solution Fit** - Would they use IPE?

**Template capture:**
```markdown
# validation.md Template

## Section: User Interviews
- Length: Table of interviewees + key quotes
- Content: Interview subjects, roles, quotes
- Agent help: "Structure interview notes into table"

## Section: Problem Validation
- Length: 3-4 paragraphs
- Content: Validated pain points with evidence
- Agent help: "Analyze interview transcripts for patterns"
```

**Pain points to note:**
- "Agent should parse interview transcripts"
- "Agent should identify common themes"
- "I want agent to suggest validation methods"

---

### Day 7: scope.md

**Sections to complete:**
1. **MVP Scope** - What's in v1.0?
2. **Out of Scope** - What's explicitly NOT in v1.0?
3. **Future Roadmap** - v1.1, v2.0 ideas
4. **Success Criteria** - How do we know MVP succeeded?

**Template capture:**
```markdown
# scope.md Template

## Section: MVP Scope
- Length: Bulleted list + rationale
- Content: Feature list with justification
- Agent help: "Given concept.md features, suggest MVP subset"

## Section: Out of Scope
- Length: Bulleted list with explanations
- Content: Deferred features
- Agent help: "Given MVP scope, suggest what to defer"
```

**Pain points to note:**
- "Agent should suggest MVP scope based on concept"
- "Agent should validate scope is achievable in timeframe"
- "I want agent to draft success criteria"

---

## Capturing Templates

### Template Structure
For each artifact, document:

```typescript
interface ArtifactTemplate {
  slug: string;
  name: string;
  stage: string;
  sections: SectionTemplate[];
}

interface SectionTemplate {
  slug: string;
  title: string;
  order: number;
  description: string;
  expectedLength: string;  // "2-3 paragraphs", "table + 1 paragraph"
  agentHelp: string | null;  // "None" | "Research X and summarize"
  exampleContent: string;  // Actual example from your IPE artifacts
}
```

### Example: concept.md Template

```json
{
  "slug": "concept",
  "name": "concept.md",
  "stage": "discovery",
  "sections": [
    {
      "slug": "what-is-it",
      "title": "What Is It?",
      "order": 1,
      "description": "Product definition and core purpose in 2-3 paragraphs",
      "expectedLength": "2-3 paragraphs",
      "agentHelp": null,
      "exampleContent": "IPE (Integrated Planning Environment) is a planning layer that orchestrates AI-augmented development from concept to implementation-ready state..."
    },
    {
      "slug": "problem-being-solved",
      "title": "Problem Being Solved",
      "order": 2,
      "description": "Context paragraph + bulleted pain points",
      "expectedLength": "1 paragraph + 3-5 bullets",
      "agentHelp": "Research similar tools' problem statements",
      "exampleContent": "Developers currently spend 40% of their time context-switching between planning documents..."
    }
    // ... more sections
  ]
}
```

---

## Week 1 End Deliverables

### 1. Finalized Markdown Files
```
/ipe-demo/
  /discovery/
    concept.md         ✓ Finalized
    research.md        ✓ Finalized
    validation.md      ✓ Finalized
    scope.md           ✓ Finalized
```

### 2. Template Definitions
```
/templates/
  discovery/
    concept.template.json
    research.template.json
    validation.template.json
    scope.template.json
```

### 3. Agent Requirements Doc
```markdown
# Agent Features Needed (Priority Order)

## P0 (Week 3)
1. Research competitive tools and summarize
2. Build comparison tables from docs
3. Suggest features based on problem statement

## P1 (Post-MVP)
4. Parse interview transcripts for themes
5. Validate scope achievability
6. Track market changes over time

## P2 (Future)
7. Auto-update research when competitors ship
8. Suggest success metrics from features
```

---

## Week 2: Building the Editor

### Use Week 1 Content as Seed Data

**Migration script:**
```typescript
// scripts/seed-ipe-demo.ts
async function seedIPEDemo() {
  // 1. Create project
  const project = await supabase
    .from('projects')
    .insert({ name: 'ipe-demo', current_stage: 'discovery' })
    .select()
    .single();
  
  // 2. Create artifacts from markdown files
  const conceptMd = fs.readFileSync('./ipe-demo/discovery/concept.md', 'utf-8');
  const conceptContent = markdownToTiptapJSON(conceptMd);
  
  await supabase.from('artifacts').insert({
    project_id: project.id,
    name: 'concept.md',
    slug: 'concept',
    stage: 'discovery',
    status: 'finalized',
    content: conceptContent,
    section_metadata: CONCEPT_SECTIONS,
    sections_total: 6,
    sections_complete: 6
  });
  
  // ... repeat for other artifacts
}
```

### Test Editor with Real Content

**Test scenarios:**
1. ✅ Open concept.md → See all 6 sections
2. ✅ Collapse section → UI updates
3. ✅ Uncheck "Done" → Progress badge updates (6/6 → 5/6)
4. ✅ Edit content → Auto-saves to Supabase
5. ✅ Switch to research.md → Content loads

---

## Week 3: Adding Agents

### Implement Top 3 Pain Points

**Based on Week 1 notes:**

#### Pain Point #1: Research competitive tools
**Agent capability:**
```typescript
// Command: "/research [tool name]"
async function researchTool(toolName: string) {
  // 1. Web search for tool
  const searchResults = await webSearch(toolName + " features docs");
  
  // 2. Fetch docs
  const docs = await fetchDocs(searchResults[0].url);
  
  // 3. Summarize
  const summary = await claude.summarize(docs);
  
  // 4. Update research.md
  await updateSection('research', 'competitive-analysis', summary);
}
```

#### Pain Point #2: Build comparison tables
**Agent capability:**
```typescript
// Command: "/compare [tool1] [tool2]"
async function compareTools(tools: string[]) {
  // 1. Gather feature lists
  const features = await Promise.all(
    tools.map(tool => getFeatureList(tool))
  );
  
  // 2. Generate markdown table
  const table = generateComparisonTable(tools, features);
  
  // 3. Insert into research.md
  await updateSection('research', 'competitive-analysis', table);
}
```

#### Pain Point #3: Suggest features
**Agent capability:**
```typescript
// Command: "/suggest-features"
async function suggestFeatures() {
  // 1. Read problem statement from concept.md
  const problems = await getSection('concept', 'problem-being-solved');
  
  // 2. Ask Claude for feature ideas
  const suggestions = await claude.ask(
    `Given these problems: ${problems}\nSuggest 5 core features for a solution.`
  );
  
  // 3. Update concept.md
  await updateSection('concept', 'core-features', suggestions);
}
```

---

## Success Metrics for Bootstrap

**By end of Week 3, you should have:**

### Functional Product
- ✅ Editor that loads/saves Discovery artifacts
- ✅ Section collapse/expand works
- ✅ Progress tracking accurate
- ✅ Chat panel with 3 working agent commands
- ✅ Snapshot creation/restoration tested

### Real Artifacts
- ✅ 4 finalized Discovery artifacts (your IPE docs)
- ✅ Starting Solution Design stage artifacts
- ✅ Proven templates for future projects

### Validated Workflow
- ✅ Confirmed section structure works
- ✅ Identified which agent features matter most
- ✅ Documented pain points to avoid
- ✅ Ready to complete Stage 2-5 using your own tool

---

## What This Gives You

**Immediate value:**
- Working MVP in 3 weeks
- Real documentation for IPE
- Validated product design

**Long-term value:**
- Templates for future projects
- Proven agent patterns
- User manual writes itself (your artifacts)
- Demo content for marketing

**Confidence:**
- You've used it yourself
- You know it works
- You've felt the pain points
- You've proven the workflow

---

## Next Steps After Bootstrap

### Week 4: Complete Solution Design Stage
Use IPE to design IPE's architecture:
- stack.md (Next.js, Tiptap, Supabase - already decided!)
- architecture.md (3-panel layout, agent integration)
- data-model.md (artifacts, sections, snapshots - already done!)
- context-schema.md (How agents read/write artifacts)

### Week 5: Environment Setup Stage
Use IPE to set up IPE's repo:
- repo-init.md (GitHub, structure, .env)
- dependencies.md (package.json entries)
- scaffolding.md (folder structure, base components)

### Week 6+: Polish & Launch
- Workflow + Implementation stages
- Public beta
- Documentation site (generated from your artifacts!)

---

**Ready to start Week 1?** Let me know if you want me to create the initial markdown file scaffolds for the Discovery artifacts!
