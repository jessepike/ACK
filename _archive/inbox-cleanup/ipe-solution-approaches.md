# IPE Solution Approaches
## Three Weight Classes for Solving the Context/Governance Problem

**Date:** 2025-01-01  
**Purpose:** Evaluate solution approaches before committing to implementation

---

## Evaluation Criteria

Any solution must:
- ✓ Reduce friction, not add it
- ✓ Work immediately on real projects
- ✓ Handle memory/persistence
- ✓ Enable drift detection (at least partially automated)
- ✓ Get agent compliance from 60-70% → 90%+
- ✓ Fit into existing workflow

---

## Approach A: Structured Repo Layer (Lightest)

### Concept
No new app. Just a disciplined folder structure and file conventions that live in the repo. Agents are pointed to these files. Drift detection via git hooks and simple validation scripts.

### Components

```
project/
├── .context/
│   ├── intent.md           # What we're building and why
│   ├── decisions.md        # Key decisions with rationale
│   ├── constraints.md      # Technical and business constraints
│   ├── current-focus.md    # What we're working on NOW
│   └── memory.md           # Accumulated context (append-only)
├── .environment/
│   ├── manifest.yaml       # Agents, tools, plugins needed
│   ├── agent-configs/      # Per-agent configuration files
│   │   ├── claude.md       # Claude-specific instructions
│   │   └── cursor.rules    # Cursor rules if using
│   └── setup-checklist.md  # Manual setup steps
├── .rules/
│   ├── agent-instructions.md   # How agents should behave
│   └── validation-checks.md    # What to verify
├── .drift/
│   └── baseline.json       # Hash/snapshot of key specs
└── scripts/
    ├── inject-context.sh   # Prepares context for agent session
    ├── check-drift.sh      # Compares current state to baseline
    └── update-memory.sh    # Appends session learnings to memory
```

### Environment Manifest Example

```yaml
# .environment/manifest.yaml
project: risk-tools
type: web-app

agents:
  primary: claude-sonnet-4
  code-review: claude-opus
  research: gemini-pro

tools:
  - mcp-filesystem
  - mcp-github
  - mcp-postgres

memory:
  type: claude-projects
  backup: local-markdown

dependencies:
  runtime:
    - node: ">=20"
    - pnpm: ">=8"
  ai-tooling:
    - cursor: optional
    - claude-code: required

workflows:
  - spec-driven-development
  - pr-on-milestone

setup_notes: |
  1. Enable Claude memory for this project
  2. Configure MCP servers in Claude desktop
  3. Initialize repo with pnpm install
```

### How It Works

1. **Before session:** Run `inject-context.sh` → outputs combined context to paste or pipe to agent
2. **During session:** Agent references `.context/` and `.rules/` files
3. **After session:** Run `update-memory.sh` → captures what was learned/decided
4. **Periodically:** Run `check-drift.sh` → flags if code structure diverges from specs

### Drift Detection
- Hash key specification files
- Compare directory structure against declared architecture
- Simple: "These files exist that weren't in the plan"
- Script outputs diff for human review

### Pros
- Zero new tools—just files and scripts
- Version controlled with the code
- Works with any IDE, any agent
- Can start using today
- Portable across projects

### Cons
- Manual discipline required
- Context injection is copy/paste or CLI
- Drift detection is basic (structural, not semantic)
- No UI, no visualization
- Memory is just a file—no query capability

### Effort
- **Setup:** 1-2 days to create structure and scripts
- **Per project:** 30 min to initialize
- **Ongoing:** Low overhead if habits stick

### Best For
- Immediate start with no tooling investment
- Testing whether structured context actually helps
- Projects where simplicity > features

---

## Approach B: CLI + Local Memory Service (Medium)

### Concept
A CLI tool that manages context injection, memory persistence, and drift detection. Runs locally. No cloud dependency. Integrates with any editor via terminal.

### Components

```bash
ipe init                    # Initialize project with .ipe folder
ipe context                 # Show current context summary
ipe inject                  # Output context for agent (pipe or copy)
ipe remember "decision..."  # Add to persistent memory
ipe recall "architecture"   # Query memory for relevant context
ipe drift check             # Run drift detection
ipe drift baseline          # Update baseline after intentional changes
ipe status                  # Show project state, recent changes, flags
ipe env show                # Show current environment manifest
ipe env add tool <name>     # Add tool to manifest
ipe env validate            # Check if all required tools are available
ipe env export              # Export environment config for new project
ipe template list           # Show available project templates
ipe template apply <name>   # Apply template to current project
```

### Architecture

```
~/.ipe/                     # Global config and memory index
project/.ipe/
├── config.yaml             # Project settings
├── context/                # Structured context files
├── memory.db               # SQLite for queryable memory
├── baselines/              # Drift detection snapshots
└── history/                # Session logs
```

### How It Works

1. **Memory Layer:** SQLite database stores decisions, context, learnings. Queryable via `ipe recall`.
2. **Context Injection:** `ipe inject` compiles relevant context based on current directory/file. Can pipe directly to agent or copy to clipboard.
3. **Drift Detection:** Compares codebase against declared structure. Can hook into git commits.
4. **Session Tracking:** Optionally log what was done each session for continuity.

### Drift Detection
- Schema validation (does code structure match declared architecture?)
- File hash comparison for locked specs
- Pattern matching for architectural rules ("all API routes should be in /api")
- Git hook integration—warn before commit if drift detected

### Pros
- Queryable memory (not just flat files)
- Automated context injection
- Drift detection with git integration
- Works offline, no cloud dependency
- Can be extended over time
- Single tool, consistent interface

### Cons
- Need to build the CLI (or find existing one to adapt)
- Still terminal-based, no visual UI
- Memory query quality depends on how well things are indexed
- Learning curve for commands

### Effort
- **Build:** 1-2 weeks for basic CLI
- **Setup per project:** 10 min
- **Ongoing:** Low friction once habits form

### Best For
- Developers comfortable in terminal
- Projects that need real memory/query capability
- Wanting drift detection without full app
- Building toward something bigger incrementally

---

## Approach C: IDE Extension + Memory Service (Heavier)

### Concept
Extension for Zed or Anti-Gravity (or VS Code as fallback) that provides:
- Sidebar for context/artifact management
- Memory panel showing project state
- Drift detection with visual indicators
- Context injection into integrated AI chat

### Components

**Extension Features:**
- 📁 **Context Panel:** View/edit structured context files
- 🧠 **Memory Panel:** Query and add to project memory
- ⚠️ **Drift Indicators:** Gutter/status bar warnings when drift detected
- 📋 **Inject Button:** One-click context preparation for AI chat
- ✓ **Checkpoint UI:** Simple "mark as complete" for artifacts

**Backend Service:**
- Local memory service (same as Approach B)
- File watcher for real-time drift detection
- API for extension to query/update

### How It Works

1. **Sidebar shows current context state** — what's defined, what's in progress, any flags
2. **Memory is always available** — search past decisions without leaving editor
3. **Drift detection runs continuously** — warnings appear inline or in status bar
4. **One-click context injection** — prepares agent prompt with relevant context
5. **Checkpoints are visual** — click to mark sections/artifacts complete

### Drift Detection
- Same as Approach B, but real-time via file watcher
- Visual indicators in editor (red squiggle, status bar icon)
- Diff view showing spec vs. implementation

### Pros
- Lives where you work (no context switch)
- Visual interface for state management
- Real-time feedback on drift
- Lower friction for context injection
- Could integrate with IDE's native AI features

### Cons
- More complex to build
- Tied to specific IDE(s)
- Extension APIs vary (Zed vs. VS Code vs. Anti-Gravity)
- More maintenance burden
- Risk of becoming bloated

### Effort
- **Build:** 4-8 weeks for functional extension + backend
- **Setup per project:** 5 min
- **Ongoing:** Should be lowest friction of all approaches

### Best For
- Heavy daily use across multiple projects
- Strong preference for visual over terminal
- Willing to invest build time for better UX
- Long-term tool you'll use for years

---

## Comparison Matrix

| Capability | Approach A (Repo) | Approach B (CLI) | Approach C (Extension) |
|------------|-------------------|------------------|------------------------|
| Setup time | 1-2 days | 1-2 weeks | 4-8 weeks |
| Per-project init | 30 min | 10 min | 5 min |
| Memory persistence | File-based | SQLite (queryable) | SQLite (queryable) |
| Context injection | Manual paste | CLI command | One-click |
| Drift detection | Basic scripts | Git hooks + CLI | Real-time visual |
| Environment manifest | YAML file (manual) | CLI-managed | UI-managed |
| Template reuse | Copy folder | `ipe template` | Template picker UI |
| IDE integration | None | Terminal | Native sidebar |
| Friction level | Medium | Low-Medium | Low |
| Flexibility | High | High | Medium (IDE-specific) |
| Build complexity | Minimal | Moderate | High |

---

## Recommendation

### Start with Approach A (1-2 days)
- Prove the concept works
- Test structured context with real projects
- Learn what actually helps vs. what's overhead
- Zero tooling investment

### Evolve to Approach B (if A proves valuable)
- Build CLI incrementally
- Add features based on actual pain points
- Keep it simple, don't overbuild

### Consider Approach C (if B becomes daily driver)
- Only if CLI friction is the bottleneck
- Only for IDE you're committed to long-term
- Could contribute to Zed ecosystem if valuable

---

## Hybrid Path

Nothing says these are exclusive. A pragmatic path:

1. **Week 1:** Implement Approach A structure in one project
2. **Week 2-3:** Use it manually, note friction points
3. **Week 4:** Build minimal CLI for worst friction (maybe just `ipe inject` and `ipe remember`)
4. **Month 2:** Expand CLI based on real usage
5. **Month 3+:** Evaluate if extension is worth it

This way you're always using something, learning what matters, and building only what you need.

---

## Questions Before Deciding

1. How much do you want to build vs. use existing pieces?
2. Is terminal workflow acceptable, or do you need visual UI?
3. Which IDE are you committing to? (Affects extension approach)
4. How important is queryable memory vs. simple append-only?
5. Can basic drift detection (structural) suffice, or do you need semantic analysis?

---

## Next Steps

1. **Pick an approach** (recommend starting with A)
2. **Define the artifact structure** for your first project
3. **Build/implement** the minimum version
4. **Use it on a real project** for 1-2 weeks
5. **Evaluate** what worked, what didn't
6. **Iterate** toward B or C if needed

---

**The goal: Start simple, prove value, expand based on real feedback.**
