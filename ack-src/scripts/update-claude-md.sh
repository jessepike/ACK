#!/bin/bash
# Hook: update-claude-md.sh
# Event: Stop
# Purpose: Update CLAUDE.md active context section with current task state
#
# Triggered when: Agent stops responding (task complete or pause)
# Updates: "Active Context" section in CLAUDE.md with current task info

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CLAUDE_MD="${CLAUDE_PROJECT_DIR}/.claude/CLAUDE.md"
STATE_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation-state.json"
TASKS_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation/tasks.md"

# Logging
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/hooks/update-claude-md.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ============================================================================
# Functions
# ============================================================================

log() {
    echo "[${TIMESTAMP}] $1" >> "${LOG_FILE}"
}

error() {
    echo "ERROR: $1" >&2
    log "ERROR: $1"
    exit 2
}

# ============================================================================
# Validation
# ============================================================================

log "Starting CLAUDE.md update"

# Check required files exist
if [ ! -f "${CLAUDE_MD}" ]; then
    error "CLAUDE.md not found at ${CLAUDE_MD}"
fi

if [ ! -f "${STATE_FILE}" ]; then
    log "WARNING: State file not found, creating minimal state"
    mkdir -p "$(dirname "${STATE_FILE}")"
    echo '{"current_task":null,"files_modified":[],"last_updated":null}' > "${STATE_FILE}"
fi

# Check jq is available
if ! command -v jq &> /dev/null; then
    error "jq is required but not installed. Install with: brew install jq"
fi

# ============================================================================
# Parse Hook Input (optional, not all Stop hooks provide it)
# ============================================================================

input=$(cat)
log "Received input: ${input}"

# ============================================================================
# Read Current State
# ============================================================================

current_task=$(jq -r '.current_task // "None"' "${STATE_FILE}")
files_modified=$(jq -r '.files_modified // [] | join(", ")' "${STATE_FILE}")
last_updated=$(jq -r '.last_updated // "Never"' "${STATE_FILE}")

log "Current task: ${current_task}"
log "Files modified: ${files_modified}"
log "Last updated: ${last_updated}"

# ============================================================================
# Get Task Progress from tasks.md (if exists)
# ============================================================================

task_stats="N/A"
if [ -f "${TASKS_FILE}" ]; then
    total_tasks=$(grep -c "^### TASK-" "${TASKS_FILE}" || echo "0")
    completed_tasks=$(grep -c "Status: ✅ Complete" "${TASKS_FILE}" || echo "0")
    in_progress_tasks=$(grep -c "Status: 🔄 In Progress" "${TASKS_FILE}" || echo "0")
    
    task_stats="$completed_tasks/$total_tasks complete, $in_progress_tasks in progress"
    log "Task statistics: ${task_stats}"
fi

# ============================================================================
# Build Active Context Content
# ============================================================================

active_context=$(cat <<EOF
**Current Task:** ${current_task}  
**Task Progress:** ${task_stats}  
**Recent Files:** ${files_modified:-None}  
**Last Updated:** ${last_updated}

*This section is automatically updated via hooks. See implementation-state.json for details.*
EOF
)

log "Generated active context content"

# ============================================================================
# Update CLAUDE.md
# ============================================================================

# Create a temporary file
tmp_file=$(mktemp)

# Find the Active Context section and replace it
if grep -q "## \[ACTIVE-CONTEXT\]" "${CLAUDE_MD}"; then
    log "Updating existing Active Context section"
    
    # Use awk to replace content between markers
    awk -v content="${active_context}" '
        /^## \[ACTIVE-CONTEXT\]/ {
            print $0
            print ""
            print content
            skip=1
            next
        }
        /^## \[/ && skip {
            skip=0
        }
        !skip
    ' "${CLAUDE_MD}" > "${tmp_file}"
    
else
    log "Active Context section not found, appending to file"
    
    # Append new section before closing
    cat "${CLAUDE_MD}" > "${tmp_file}"
    cat >> "${tmp_file}" <<EOF

---

## [ACTIVE-CONTEXT] - Current Work (Auto-Updated)

${active_context}
EOF
fi

# Validate the temp file is not empty
if [ ! -s "${tmp_file}" ]; then
    error "Generated file is empty, aborting update"
fi

# Replace original with updated version
mv "${tmp_file}" "${CLAUDE_MD}"

log "Successfully updated CLAUDE.md"

# ============================================================================
# Update last modified timestamp in state
# ============================================================================

jq --arg time "${TIMESTAMP}" \
   '.last_updated = $time' \
   "${STATE_FILE}" > "${STATE_FILE}.tmp" && \
   mv "${STATE_FILE}.tmp" "${STATE_FILE}"

log "Updated state file timestamp"

# ============================================================================
# Success
# ============================================================================

echo "✓ CLAUDE.md active context updated" >&1
log "Hook completed successfully"
exit 0
