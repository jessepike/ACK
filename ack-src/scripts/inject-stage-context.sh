#!/bin/bash
# Hook: inject-stage-context.sh
# Event: SessionStart
# Purpose: Load stage context and display current status at session start
#
# Triggered when: Claude Code session starts
# Displays: Current stage, recent progress, validation results
# Loads: claude-mem observations (if available)

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CLAUDE_MD="${CLAUDE_PROJECT_DIR}/.claude/CLAUDE.md"
STATE_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation-state.json"
TASKS_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation/tasks.md"

# Logging
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/hooks/inject-context.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ============================================================================
# Functions
# ============================================================================

log() {
    echo "[${TIMESTAMP}] $1" >> "${LOG_FILE}"
}

get_current_stage() {
    if [ ! -f "${CLAUDE_MD}" ]; then
        echo "Unknown"
        return
    fi
    
    # Extract stage number and name
    grep -m1 "^Stage [0-9]:" "${CLAUDE_MD}" | \
        sed -E 's/^Stage ([0-9]): (.*)/\1 - \2/' || echo "Unknown"
}

get_completed_stages() {
    if [ ! -f "${CLAUDE_MD}" ]; then
        echo "None"
        return
    fi
    
    # Count completed stages
    grep -c "^✅ Stage" "${CLAUDE_MD}" 2>/dev/null || echo "0"
}

get_task_stats() {
    if [ ! -f "${TASKS_FILE}" ]; then
        echo "No tasks file found"
        return
    fi
    
    local total=$(grep -c "^### TASK-" "${TASKS_FILE}" 2>/dev/null || echo "0")
    local complete=$(grep -c "Status: ✅ Complete" "${TASKS_FILE}" 2>/dev/null || echo "0")
    local in_progress=$(grep -c "Status: 🔄 In Progress" "${TASKS_FILE}" 2>/dev/null || echo "0")
    local blocked=$(grep -c "Status: 🚫 Blocked" "${TASKS_FILE}" 2>/dev/null || echo "0")
    
    echo "${complete}/${total} complete, ${in_progress} in progress, ${blocked} blocked"
}

get_recent_activity() {
    if [ ! -f "${STATE_FILE}" ]; then
        echo "No recent activity"
        return
    fi
    
    local last_updated=$(jq -r '.last_updated // "Never"' "${STATE_FILE}")
    local current_task=$(jq -r '.current_task // "None"' "${STATE_FILE}")
    local file_count=$(jq -r '.files_modified | length' "${STATE_FILE}" 2>/dev/null || echo "0")
    
    echo "Last: ${last_updated} | Current: ${current_task} | Files: ${file_count}"
}

validate_context() {
    local issues=0
    
    # Check CLAUDE.md exists
    if [ ! -f "${CLAUDE_MD}" ]; then
        echo "⚠️  CLAUDE.md not found"
        ((issues++))
    fi
    
    # Check token budget (rough estimate: 1 char ≈ 0.25 tokens)
    if [ -f "${CLAUDE_MD}" ]; then
        local chars=$(wc -c < "${CLAUDE_MD}")
        local tokens=$((chars / 4))
        
        if [ $tokens -gt 20000 ]; then
            echo "⚠️  CLAUDE.md may exceed token budget (~${tokens} tokens)"
            ((issues++))
        fi
    fi
    
    # Check for broken imports
    if [ -f "${CLAUDE_MD}" ]; then
        while IFS= read -r import_path; do
            local full_path="${CLAUDE_PROJECT_DIR}/${import_path}"
            if [ ! -f "${full_path}" ]; then
                echo "⚠️  Broken import: ${import_path}"
                ((issues++))
            fi
        done < <(grep "^@" "${CLAUDE_MD}" | sed 's/@//' || true)
    fi
    
    return $issues
}

check_claude_mem() {
    # Check if claude-mem plugin is available
    if command -v mem-search &> /dev/null || [ -d "${CLAUDE_PROJECT_DIR}/.claude-mem" ]; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# Main Display
# ============================================================================

log "Starting session context injection"

# Parse hook input
input=$(cat)
session_id=$(echo "$input" | jq -r '.session_id // "unknown"')

log "Session ID: ${session_id}"

# ============================================================================
# Build and Display Context Summary
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  IPE Session Context"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Current Stage
current_stage=$(get_current_stage)
echo "📍 Current Stage: ${current_stage}"
log "Current stage: ${current_stage}"

# Completed Stages
completed=$(get_completed_stages)
echo "✅ Completed Stages: ${completed}"
log "Completed stages: ${completed}"

# Task Progress (if in Stage 5)
if echo "${current_stage}" | grep -q "^5"; then
    task_stats=$(get_task_stats)
    echo "📋 Task Progress: ${task_stats}"
    log "Task stats: ${task_stats}"
fi

# Recent Activity
recent=$(get_recent_activity)
echo "🕐 Recent Activity: ${recent}"
log "Recent activity: ${recent}"

echo ""
echo "───────────────────────────────────────────────────────────────"
echo ""

# ============================================================================
# Validation
# ============================================================================

echo "🔍 Context Validation:"
echo ""

if validate_context; then
    echo "✓ All validation checks passed"
    log "Validation: PASSED"
else
    echo ""
    echo "Review warnings above. Run: .claude/hooks/validate-claude-md.sh"
    log "Validation: WARNINGS"
fi

echo ""
echo "───────────────────────────────────────────────────────────────"
echo ""

# ============================================================================
# Claude-mem Integration (if available)
# ============================================================================

if check_claude_mem; then
    echo "💾 Loading implementation history (claude-mem)..."
    log "claude-mem available"
    
    # Query recent observations
    # Note: Actual implementation depends on claude-mem plugin
    echo ""
    echo "Recent observations available via:"
    echo "  - mem-search skill"
    echo "  - Query: 'What did we do last session?'"
    echo "  - Query: 'Show recent task completions'"
    echo ""
else
    log "claude-mem not available"
fi

# ============================================================================
# Quick Links
# ============================================================================

echo "📚 Quick Reference:"
echo ""
echo "  Current stage artifacts:"

# List current stage directory based on stage number
stage_num=$(echo "${current_stage}" | grep -oE "^[0-9]")
case $stage_num in
    1) echo "    .ipe/discovery/" ;;
    2) echo "    .ipe/solution-design/" ;;
    3) echo "    .ipe/environment-setup/" ;;
    4) echo "    .ipe/workflow-config/" ;;
    5) echo "    .ipe/implementation/" ;;
esac

echo ""
echo "  Configuration:"
echo "    .claude/CLAUDE.md - Project context"
echo "    .claude/claude.md - Agent behavior rules"
echo "    .claude/settings.json - Hook configuration"
echo ""

# ============================================================================
# Next Actions (Stage-Specific)
# ============================================================================

echo "🎯 Next Actions:"
echo ""

case $stage_num in
    1)
        echo "  → Complete discovery artifacts"
        echo "  → Interview stakeholders"
        echo "  → Finalize requirements"
        ;;
    2)
        echo "  → Design solution architecture"
        echo "  → Select technology stack"
        echo "  → Define data models"
        ;;
    3)
        echo "  → Set up development environment"
        echo "  → Configure tools and dependencies"
        echo "  → Establish repository structure"
        ;;
    4)
        echo "  → Define workflows and processes"
        echo "  → Configure agent behavior"
        echo "  → Set up automation hooks"
        ;;
    5)
        echo "  → Check .ipe/implementation/tasks.md"
        echo "  → Continue with current task"
        echo "  → Mark tasks complete as you go"
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# CLAUDE.md Loading
# ============================================================================

# CLAUDE.md is automatically loaded by Claude Code
# This hook just provides the summary display

log "Context injection completed"
log "Session ready"

exit 0
