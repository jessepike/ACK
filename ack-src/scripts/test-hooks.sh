#!/bin/bash
# Helper: test-hooks.sh
# Purpose: Test all IPE hooks with sample data
#
# Usage: ./test-hooks.sh [hook-name]
# Tests: All hooks or specific hook with sample input

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

HOOKS_DIR="${CLAUDE_PROJECT_DIR}/.claude/hooks"
TEST_DIR="${CLAUDE_PROJECT_DIR}/.claude/hooks/test-data"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# Functions
# ============================================================================

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# ============================================================================
# Create Test Data
# ============================================================================

setup_test_data() {
    mkdir -p "${TEST_DIR}"
    
    # Sample PostToolUse input (Write operation)
    cat > "${TEST_DIR}/post-tool-write.json" <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/transcript.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "src/api/users.py",
    "content": "# User API endpoints\n"
  },
  "tool_use_id": "toolu_test123"
}
EOF

    # Sample PostToolUse input (Edit operation)
    cat > "${TEST_DIR}/post-tool-edit.json" <<'EOF'
{
  "session_id": "test-session-123",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "tests/test_users.py"
  },
  "tool_use_id": "toolu_test456"
}
EOF

    # Sample Stop event
    cat > "${TEST_DIR}/stop.json" <<'EOF'
{
  "session_id": "test-session-123",
  "hook_event_name": "Stop"
}
EOF

    # Sample SessionEnd event
    cat > "${TEST_DIR}/session-end.json" <<'EOF'
{
  "session_id": "test-session-123",
  "hook_event_name": "SessionEnd",
  "transcript_path": "/tmp/transcript.jsonl"
}
EOF

    # Sample SessionStart event
    cat > "${TEST_DIR}/session-start.json" <<'EOF'
{
  "session_id": "test-session-124",
  "hook_event_name": "SessionStart"
}
EOF

    success "Created test data in ${TEST_DIR}"
}

# ============================================================================
# Test Functions
# ============================================================================

test_check_structure() {
    info "Testing check-structure.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/check-structure.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Test 1: Valid file location
    echo "  Test 1: Valid file in src/"
    echo '{"tool_name":"Write","tool_input":{"file_path":"src/api/users.py"}}' | \
        bash "$hook" && success "    Passed" || error "    Failed"
    
    echo ""
    
    # Test 2: Invalid file in root
    echo "  Test 2: Invalid file in root"
    echo '{"tool_name":"Write","tool_input":{"file_path":"users.py"}}' | \
        bash "$hook" 2>/dev/null && error "    Should have failed" || success "    Correctly blocked"
    
    echo ""
    
    # Test 3: Test file in correct location
    echo "  Test 3: Test file in tests/"
    echo '{"tool_name":"Write","tool_input":{"file_path":"tests/test_users.py"}}' | \
        bash "$hook" && success "    Passed" || error "    Failed"
    
    echo ""
}

test_track_implementation() {
    info "Testing track-implementation.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/track-implementation.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Create minimal state file
    local state_file="${CLAUDE_PROJECT_DIR}/.ipe/implementation-state.json"
    mkdir -p "$(dirname "$state_file")"
    
    echo '{"current_task":null,"files_modified":[],"tasks_completed":[],"last_updated":null,"total_file_changes":0}' > "$state_file"
    
    # Test: Track file change
    echo "  Test: Track file modification"
    cat "${TEST_DIR}/post-tool-write.json" | bash "$hook"
    
    if jq -e '.files_modified[] | select(. == "src/api/users.py")' "$state_file" > /dev/null; then
        success "    File tracked in state"
    else
        error "    File not tracked"
    fi
    
    # Show state
    echo ""
    echo "  Current state:"
    jq . "$state_file"
    echo ""
}

test_update_claude_md() {
    info "Testing update-claude-md.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/update-claude-md.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Ensure CLAUDE.md exists
    local claude_md="${CLAUDE_PROJECT_DIR}/.claude/CLAUDE.md"
    
    if [ ! -f "$claude_md" ]; then
        warning "  CLAUDE.md not found, creating minimal version"
        mkdir -p "$(dirname "$claude_md")"
        cat > "$claude_md" <<'EOF'
# Project Context

## Current Stage
Stage 5: Implementation

## Completed Stages
✅ Stage 1: Discovery
✅ Stage 2: Solution Design
✅ Stage 3: Environment Setup
✅ Stage 4: Workflow Configuration

## [ACTIVE-CONTEXT] - Current Work (Auto-Updated)

**Current Task:** None
**Last Updated:** Never
EOF
    fi
    
    # Test: Update active context
    echo "  Test: Update active context section"
    cat "${TEST_DIR}/stop.json" | bash "$hook"
    
    if grep -q "\[ACTIVE-CONTEXT\]" "$claude_md"; then
        success "    Active context section updated"
        echo ""
        echo "  Updated section:"
        sed -n '/\[ACTIVE-CONTEXT\]/,/^##/p' "$claude_md" | head -n -1
        echo ""
    else
        error "    Active context not found"
    fi
}

test_inject_context() {
    info "Testing inject-stage-context.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/inject-stage-context.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Test: Display context at session start
    echo "  Test: Session start context injection"
    echo ""
    cat "${TEST_DIR}/session-start.json" | bash "$hook"
    echo ""
}

test_finalize_stage() {
    info "Testing finalize-stage.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/finalize-stage.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Create a test stage directory
    local stage_dir="${CLAUDE_PROJECT_DIR}/.ipe/test-stage"
    mkdir -p "$stage_dir"
    
    # Create a finalized artifact
    cat > "${stage_dir}/test-artifact.md" <<'EOF'
---
artifact: test-artifact.md
status: finalized
---
# Test Artifact
EOF
    
    # Test: Stage finalization check
    echo "  Test: Check stage finalization"
    cat "${TEST_DIR}/session-end.json" | bash "$hook"
    echo ""
}

test_validate_claude_md() {
    info "Testing validate-claude-md.sh..."
    echo ""
    
    local hook="${HOOKS_DIR}/validate-claude-md.sh"
    
    if [ ! -f "$hook" ]; then
        error "Hook script not found: $hook"
        return 1
    fi
    
    # Test: Validate CLAUDE.md
    echo "  Test: CLAUDE.md validation"
    echo ""
    bash "$hook"
    echo ""
}

# ============================================================================
# Main Test Runner
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  IPE Hook Testing Suite"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Setup test data
setup_test_data
echo ""

# Determine which tests to run
if [ -n "${1:-}" ]; then
    # Run specific test
    case "$1" in
        check-structure)
            test_check_structure
            ;;
        track-implementation)
            test_track_implementation
            ;;
        update-claude-md)
            test_update_claude_md
            ;;
        inject-context)
            test_inject_context
            ;;
        finalize-stage)
            test_finalize_stage
            ;;
        validate-claude-md)
            test_validate_claude_md
            ;;
        *)
            error "Unknown hook: $1"
            echo ""
            echo "Available hooks:"
            echo "  - check-structure"
            echo "  - track-implementation"
            echo "  - update-claude-md"
            echo "  - inject-context"
            echo "  - finalize-stage"
            echo "  - validate-claude-md"
            exit 1
            ;;
    esac
else
    # Run all tests
    test_check_structure
    echo ""
    
    test_track_implementation
    echo ""
    
    test_update_claude_md
    echo ""
    
    test_inject_context
    echo ""
    
    test_finalize_stage
    echo ""
    
    test_validate_claude_md
    echo ""
fi

echo "═══════════════════════════════════════════════════════════════"
echo ""
success "Testing complete!"
echo ""
echo "Test data saved in: ${TEST_DIR}"
echo ""
