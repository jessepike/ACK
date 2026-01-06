---
total_insights: 40
high_priority: 23
medium_priority: 17
last_updated: 2026-01-04
last_curated: 2026-01-04
sources_count: 6
---

# Tips & Insights Backlog

Actionable insights extracted from external sources for ACK improvement.

**Statuses**: `backlog` | `in-progress` | `implemented` | `rejected`

---

## High Priority

### [ARCHITECTURE] Artifact Governance System
- **Source**: Internal planning session
- **Added**: 2026-01-04
- **Description**: Comprehensive artifact creation and validation system with config-driven scope (`.frontmatter.yaml`), `/create-artifact` skill, pre-commit validation hooks, and template migrations to match the frontmatter schema.
- **Application**: Implement 5-phase plan: (1) Foundation config file, (2) Template migrations, (3) Pre-commit hooks, (4) /create-artifact skill with full workflow, (5) Artifact registry. See `docs/plans/artifact-governance.md` for full plan.
- **Effort**: high | **Impact**: high
- **Status**: backlog

### [WORKFLOW] Project Self-Onboarding via Init
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Description**: Automated generation of project documentation that helps AI understand codebase structure, conventions, and patterns without manual explanation.
- **Application**: Implement ACK's `/scaffold` command to generate CLAUDE.md-style memory files that document governance rules, validation schemas, and registry metadata standards.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [PATTERN] Hierarchical Context Management
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Description**: Layered memory system combining general project docs with topic-specific rules organized in `.claude/rules/` with conditional path-based activation via YAML frontmatter.
- **Application**: Build ACK's memory layer with governance rules separated by artifact type that activate based on file patterns during AI interactions.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [ARCHITECTURE] Hooks for Deterministic Control
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Description**: Lifecycle hooks (PreToolUse, PermissionRequest, etc.) enable custom shell scripts to intercept and control AI actions at critical points.
- **Application**: Design ACK's governance layer as hook handlers: validate artifacts pre-write, log registry mutations, enforce permission checks.
- **Effort**: high | **Impact**: high
- **Status**: backlog

### [WORKFLOW] Parallel Claude Execution
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Run 5 Claudes in parallel across numbered terminal tabs with system notifications (iTerm2) for completion alerts. Hand off long tasks with `&` or `--teleport`.
- **Application**: Design ACK workflows to support parallel artifact validation—run governance checks, schema validation, and registry updates concurrently across multiple Claude instances.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [PATTERN] Shared CLAUDE.md with Mistakes Log
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Single CLAUDE.md checked into git, team contributes multiple times/week. Critically, add past mistakes so Claude won't repeat them.
- **Application**: ACK's memory tier should include a `mistakes.md` or error log section that captures governance violations and failed validations to prevent recurrence.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [WORKFLOW] Slash Commands for Workflows
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Store repeated workflows in `.claude/commands/`, check into git. Use inline bash to pre-compute values for speed. Example: `/commit-push-pr` used dozens of times daily.
- **Application**: Ship ACK with pre-built slash commands: `/validate-artifact`, `/register`, `/check-governance`, `/scaffold-project` stored in registry for team reuse.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [TECHNIQUE] Subagents for Specialized Tasks
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Define purpose-built subagents like `code-simplifier` (simplifies code when done) and `verify-app` (end-to-end testing instructions).
- **Application**: Create ACK subagents: `artifact-validator`, `registry-checker`, `governance-auditor` that can be invoked for specialized validation tasks.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [ARCHITECTURE] Stop Hooks for Auto-Resume
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Stop hooks enable auto-resume for long-running tasks (up to ~42 hours). PostToolUse hooks format code. Ralph-wiggum plugin enables continuous running.
- **Application**: Implement ACK governance as stop hooks—automatically resume validation pipelines, checkpoint progress, and ensure deterministic completion of registry operations.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [INTEGRATION] PR Review with @claude Tagging
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Tag @claude on coworkers' PRs during code review to suggest additions to shared docs. Uses GitHub Action for automated integration, inspired by "Compounding Engineering" concept.
- **Application**: Create ACK GitHub Action that validates artifacts on PR, tags violations, and auto-suggests governance doc updates when patterns are detected.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [TECHNIQUE] Inline Bash Pre-computation
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Slash commands use inline bash to pre-compute values (git status, file info) before Claude processes, reducing back-and-forth and enabling Claude to use the workflow itself.
- **Application**: ACK slash commands should pre-compute registry state, artifact checksums, and validation status inline—pass computed context to Claude rather than having it query repeatedly.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [PATTERN] Verification as Quality Multiplier
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Giving Claude ways to verify its own work 2-3x the quality. Domain-specific verification is key—bash commands, test suites, Chrome extension for UI testing, simulators.
- **Application**: Build verification into every ACK workflow: schema validation after artifact creation, registry consistency checks, governance rule compliance verification as mandatory post-steps.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [PATTERN] Team Knowledge Compounding
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Shared docs grow via team contributions multiple times/week. Add guidance whenever Claude makes a mistake. Different teams maintain their own docs. Knowledge compounds over time.
- **Application**: ACK governance docs should have contribution workflow—when validation fails, prompt user to add the failure pattern to prevention rules, compounding team knowledge.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [PATTERN] Spec-Driven Constrained Executor
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Treat Claude as a constrained executor, not a conversational coder. Define intent precisely with markdown sections, bullet constraints, tables, and XML-style tags. Separate "What" (behavior, constraints, success) from "How" (left to model).
- **Application**: ACK artifact templates should enforce structured spec format—require Objective, Constraints, Acceptance Criteria sections. Reject prose-only artifact definitions.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [ARCHITECTURE] Minimal Starter File Set
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Every serious project needs CLAUDE.md (rules), PROJECT.md (what), ARCHITECTURE.md (how), TASKS.md (work items), DECISIONS.md (rationale). Inject these every session as persistent ground truth.
- **Application**: ACK scaffold command should generate this canonical 5-file structure. Memory tier templates should match this pattern exactly.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [WORKFLOW] Mandatory Validator Pass
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Run a second pass explicitly validating implementation against original objective, constraints, and acceptance criteria. List deviations explicitly. Never trust first-pass code.
- **Application**: ACK governance should require validator pass before artifact acceptance—compare output vs spec, auto-generate deviation report, block registration if deviations unresolved.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

### [PATTERN] Drift Detection System
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Track four drift types: intent drift (wrong problem), scope creep (added features), architecture drift (broken structure), security drift (weak defaults). Force "What changed? Why?" reconciliation sections.
- **Application**: Build drift detection into ACK validation—compare artifacts against original spec, flag additions/removals, require explicit justification for any deviation from locked plan.
- **Effort**: high | **Impact**: high
- **Status**: backlog

### [TECHNIQUE] Self-Critique and Adversarial Prompts
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Use targeted prompts like "Top 3 ways this could fail?" and "What would a hostile senior engineer flag?" to surface weaknesses before they become problems.
- **Application**: Include self-critique prompts in ACK validation workflow—auto-inject adversarial review questions, capture responses as governance metadata on artifacts.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [WORKFLOW] Custom Skills Enable Tab Completion
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: When workflows and skills are structured in CLAUDE.md, Claude Code predicts and completes next expected prompts via tab. Finely segmented custom skills chain task completions automatically.
- **Application**: ACK slash commands and skills should be designed for tab-completion predictability—structured naming conventions enable Claude to predict next governance step in workflow.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [TECHNIQUE] Commit Before Worktrees
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Always commit changes before creating Git worktrees to avoid carrying uncommitted state into experiments. Prevents cross-contamination between parallel tasks.
- **Application**: ACK worktree documentation should enforce commit-first rule. Validation scripts could warn if uncommitted changes exist before worktree creation.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [ARCHITECTURE] Global vs Project Instruction Files
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Maintain global `.claude/CLAUDE.md` for cross-project rules/preferences, separate from project-level CLAUDE.md. Enables consistent behavior across all projects.
- **Application**: ACK memory tier should distinguish global rules (user preferences, tool configs) from project rules (architecture, domain). Ship both templates.
- **Effort**: low | **Impact**: high
- **Status**: backlog

### [INTEGRATION] Multi-Model Orchestration Layer
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: Coordinate multiple AI CLIs (Claude, Gemini, Codex) within containers, with one interface managing model selection, data routing, and result aggregation. Claude handles orchestration without manual terminal switching.
- **Application**: Design ACK to support multi-model validation pipelines—route different artifact types to specialized models, aggregate governance results, enable fallback chains when primary model unavailable.
- **Effort**: high | **Impact**: high
- **Status**: backlog

### [TECHNIQUE] Conversation Cloning for Exploration
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: Duplicate conversations with new UUIDs to explore alternative approaches while preserving original threads. Enables safe experimentation without losing working state.
- **Application**: ACK memory system should support session branching—clone artifact validation state to test alternative governance rules, merge successful experiments back to main workflow.
- **Effort**: medium | **Impact**: high
- **Status**: backlog

---

## Medium Priority

### [PATTERN] Plan Mode Before Execution
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Demoted**: 2026-01-04 - Native Claude Code feature exists
- **Description**: Two-phase interaction where AI analyzes and proposes changes first, awaiting human approval before executing modifications.
- **Application**: Document ACK-specific plan-review patterns for artifact deployments; leverage native plan mode rather than reimplementing.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [INTEGRATION] Bash Command Injection via Prefix
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Rejected**: 2026-01-04 - Native Claude Code feature, nothing to implement
- **Description**: Lightweight `!` syntax to execute commands instantly without token overhead, keeping AI context focused on reasoning.
- **Application**: N/A - use native `!` prefix in Claude Code directly.
- **Effort**: low | **Impact**: medium
- **Status**: rejected

### [TECHNIQUE] Headless Mode for Automation
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Description**: Non-interactive CLI execution (`-p` flag) allowing AI to work in pipelines and scripts with output directed to stdout.
- **Application**: Enable ACK to run as CI/CD step: validate against governance rules, register artifacts, output results for downstream stages.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

### [PATTERN] Reversible Conversation Checkpoints
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 2025-12-28
- **Description**: Rewind feature preserves conversation history while discarding speculative changes, enabling safe exploration.
- **Application**: Implement transaction-like semantics for ACK artifact modifications: checkpoint before changes, rollback if validation fails.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

### [INTEGRATION] MCP Config in Version Control
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Check `.mcp.json` into git for tool integrations (Slack, BigQuery, Sentry, etc.). Team shares consistent tooling setup.
- **Application**: ACK should generate and manage `.mcp.json` templates with governance-related MCP servers pre-configured for artifact validation and registry access.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [TECHNIQUE] Git Worktrees for Parallel Tasks
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 2026-01-02
- **Description**: Use git worktrees to run parallel Claude tasks on the same repo without branch conflicts, enabling isolated experimentation.
- **Application**: Document worktree workflow for ACK development—run governance experiments in isolated worktrees, validate before merging to main registry.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [WORKFLOW] Cross-Platform Session Handoff
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Start Claude sessions from iOS app in morning, hand off between terminal/web using `&` backgrounding or `--teleport`. Enables async workflows across devices without losing context.
- **Application**: Document ACK session continuity patterns—support workflows where governance checks start on mobile, continue on desktop, with artifact state preserved across handoffs.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [TECHNIQUE] Sandbox Permission Mode
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026) - Detailed Thread
- **Added**: 2026-01-02
- **Description**: Use `--permission-mode=dontAsk` in sandboxed environments to prevent blocking on prompts during automated/long-running tasks while maintaining safety in production.
- **Application**: ACK CI/CD pipelines should run in sandbox mode with dontAsk permissions, while interactive sessions maintain approval gates for governance mutations.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [WORKFLOW] Pre-Rollover Context Summary
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: Before long sessions end, have Claude summarize decisions, assumptions, and open questions. Write summaries back into docs to preserve context across session boundaries.
- **Application**: ACK should prompt for context summary when session length threshold reached—auto-generate DECISIONS.md updates, capture open questions for next session bootstrap.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

### [PATTERN] One Task Per Turn Execution
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 2026-01-01
- **Description**: During execution phase, process one task per turn rather than batching. Enables validation checkpoints and prevents cascading errors from compounding.
- **Application**: ACK complex workflows should decompose into single-task steps with validation gates between each—fail fast on first error rather than batch-failing at end.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [TECHNIQUE] Explore Sub-Agent for Codebase Navigation
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Built-in `Explore` sub-agent aggressively searches codebases with glob/grep patterns. Faster than manual file-by-file exploration for large projects.
- **Application**: ACK validation workflows should leverage Explore sub-agent to find related artifacts, check for naming conflicts, and verify registry consistency across codebase.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [TECHNIQUE] Cut System Prompt in Half
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Shorter system prompts lead to cleaner output and faster responses. Conciseness improves model focus and reduces token overhead.
- **Application**: ACK governance rules should be concise—use bullet constraints over prose, eliminate redundancy, aim for minimal effective instruction set.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [INTEGRATION] Container Isolation for Reproducibility
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Run Claude Code in containers to isolate environments for reproducible setups. Ensures consistent behavior across team members and CI/CD.
- **Application**: Ship ACK with Dockerfile template that includes pre-configured governance rules, registry access, and validation tools for consistent team environments.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

### [INTEGRATION] OpenTelemetry Metrics Exposure
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 2026-01-03
- **Description**: Claude Code CLI exposes OpenTelemetry metrics for performance monitoring. Enables tracking of usage patterns, latency, and resource consumption.
- **Application**: ACK governance layer could emit custom metrics—validation pass/fail rates, drift detection frequency, artifact registration latency for observability dashboards.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

### [WORKFLOW] Voice-First Development Interface
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: Use local voice transcription (SuperWhisper, MacWhisper) to communicate with Claude faster than typing. Works in shared spaces with whispered input through earphones.
- **Application**: Document voice-to-ACK workflow patterns—voice commands for artifact validation, governance queries, and registry operations enable hands-free development while coding.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [PATTERN] Context Freshness via Conversation Cycling
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: AI performance degrades as conversation context accumulates. Start fresh conversations for distinct topics or when quality declines, treating context like perishable goods.
- **Application**: ACK memory design should optimize for context freshness—segment governance state by artifact type, enable quick session bootstrap from minimal memory rather than full history replay.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [TECHNIQUE] Exponential Backoff for Long Operations
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: Implement exponential backoff polling (1min, 2min, 4min) for long-running operations. More token-efficient than continuous output streams for CI/CD monitoring.
- **Application**: ACK registry operations and batch validations should use exponential backoff status checks—reduce token overhead during lengthy artifact processing pipelines.
- **Effort**: low | **Impact**: medium
- **Status**: backlog

### [PATTERN] Abstraction Level Navigation
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2026-01-04
- **Description**: Balance between high-level "vibe coding" for non-critical work and detailed inspection for critical systems. Adjust depth contextually—Claude guides navigation between overview and granular levels.
- **Application**: ACK governance should support variable validation depth—lightweight checks for experimental artifacts, exhaustive validation for production registrations, with explicit abstraction markers.
- **Effort**: medium | **Impact**: medium
- **Status**: backlog

---

## Changelog

### 2026-01-04
- **Source**: Internal planning session
- **Added**: 1 high priority (Artifact Governance System)
- **Plan saved**: `docs/plans/artifact-governance.md`

### 2026-01-04 (Curation)
- **Reviewed**: 7 oldest items (from adocomplete.com/advent-of-claude-2025/)
- **Demoted**: Plan Mode Before Execution (high → medium) - native Claude Code feature
- **Rejected**: Bash Command Injection via Prefix - native Claude Code feature
- **Kept**: 5 items unchanged

### 2026-01-04
- **Source**: https://www.linkedin.com/pulse/32-claude-code-tips-from-basics-advanced-yk-sugi-kexec
- **Added**: 2 high priority, 4 medium priority
- **Skipped**: 25 duplicates (covered by existing entries)
- **New insights**: Multi-Model Orchestration Layer, Conversation Cloning for Exploration, Voice-First Development Interface, Context Freshness via Conversation Cycling, Exponential Backoff for Long Operations, Abstraction Level Navigation

### 2026-01-03
- **Source**: Reddit r/ClaudeCode Top 20 Tips (Jan 2026)
- **Added**: 3 high priority, 4 medium priority
- **New insights**: Custom Skills Enable Tab Completion, Commit Before Worktrees, Global vs Project Instruction Files, Explore Sub-Agent for Codebase Navigation, Cut System Prompt in Half, Container Isolation for Reproducibility, OpenTelemetry Metrics Exposure

### 2026-01-02
- **Source**: Boris Cherny - Claude Code Tips (Jan 2026)
- **Added**: 9 high priority, 4 medium priority
- **New insights**: Parallel Claude Execution, Shared CLAUDE.md with Mistakes Log, Slash Commands for Workflows, Subagents for Specialized Tasks, Stop Hooks for Auto-Resume, PR Review with @claude Tagging, Inline Bash Pre-computation, Verification as Quality Multiplier, Team Knowledge Compounding, MCP Config in Version Control, Git Worktrees for Parallel Tasks, Cross-Platform Session Handoff, Sandbox Permission Mode

### 2026-01-01
- **Source**: X Posts Cheat Sheet (Dec 2025 – Jan 2026)
- **Added**: 5 high priority, 2 medium priority
- **New insights**: Spec-Driven Constrained Executor, Minimal Starter File Set, Mandatory Validator Pass, Drift Detection System, Self-Critique and Adversarial Prompts, Pre-Rollover Context Summary, One Task Per Turn Execution

### 2025-12-28
- **Source**: https://adocomplete.com/advent-of-claude-2025/
- **Added**: 4 high priority, 3 medium priority
- **New insights**: Project Self-Onboarding via Init, Hierarchical Context Management, Plan Mode Before Execution, Hooks for Deterministic Control, Bash Command Injection via Prefix, Headless Mode for Automation, Reversible Conversation Checkpoints
