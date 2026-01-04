#!/bin/bash
# Hook: finalize-stage.sh
# Event: SessionEnd
# Purpose: Mark current stage as complete if all artifacts are finalized
#
# Triggered when: Claude Code session ends
# Checks: Stage artifacts for finalized status
# Updates: CLAUDE.md with stage completion marker

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CLAUDE_MD="${CLAUDE_PROJECT_DIR}/.claude/CLAUDE.md"
IPE_DIR="${CLAUDE_PROJECT_DIR}/.ipe"

# Logging
LOG_FILE="${CLAUDE_PROJECT_DIR}/.claude/hooks/finalize-stage.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TODAY=$(date -u +"%Y-%m-%d")

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

get_current_stage() {
    # Extract current stage from CLAUDE.md
    if [ ! -f "${CLAUDE_MD}" ]; then
        echo "unknown"
        return
    fi
    
    # Look for "Stage X: Name" pattern
    grep -m1 "^Stage [0-9]:" "${CLAUDE_MD}" | \
        sed -E 's/^Stage ([0-9]):.*/\1/' || echo "unknown"
}

get_stage_name() {
    local stage_num=$1
    case $stage_num in
        1) echo "discovery" ;;
        2) echo "solution-design" ;;
        3) echo "environment-setup" ;;
        4) echo "workflow-config" ;;
        5) echo "implementation" ;;
        *) echo "unknown" ;;
    esac
}

check_artifacts_finalized() {
    local stage_dir=$1
    
    if [ ! -d "${stage_dir}" ]; then
        log "Stage directory not found: ${stage_dir}"
        return 1
    fi
    
    # Find all .md files in stage directory
    local total=0
    local finalized=0
    
    while IFS= read -r -d '' file; do
        ((total++))
        
        # Check if file has "status: finalized" in frontmatter
        if grep -q "^status: finalized" "$file" 2>/dev/null; then
            ((finalized++))
            log "✓ Finalized: $(basename "$file")"
        else
            log "✗ Not finalized: $(basename "$file")"
        fi
    done < <(find "${stage_dir}" -name "*.md" -print0)
    
    if [ $total -eq 0 ]; then
        log "No artifacts found in ${stage_dir}"
        return 1
    fi
    
    if [ $finalized -eq $total ]; then
        log "All $total artifacts finalized"
        return 0
    else
        log "Only $finalized of $total artifacts finalized"
        return 1
    fi
}

mark_stage_complete() {
    local stage_num=$1
    local stage_name=$2
    
    # Create completion marker
    local marker="✅ Stage ${stage_num}: ${stage_name} (${TODAY})"
    
    # Check if already marked complete
    if grep -q "${marker}" "${CLAUDE_MD}" 2>/dev/null; then
        log "Stage already marked complete"
        return 0
    fi
    
    # Update CLAUDE.md "Completed Stages" section
    local tmp_file=$(mktemp)
    
    if grep -q "## Completed Stages" "${CLAUDE_MD}"; then
        # Add to existing section
        awk -v marker="${marker}" '
            /^## Completed Stages/ {
                print $0
                getline
                print $0
                print marker
                next
            }
            { print }
        ' "${CLAUDE_MD}" > "${tmp_file}"
    else
        # Create new section
        cat "${CLAUDE_MD}" > "${tmp_file}"
        cat >> "${tmp_file}" <<EOF

---

## Completed Stages
${marker}
EOF
    fi
    
    mv "${tmp_file}" "${CLAUDE_MD}"
    log "Marked stage ${stage_num} as complete in CLAUDE.md"
}

update_current_stage() {
    local next_stage=$1
    
    # Update "Current Stage" section
    local tmp_file=$(mktemp)
    
    sed -E "s/^(Stage: )[0-9].*/\1${next_stage}/" "${CLAUDE_MD}" > "${tmp_file}"
    mv "${tmp_file}" "${CLAUDE_MD}"
    
    log "Updated current stage to ${next_stage}"
}

# ============================================================================
# Main Logic
# ============================================================================

log "Starting stage finalization check"

# Parse hook input
input=$(cat)
log "Received input: ${input}"

# Check required files
if [ ! -f "${CLAUDE_MD}" ]; then
    log "CLAUDE.md not found, skipping finalization"
    exit 0
fi

# Get current stage
current_stage=$(get_current_stage)
log "Current stage: ${current_stage}"

if [ "${current_stage}" == "unknown" ]; then
    log "Could not determine current stage, skipping"
    exit 0
fi

# Get stage name and directory
stage_name=$(get_stage_name "${current_stage}")
stage_dir="${IPE_DIR}/${stage_name}"

log "Checking stage directory: ${stage_dir}"

# Check if all artifacts are finalized
if check_artifacts_finalized "${stage_dir}"; then
    log "All artifacts finalized, marking stage complete"
    
    # Mark stage as complete
    mark_stage_complete "${current_stage}" "${stage_name}"
    
    # Move to next stage (if not already at stage 5)
    if [ "${current_stage}" -lt 5 ]; then
        next_stage=$((current_stage + 1))
        update_current_stage "${next_stage}"
        
        echo "✓ Stage ${current_stage} finalized. Ready for Stage ${next_stage}." >&1
        log "Moved to stage ${next_stage}"
    else
        echo "✓ Stage 5 (Implementation) finalized. Project complete!" >&1
        log "Stage 5 complete - project finished"
    fi
    
    # Optional: Create stage summary
    summary_file="${stage_dir}/stage-summary.txt"
    cat > "${summary_file}" <<EOF
Stage ${current_stage}: ${stage_name}
Finalized: ${TODAY}
Session: $(echo "$input" | jq -r '.session_id // "unknown"')

All artifacts completed and marked as finalized.
EOF
    log "Created stage summary: ${summary_file}"
    
else
    log "Not all artifacts finalized, skipping stage completion"
    echo "Stage ${current_stage} not yet complete. Finalize all artifacts before ending." >&1
fi

log "Hook completed successfully"
exit 0
