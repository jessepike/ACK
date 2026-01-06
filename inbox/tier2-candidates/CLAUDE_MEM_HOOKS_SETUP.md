# Claude-Mem Hooks Installation Guide

**Quick reference for setting up automatic observation capture**

---

## Prerequisites

1. **claude-mem CLI installed**
   ```bash
   npm install -g claude-mem
   ```

2. **Verify installation**
   ```bash
   which claude-mem
   # Should output: /path/to/bin/claude-mem
   ```

---

## Installation Steps

### Step 1: Run Installer

```bash
claude-mem install
```

### Step 2: Choose Scope

The installer will prompt: **"Install globally or per-project?"**

**Options:**
- **Global** - Captures ALL Claude Code sessions system-wide
- **Project** - Captures only for specific directories (RECOMMENDED)

**Recommendation:** Choose **Project** to avoid capturing unrelated Claude Code work.

### Step 3: Select Projects

When prompted, enter the full paths to projects you want to track:

```
/Users/jessepike/code/sandbox/project-studio
/Users/jessepike/code/sandbox/vet-books
```

**Tips:**
- Use absolute paths (not relative)
- One path per line
- Press Enter after each path
- Type "done" or Ctrl+D when finished

### Step 4: Verify Installation

```bash
claude-mem status
```

**Expected Output:**
```
✓ Hooks installed for:
  - /Users/jessepike/code/sandbox/project-studio
  - /Users/jessepike/code/sandbox/vet-books
✓ Status: Active
✓ Database: ~/.claude-mem/claude-mem.db
```

---

## What Gets Created

### Hook Scripts
Location: `~/.claude-mem/hooks/`

Files:
- `pre-prompt.sh` - Runs before Claude responds
- `post-response.sh` - Runs after Claude completes action

These scripts:
- Capture tool usage (reads, writes, bash commands)
- Compress observations via AI (~500 tokens each)
- Store in SQLite database

### Claude Code Settings
Location: `~/.claude/settings.json`

Added configuration:
```json
{
  "hooks": {
    "enabled": true,
    "paths": [
      "/Users/jessepike/code/sandbox/project-studio",
      "/Users/jessepike/code/sandbox/vet-books"
    ]
  }
}
```

### Database
Location: `~/.claude-mem/claude-mem.db`

Tables:
- `sessions` - Work session metadata
- `observations` - Compressed agent activity
- `prompts` - User prompts

---

## How It Works

### Automatic Capture Flow

1. **You start Claude Code** in `/Users/jessepike/code/sandbox/project-studio`
2. **You ask Claude** to implement a feature
3. **Claude writes code**, runs tests, fixes bugs
4. **claude-mem hooks capture** each action:
   - File reads/writes
   - Bash commands
   - Decision points
5. **AI compresses** raw data into observations (~500 tokens)
6. **Stored in database** with type, narrative, file path, timestamp
7. **Project Studio polls** database every 10 seconds (configurable)
8. **Observations appear** in Dashboard ObservationFeed

**Zero manual intervention required** after setup.

---

## Project Studio Integration

### Enable Polling

1. Open **Project Studio**
2. Navigate to **Settings**
3. Scroll to **Claude-Mem Integration**
4. Toggle **"Auto-refresh Observations"** → ON
5. Set **Polling Interval** (default: 10 seconds)

### View Observations

**Dashboard:**
- Scroll to bottom → "Agent Activity" card
- Shows recent observations across all projects
- Refresh button for manual updates

**Project View:**
- Open a project with `repo_path` set
- Observations filtered to that project only

### Observation Types

Displayed with color-coded icons:

- 🔀 **Decision** (purple) - Architectural choices
- 🐛 **Bugfix** (red) - Bug fixes
- ⚡ **Feature** (green) - New functionality
- 🔄 **Refactor** (blue) - Code improvements
- 💡 **Discovery** (yellow) - New insights
- 📄 **Change** (gray) - Generic changes

### Promote to Learning

**Workflow:**
1. Find valuable observation in feed
2. Click **↑** (promote button)
3. **CaptureLearningModal** opens pre-filled:
   - Title: observation concept
   - Problem: observation narrative
   - Tags: observation type
4. Add **Solution** field
5. Click **Save**
6. Learning appears with **"From Agent"** badge

---

## Troubleshooting

### Issue: Observations not appearing

**Checks:**
1. Verify hooks installed:
   ```bash
   claude-mem status
   ```

2. Check database exists:
   ```bash
   ls ~/.claude-mem/claude-mem.db
   ```

3. Ensure Project Studio polling enabled:
   - Settings → Claude-Mem Integration → Auto-refresh ON

4. Restart Claude Code:
   - Hooks may not activate until restart

### Issue: Wrong project observations showing

**Problem:** Observations from wrong project appearing

**Fix:**
- Set `repo_path` in Project Studio project settings
- Observations are filtered by file path matching
- Ensure repo_path exactly matches claude-mem session project_path

### Issue: Hooks not capturing

**Problem:** Working in Claude Code but no observations captured

**Checks:**
1. Verify you're in a tracked directory:
   ```bash
   pwd
   # Should match one of your configured paths
   ```

2. Check hooks are active:
   ```bash
   claude-mem status
   # Should show "Status: Active"
   ```

3. Try manual capture test:
   ```bash
   claude-mem save "Test observation"
   ```

4. Restart Claude Code

### Issue: Database locked

**Problem:** "Database is locked" error

**Fix:**
- Close all instances of Project Studio
- Close claude-mem web viewer (if running)
- Restart Project Studio
- claude-mem database opens read-only (shouldn't lock)

---

## Maintenance

### View Captured Data

**CLI:**
```bash
# List recent observations
sqlite3 ~/.claude-mem/claude-mem.db "SELECT * FROM observations ORDER BY created_at DESC LIMIT 10"

# Count observations
sqlite3 ~/.claude-mem/claude-mem.db "SELECT COUNT(*) FROM observations"

# List sessions
sqlite3 ~/.claude-mem/claude-mem.db "SELECT * FROM sessions"
```

**Web Viewer (if available):**
```bash
# Start web viewer
claude-mem serve

# Open browser to http://localhost:37777
```

### Backup Database

```bash
# Backup claude-mem database
cp ~/.claude-mem/claude-mem.db ~/.claude-mem/claude-mem-backup-$(date +%Y%m%d).db

# Backup Project Studio database
cp ~/Library/Application\ Support/project-studio/project-studio-data/studio.db ~/Desktop/studio-backup-$(date +%Y%m%d).db
```

### Uninstall Hooks

```bash
# Remove hooks (stops capturing)
claude-mem uninstall

# Verify
claude-mem status
# Should show "Hooks not installed"
```

---

## Advanced Configuration

### Custom Database Path

**Override default location:**

In Project Studio Settings (future feature):
```
claude_mem_db_path: /custom/path/to/claude-mem.db
```

Currently uses default: `~/.claude-mem/claude-mem.db`

### Polling Intervals

**Available options:**
- 5 seconds - Very responsive, higher overhead
- 10 seconds - **Default**, balanced
- 30 seconds - Less frequent, lower overhead
- 60 seconds - Minimal overhead, delayed updates

**Set in Settings → Claude-Mem Integration → Polling Interval**

### Visibility Detection

**Automatic behavior:**
- Polling **pauses** when window minimized or hidden
- Polling **resumes** when window restored
- Saves resources during inactive periods
- No configuration needed (built-in)

---

## Next Steps

After hooks are installed and working:

1. **Start a Claude Code session** in a tracked project
2. **Work normally** - ask Claude to implement features
3. **Check Project Studio Dashboard** - observations should appear
4. **Review observations** - look for valuable insights
5. **Promote to learnings** - convert good observations to permanent knowledge
6. **Build memory library** - accumulate learnings over time

---

## Reference Links

- **Project Studio Documentation:** `docs/FEATURES.md`
- **Polling Implementation:** `docs/CLAUDE_MEM_POLLING_IMPLEMENTATION.md`
- **Testing Guide:** `docs/TESTING_GUIDE_CLAUDE_MEM_POLLING.md`
- **Project Context:** `claude.md`

---

**Last Updated:** 2025-12-29
