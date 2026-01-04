#!/bin/bash
# Hook: track-implementation.sh
# Event: PostToolUse (Write|Edit)
# Purpose: Track implementation progress by updating state file
#
# Triggered when: After Write or Edit tool operations
# Updates: implementation-state.json with file changes and timestamps
# Detects: Task completion (when tasks.md is modified)

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

STATE_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation-state.json"
TASKS_FILE="${CLAUDE_PROJECT_DIR}/.ipe/implementation/tasks.md"
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/hooks/track-implementation.log"
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
# Initialize State File (if needed)
# ============================================================================

if [ ! -f "${STATE_FILE}" ]; then
    log "State file not found, creating initial state"
    mkdir -p "$(dirname "${STATE_FILE}")"
    
    cat > "${STATE_FILE}" <<EOF
{
  "current_task": null,
  "files_modified": [],
  "tasks_completed": [],
  "last_updated": null,
  "session_start": "${TIMESTAMP}",
  "total_file_changes": 0
}
EOF
fi

# Check jq is available
if ! command -v jq &> /dev/null; then
    error "jq is required but not installed. Install with: brew install jq"
fi

# ============================================================================
# Parse Hook Input
# ============================================================================

input=$(cat)
log "Received input"

# Extract relevant information
tool_name=$(echo "$input" | jq -r '.tool_name // ""')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // ""')

if [ -z "$file_path" ]; then
    log "No file_path in input, skipping tracking"
    exit 0
fi

# Make path relative to project root
file_path=${file_path#"${CLAUDE_PROJECT_DIR}/"}

log "Tracking change: ${tool_name} on ${file_path}"

# ============================================================================
# Update State File
# ============================================================================

# Add file to modified list (if not already there)
jq --arg file "$file_path" --arg time "$TIMESTAMP" '
    .files_modified |= (
        if . == null then [$file]
        elif (. | index($file)) then .
        else . + [$file]
        end
    ) |
    .last_updated = $time |
    .total_file_changes += 1
' "${STATE_FILE}" > "${STATE_FILE}.tmp" && \
    mv "${STATE_FILE}.tmp" "${STATE_FILE}"

log "Updated state file with file change"

# ============================================================================
# Detect Task Completion
# ============================================================================

# Check if tasks.md was modified
if [ "$file_path" == "$(echo ${TASKS_FILE#"${CLAUDE_PROJECT_DIR}/"} | sed 's|^/||')" ] || \
   [ "$file_path" == ".ipe/implementation/tasks.md" ]; then
    
    log "tasks.md was modified, checking for task completions"
    
    # Extract newly completed tasks
    # Look for tasks marked complete that aren't in state file yet
    if [ -f "${TASKS_FILE}" ]; then
        # Get list of completed tasks from tasks.md
        completed_in_file=$(grep -A5 "^### TASK-" "${TASKS_FILE}" | \
                           grep -B1 "Status: ✅ Complete" | \
                           grep "^### TASK-" | \
                           sed -E 's/^### (TASK-[0-9]+).*/\1/' || echo "")
        
        if [ -n "$completed_in_file" ]; then
            log "Found completed tasks in tasks.md"
            
            # Get already tracked completed tasks
            already_completed=$(jq -r '.tasks_completed[]? // ""' "${STATE_FILE}" 2>/dev/null || echo "")
            
            # Find new completions
            while IFS= read -r task_id; do
                if [ -n "$task_id" ]; then
                    # Check if task already tracked
                    if ! echo "$already_completed" | grep -q "^${task_id}$"; then
                        log "New task completion detected: ${task_id}"
                        
                        # Extract task details from tasks.md
                        task_title=$(grep -A2 "^### ${task_id}" "${TASKS_FILE}" | \
                                    grep "^Title:" | \
                                    sed 's/^Title: //' || echo "Unknown")
                        
                        # Add to state file
                        jq --arg id "$task_id" \
                           --arg title "$task_title" \
                           --arg time "$TIMESTAMP" '
                            .tasks_completed += [{
                                "id": $id,
                                "title": $title,
                                "completed_at": $time
                            }] |
                            .current_task = $id
                        ' "${STATE_FILE}" > "${STATE_FILE}.tmp" && \
                            mv "${STATE_FILE}.tmp" "${STATE_FILE}"
                        
                        log "Added ${task_id} to completed tasks"
                        
                        # Optional: Create git commit
                        if command -v git &> /dev/null && [ -d "${CLAUDE_PROJECT_DIR}/.git" ]; then
                            (
                                cd "${CLAUDE_PROJECT_DIR}"
                                git add "${TASKS_FILE}" "${STATE_FILE}" 2>/dev/null || true
                                git commit -m "[${task_id}] Mark task complete: ${task_title}" 2>/dev/null || true
                                log "Created git commit for task completion"
                            )
                        fi
                        
                        # Output success message
                        echo "✓ Task ${task_id} completion tracked" >&1
                    fi
                fi
            done <<< "$completed_in_file"
        fi
    fi
fi

# ============================================================================
# Update Current Task
# ============================================================================

# Try to detect current task from tasks.md
if [ -f "${TASKS_FILE}" ]; then
    # Find first in-progress task
    current_task=$(grep -A5 "^### TASK-" "${TASKS_FILE}" | \
                  grep -B1 "Status: 🔄 In Progress" | \
                  grep "^### TASK-" | \
                  head -1 | \
                  sed -E 's/^### (TASK-[0-9]+).*/\1/' || echo "null")
    
    if [ "$current_task" != "null" ] && [ -n "$current_task" ]; then
        jq --arg task "$current_task" \
           '.current_task = $task' \
           "${STATE_FILE}" > "${STATE_FILE}.tmp" && \
            mv "${STATE_FILE}.tmp" "${STATE_FILE}"
        
        log "Updated current task to: ${current_task}"
    fi
fi

# ============================================================================
# Cleanup Old Entries (keep last 50 files)
# ============================================================================

file_count=$(jq '.files_modified | length' "${STATE_FILE}")

if [ "$file_count" -gt 50 ]; then
    log "Pruning old file entries (keeping last 50)"
    
    jq '.files_modified |= .[-50:]' \
       "${STATE_FILE}" > "${STATE_FILE}.tmp" && \
        mv "${STATE_FILE}.tmp" "${STATE_FILE}"
fi

# ============================================================================
# Success
# ============================================================================

log "Implementation tracking completed"
exit 0
