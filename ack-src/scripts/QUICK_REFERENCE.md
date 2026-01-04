---
type: guide
description: "ACK Hooks - Quick Reference Card"
version: 0.1.0
updated: "2026-01-04T09:26:12"
---

# ACK Hooks - Quick Reference Card

**Version:** 1.0  
**Stage:** 4 (Workflow Configuration)  
**Component:** Claude Code Hook Scripts

---

## 📦 What's Included

**6 Hook Scripts:**
1. `update-claude-md.sh` - Update active context (Stop hook)
2. `finalize-stage.sh` - Mark stages complete (SessionEnd hook)
3. `inject-stage-context.sh` - Load context at startup (SessionStart hook)
4. `check-structure.sh` - Validate file placement (PostToolUse hook)
5. `track-implementation.sh` - Track state changes (PostToolUse hook)
6. `validate-claude-md.sh` - Manual validation

**3 Helper Scripts:**
1. `configure-hooks.sh` - Auto-configure settings.json
2. `test-hooks.sh` - Test all hooks with sample data
3. `install.sh` - Installation helper

**Documentation:**
1. `README.md` - Complete documentation

---

## 🚀 Quick Start

```bash
# 1. Install hooks
./install.sh

# 2. Configure settings.json
./.claude/hooks/configure-hooks.sh

# 3. Test everything
./.claude/hooks/test-hooks.sh

# 4. Validate setup
./.claude/hooks/validate-claude-md.sh
```

---

## 🔧 Hook Events

| Hook Script | Event | When It Runs | What It Does |
|-------------|-------|--------------|--------------|
| inject-stage-context.sh | SessionStart | Claude Code starts | Shows stage status, loads context |
| update-claude-md.sh | Stop | Agent stops | Updates CLAUDE.md active section |
| finalize-stage.sh | SessionEnd | Session ends | Checks stage completion |
| check-structure.sh | PostToolUse | After Write/Edit | Validates file placement |
| track-implementation.sh | PostToolUse | After Write/Edit | Updates state tracking |

---

## 📋 Manual Commands

```bash
# Validate CLAUDE.md
./.claude/hooks/validate-claude-md.sh

# Test specific hook
./.claude/hooks/test-hooks.sh check-structure

# Manual context update
./.claude/hooks/update-claude-md.sh

# Configure hooks (interactive)
./.claude/hooks/configure-hooks.sh

# Test all hooks
./.claude/hooks/test-hooks.sh
```

---

## 🔍 What Each Hook Does

### SessionStart: inject-stage-context.sh
**Displays:**
- Current stage and progress
- Task statistics
- Recent activity
- Validation results
- Quick reference links

**Example Output:**
```
═══════════════════════════════════════════════════════════════
  ACK Session Context
═══════════════════════════════════════════════════════════════

📍 Current Stage: 5 - Implementation
✅ Completed Stages: 4
📋 Task Progress: 12/45 complete, 3 in progress, 0 blocked
🕐 Recent Activity: Last: 2025-01-02T15:30:00Z | Current: TASK-015

🔍 Context Validation:
✓ All validation checks passed
```

### Stop: update-claude-md.sh
**Updates:**
- Current task from state file
- Task progress counters
- Files modified list
- Last update timestamp

**Updates This Section:**
```markdown
## [ACTIVE-CONTEXT] - Current Work (Auto-Updated)

**Current Task:** TASK-015
**Task Progress:** 12/45 complete, 3 in progress
**Recent Files:** src/api/users.py, tests/test_users.py
**Last Updated:** 2025-01-02T15:30:00Z
```

### SessionEnd: finalize-stage.sh
**Checks:**
- All stage artifacts finalized?
- Adds completion marker to CLAUDE.md
- Moves to next stage
- Creates stage summary

**Adds:**
```markdown
## Completed Stages
✅ Stage 1: discovery (2025-01-01)
✅ Stage 2: solution-design (2025-01-02)
```

### PostToolUse: check-structure.sh
**Validates:**
- No source in root (except entry points)
- Source code in src/ only
- Tests mirror src structure
- File in allowed directory
- Naming conventions
- File size warnings

**Blocks:**
```bash
🚫 CRITICAL: Source code not allowed in root: users.py. Move to src/
```

**Warns:**
```bash
⚠️  WARNING: Test structure doesn't mirror src: tests/api/test_users.py vs src/users.py
```

### PostToolUse: track-implementation.sh
**Updates:**
- Files modified list
- Current task detection
- Task completion tracking
- Auto-commits task completions

**Updates State File:**
```json
{
  "current_task": "TASK-015",
  "files_modified": ["src/api/users.py", "tests/test_users.py"],
  "tasks_completed": [
    {"id": "TASK-012", "title": "Auth service", "completed_at": "..."}
  ],
  "last_updated": "2025-01-02T15:30:00Z",
  "total_file_changes": 47
}
```

### Manual: validate-claude-md.sh
**Checks:**
- Required sections exist
- Token budget under limit
- Imports reference existing files
- No syntax errors
- Content quality
- Stage consistency

**Output:**
```
═══════════════════════════════════════════════════════════════
  CLAUDE.md Validation Report
═══════════════════════════════════════════════════════════════

✓ CLAUDE.md file exists
✓ Found: ## Current Stage
✓ Found: ## Completed Stages
✓ Under target (20000 tokens)
✓ All imports valid
✓ No syntax errors
✓ Stage consistency verified

  ✓ VALIDATION PASSED
```

---

## 🎯 Use Cases

### Starting a Session
**Hook:** SessionStart → inject-stage-context.sh  
**Result:** See stage status, progress, next actions

### Completing a Task
**Hook:** PostToolUse → track-implementation.sh  
**Result:** Auto-tracked when tasks.md updated, git commit created

### Pausing Work
**Hook:** Stop → update-claude-md.sh  
**Result:** Progress saved to CLAUDE.md active context

### Ending a Stage
**Hook:** SessionEnd → finalize-stage.sh  
**Result:** Stage marked complete, moved to next

### Creating a File
**Hook:** PostToolUse → check-structure.sh  
**Result:** Validates placement, blocks violations

### Manual Validation
**Command:** validate-claude-md.sh  
**Result:** Full validation report

---

## 🐛 Troubleshooting

### Hooks not running
```bash
# Check configuration
cat .claude/settings.json | jq .hooks

# Verify scripts executable
ls -la .claude/hooks/*.sh

# Test manually
./.claude/hooks/update-claude-md.sh
```

### Permission errors
```bash
# Make executable
chmod +x .claude/hooks/*.sh
```

### JSON errors
```bash
# Install jq
brew install jq  # macOS
sudo apt-get install jq  # Linux

# Test jq
echo '{"test":"value"}' | jq .
```

### CLAUDE.md not updating
```bash
# Check file exists and writable
test -w .claude/CLAUDE.md && echo "OK" || echo "Not writable"

# Run validation
./.claude/hooks/validate-claude-md.sh

# Check logs
tail -f .claude/hooks/*.log
```

---

## 📁 File Structure

```
.claude/
├── CLAUDE.md                  # Auto-generated context (DO NOT EDIT)
├── claude.md                  # Agent behavior rules
├── settings.json              # Hook configuration
└── hooks/
    ├── README.md              # Full documentation
    ├── install.sh             # Installation helper
    ├── configure-hooks.sh     # Settings configurator
    ├── test-hooks.sh          # Testing suite
    ├── update-claude-md.sh    # Stop hook
    ├── finalize-stage.sh      # SessionEnd hook
    ├── inject-stage-context.sh # SessionStart hook
    ├── check-structure.sh     # PostToolUse hook
    ├── track-implementation.sh # PostToolUse hook
    ├── validate-claude-md.sh  # Manual validation
    └── *.log                  # Hook execution logs
```

---

## 🔐 Security Notes

**Hooks have access to:**
- Read/write CLAUDE.md
- Read/write implementation-state.json
- Read repo-structure.md
- Execute git commands

**Best practices:**
- Keep hooks in `.claude/hooks/` only
- No network access in hooks
- Validate all JSON input
- Use `set -euo pipefail` for safety
- Log all operations

---

## 📚 Related Documentation

- [Stage 4 Specification](../Stage_4_Workflow_Configuration_Specification.md)
- [CLAUDE.md Integration](../ACK_CLAUDE_Memory_Integration.md)
- [Context Management](../.ipe/workflow-config/context-management.md)
- [Repository Structure](../.ipe/environment-setup/repo-structure.md)

---

## 💡 Tips

**For Development:**
- Test hooks with `test-hooks.sh` before using
- Check logs in `.claude/hooks/*.log`
- Use `--dry-run` with configure-hooks.sh

**For Debugging:**
- Add `set -x` to top of hook for verbose output
- Pipe to log file: `exec >> /tmp/hook.log 2>&1`
- Test with sample JSON: `echo '{}' | ./hook.sh`

**For Performance:**
- Hooks run synchronously - keep them fast
- Minimize external commands
- Cache expensive operations
- Prune old data regularly

---

**Support:** See README.md for detailed documentation  
**Issues:** Check troubleshooting section first  
**Updates:** Version in header, check for latest
