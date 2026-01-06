# MVP Scope: ACK v1.0

---
status: "Draft"
created: 2025-01-01
author: "jess@pike"
---

## MVP Definition

<!-- 
What's the minimum viable product?
- Core value proposition in one sentence
- What can users do with v1.0?
- What problem does it solve (even if incomplete)?

Think: "Smallest thing that delivers real value"
-->

**One-line MVP:**


**Core user journey (v1.0):**
1. 
2. 
3. 
4. 
5. 


**Value delivered:**




## In Scope (v1.0)

<!-- 
Features/capabilities included in MVP:
- Group by category
- Include rationale for each
- Be specific about depth (full feature vs. basic version)

Format: Feature name | Description | Rationale
-->

### Core Features

**✓ Feature 1:**
- **What:** 
- **Why in v1.0:** 
- **Implementation level:** [Full / Basic / MVP]


**✓ Feature 2:**
- **What:** 
- **Why in v1.0:** 
- **Implementation level:**


**✓ Feature 3:**
- **What:** 
- **Why in v1.0:** 
- **Implementation level:**



### Stage Coverage

**Stages included in v1.0:**
- ✓ Discovery stage
  - All 4 artifacts (concept, research, validation, scope)
  - All sections
  - Full functionality
  
- ✓ Solution Design stage
  - [Which artifacts?]
  - [What depth?]
  
- [ ] Environment Setup stage
  - [Deferred to v1.1]
  
- [ ] Workflow Configuration stage
  - [Deferred to v1.1]
  
- [ ] Implementation Planning stage
  - [Deferred to v1.1]


### Technology Choices

**Included in v1.0:**
- Tech stack: Next.js 14, Tiptap, Supabase, Tailwind
- Deployment: Vercel
- Auth: Supabase Auth
- Storage: Supabase PostgreSQL + Storage


### Agent Capabilities

**Included in v1.0:**
- [ ] Chat interface with message history
- [ ] Agent can read artifact context
- [ ] Agent can suggest content for sections
- [ ] Basic commands (@mention, /commands)
- [ ] Snapshot creation before agent changes


### User Experience

**Included in v1.0:**
- [ ] 3-panel layout (sidebar, editor, chat)
- [ ] File tree navigation
- [ ] Section collapse/expand
- [ ] Progress tracking (X/Y done)
- [ ] Auto-save
- [ ] Markdown editor (Tiptap)
- [ ] Stage tab navigation


### Data & Storage

**Included in v1.0:**
- [ ] Projects, artifacts, sections schema
- [ ] Snapshot versioning
- [ ] Chat message history
- [ ] User authentication
- [ ] Multi-project support



## Out of Scope (v1.0)

<!-- 
Features explicitly NOT in MVP:
- Why excluded?
- When might they be added?
- What's the risk of excluding?

Be honest about limitations
-->

### Deferred to v1.1

**✗ Feature X:**
- **Why not v1.0:** 
- **Target version:** v1.1
- **Risk of excluding:** [Low / Medium / High]


**✗ Feature Y:**
- **Why not v1.0:** 
- **Target version:** v1.1
- **Risk of excluding:**


**✗ Stages 3-5 (Environment, Workflow, Implementation):**
- **Why not v1.0:** Focus on Discovery + Design first, validate workflow
- **Target version:** v1.1-v1.3
- **Risk of excluding:** Low - can validate core concept with 2 stages


**✗ Team collaboration:**
- **Why not v1.0:** Solo developer MVP, multiplayer complexity high
- **Target version:** v2.0
- **Risk of excluding:** Low for early adopters (solo devs)


**✗ Advanced agent features:**
- **Why not v1.0:** 
- **Target version:** 
- **Risk of excluding:**



### Explicitly NOT Building

**✗ Never/Maybe:**
- 
- 
- 

**Rationale:**




## MVP Constraints

<!-- 
Limitations we're accepting in v1.0:
- Technical debt
- UX compromises
- Performance targets
- Scale limitations
-->

### Technical Constraints

**What we're punting:**
- Offline mode → Online-only for v1.0
- Real-time collaboration → Single user for v1.0
- Mobile app → Web-only for v1.0
- [Constraint] → [Accepted limitation]


### Performance Targets

**Good enough for v1.0:**
- Load time: < 3 seconds
- Auto-save latency: < 1 second
- Agent response: < 10 seconds
- Max artifacts per project: 100
- Max project size: 50MB


### Scale Targets

**v1.0 is designed for:**
- User count: 50-100 users
- Project count: 10-20 projects per user
- Concurrent users: 10-20
- Storage per user: < 100MB



## Success Criteria

<!-- 
How do we know v1.0 succeeded?
- Adoption metrics
- Usage patterns
- User feedback
- Technical metrics

Be specific and measurable
-->

### Adoption Goals (3 months post-launch)

**User acquisition:**
- [ ] 50 active users (weekly active)
- [ ] 20 completed projects (Discovery → Design)
- [ ] 10 power users (5+ projects)


**Engagement:**
- [ ] Average session: 20+ minutes
- [ ] 3+ sessions per week per active user
- [ ] 70%+ completion rate for started projects


**Retention:**
- [ ] 50%+ week-over-week retention
- [ ] 30%+ month-over-month retention


### Quality Metrics

**Technical:**
- [ ] < 1% error rate
- [ ] > 99% uptime
- [ ] < 2 second p95 load time


**User satisfaction:**
- [ ] NPS > 30
- [ ] 70%+ would recommend to colleague
- [ ] < 5% churn rate


### Qualitative Success

**Users say:**
- "This replaced my Notion docs for planning"
- "I actually keep my docs up to date now"
- "The agent helps me think through problems"

**Observable behaviors:**
- Users complete full Discovery stage
- Users share projects with team
- Users request features (engagement signal)



## Future Roadmap

<!-- 
What comes after v1.0?
- v1.1, v1.2, v2.0 ideas
- Feature buckets
- Strategic direction

This is tentative/aspirational
-->

### v1.1 (1-2 months post-v1.0)

**Focus:** Polish + Stage 3 (Environment Setup)
- Environment Setup stage artifacts
- Improved agent capabilities
- Performance improvements
- Bug fixes from v1.0 feedback


### v1.2 (3-4 months post-v1.0)

**Focus:** Stages 4-5 + Templates
- Workflow Configuration stage
- Implementation Planning stage
- Project templates
- Export capabilities


### v2.0 (6-12 months post-v1.0)

**Focus:** Team features + Advanced agents
- Multi-user collaboration
- Real-time editing
- Advanced agent orchestration
- Integrations (GitHub, Jira, Linear)


### Future Ideas (No timeline)

**Potential features:**
- Mobile app
- VS Code extension
- AI model switching
- Custom agent workflows
- Analytics dashboard
- Project templates marketplace



---

## Development Timeline

<!-- 
How long will v1.0 take?
- Major milestones
- Dependencies
- Launch date target
-->

### Phase 1: Foundation (Weeks 1-2)
- Week 1: Manual Discovery (this doc!)
- Week 2: Schema + Editor basics

### Phase 2: Core Features (Weeks 3-5)
- Week 3: Agent integration
- Week 4: Solution Design stage
- Week 5: Polish + testing

### Phase 3: Launch (Week 6)
- Week 6: Beta testing + launch


**Target launch date:**


**Launch criteria:**
- [ ] All v1.0 features complete
- [ ] 5 beta testers have used it successfully
- [ ] No P0 bugs
- [ ] Documentation complete



---

**Agent help wanted:**
- [ ] Analyze concept.md features and suggest MVP subset
- [ ] Validate scope is achievable in 6 weeks
- [ ] Suggest what to defer based on complexity
- [ ] Draft success criteria based on similar products
