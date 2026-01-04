#!/bin/bash
# Hook: check-structure.sh
# Event: PostToolUse (Write|Edit)
# Purpose: Validate file placement against repo-structure.md rules
#
# Triggered when: After Write or Edit tool operations
# Validates: File created in allowed location, follows naming conventions
# Blocks: Critical violations (exit 2), warns on minor issues

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

REPO_STRUCTURE="${CLAUDE_PROJECT_DIR}/.ipe/environment-setup/repo-structure.md"
DRIFT_LOG="${CLAUDE_PROJECT_DIR}/.claude/hooks/drift.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Severity levels
SEVERITY_CRITICAL=2  # Block operation
SEVERITY_WARNING=0   # Allow but warn
SEVERITY_INFO=0      # Log only

# ============================================================================
# Functions
# ============================================================================

log() {
    echo "[${TIMESTAMP}] $1" >> "${DRIFT_LOG}"
}

error() {
    echo "🚫 CRITICAL: $1" >&2
    log "CRITICAL: $1"
    exit $SEVERITY_CRITICAL
}

warning() {
    echo "⚠️  WARNING: $1" >&2
    log "WARNING: $1"
}

info() {
    echo "ℹ️  INFO: $1" >&1
    log "INFO: $1"
}

# ============================================================================
# Parse Hook Input
# ============================================================================

input=$(cat)
log "Received input"

# Extract file path from tool input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // ""')

if [ -z "$file_path" ]; then
    log "No file_path in input, skipping validation"
    exit 0
fi

# Make path relative to project root
file_path=${file_path#"${CLAUDE_PROJECT_DIR}/"}

log "Validating file: ${file_path}"

# ============================================================================
# Load Structure Rules
# ============================================================================

if [ ! -f "${REPO_STRUCTURE}" ]; then
    warning "repo-structure.md not found, skipping validation"
    exit 0
fi

# ============================================================================
# Validation Rules
# ============================================================================

# Rule 1: No source code in project root (except main.py, app.py)
check_root_files() {
    local file=$1
    
    # Check if file is in root directory
    if [[ ! "$file" =~ / ]]; then
        # Allow specific entry point files
        case $(basename "$file") in
            main.py|app.py|setup.py|README.md|LICENSE|.gitignore|.env*)
                info "Entry point file in root: ${file}"
                return 0
                ;;
            *.py|*.js|*.ts|*.jsx|*.tsx)
                error "Source code not allowed in root: ${file}. Move to src/"
                ;;
            *)
                warning "Unexpected file in root: ${file}"
                return 0
                ;;
        esac
    fi
}

# Rule 2: Source code must be in src/ directory
check_source_location() {
    local file=$1
    
    case "$file" in
        *.py|*.js|*.ts|*.jsx|*.tsx|*.go|*.rs|*.java)
            # Must be in src/ or tests/ or scripts/
            if [[ ! "$file" =~ ^(src/|tests/|scripts/|docs/) ]]; then
                error "Source code must be in src/, tests/, or scripts/: ${file}"
            fi
            ;;
    esac
}

# Rule 3: Tests must mirror src structure
check_test_location() {
    local file=$1
    
    # Check if it's a test file
    if [[ "$file" =~ (test_|_test\.py|\.test\.|\.spec\.) ]]; then
        if [[ ! "$file" =~ ^tests/ ]]; then
            error "Test files must be in tests/ directory: ${file}"
        fi
        
        # Verify it mirrors src structure (if applicable)
        # Extract path after tests/
        local test_path=${file#tests/}
        
        # If there's a corresponding file in src/, structure should match
        local src_equivalent="src/${test_path/test_/}"
        src_equivalent="${src_equivalent/_test.py/.py}"
        
        if [ -f "${CLAUDE_PROJECT_DIR}/${src_equivalent}" ]; then
            # Check if directory structure matches
            local test_dir=$(dirname "$file")
            local src_dir=$(dirname "$src_equivalent")
            
            test_dir=${test_dir#tests/}
            src_dir=${src_dir#src/}
            
            if [ "$test_dir" != "$src_dir" ]; then
                warning "Test structure doesn't mirror src: ${file} vs ${src_equivalent}"
            fi
        fi
    fi
}

# Rule 4: Check against allowed directories from repo-structure.md
check_allowed_directories() {
    local file=$1
    
    # Extract allowed directories from repo-structure.md
    # Look for directory structure section
    local allowed_dirs=$(grep -E "^(src|tests|docs|scripts|config|\.ipe|\.claude)/" "${REPO_STRUCTURE}" 2>/dev/null | \
                        sed -E 's|^([^/]+)/.*|\1|' | \
                        sort -u || echo "")
    
    if [ -z "$allowed_dirs" ]; then
        # Fallback to defaults if repo-structure.md doesn't have structure
        allowed_dirs="src tests docs scripts config .ipe .claude"
    fi
    
    # Get first directory component
    local first_dir=$(echo "$file" | cut -d'/' -f1)
    
    # Check if first directory is allowed
    if ! echo "$allowed_dirs" | grep -q "^${first_dir}$"; then
        # Check if it's a root-level allowed file
        if [[ ! "$file" =~ / ]]; then
            check_root_files "$file"
        else
            error "Directory not allowed: ${first_dir}/. Allowed: ${allowed_dirs}"
        fi
    fi
}

# Rule 5: Naming conventions
check_naming_conventions() {
    local file=$1
    local basename=$(basename "$file")
    
    # Python files should be lowercase with underscores
    if [[ "$file" =~ \.py$ ]]; then
        if [[ "$basename" =~ [A-Z] ]] && [[ ! "$basename" =~ ^(README|LICENSE|CHANGELOG) ]]; then
            warning "Python files should use lowercase with underscores: ${basename}"
        fi
    fi
    
    # TypeScript/JavaScript components can use PascalCase
    if [[ "$file" =~ \.(tsx|jsx)$ ]]; then
        # Components should be PascalCase
        if [[ ! "$basename" =~ ^[A-Z] ]] && [[ ! "$basename" =~ ^(index|app)\. ]]; then
            warning "React components should use PascalCase: ${basename}"
        fi
    fi
    
    # Test files should have test_ prefix or _test suffix
    if [[ "$file" =~ ^tests/ ]] && [[ "$file" =~ \.py$ ]]; then
        if [[ ! "$basename" =~ ^test_ ]] && [[ ! "$basename" =~ _test\.py$ ]]; then
            warning "Python test files should start with test_ or end with _test.py: ${basename}"
        fi
    fi
}

# Rule 6: File size limits (informational)
check_file_size() {
    local file=$1
    local full_path="${CLAUDE_PROJECT_DIR}/${file}"
    
    if [ -f "$full_path" ]; then
        local size=$(wc -c < "$full_path")
        local lines=$(wc -l < "$full_path")
        
        # Warn on very large files
        if [ $lines -gt 500 ]; then
            warning "Large file (${lines} lines): ${file}. Consider splitting."
        fi
        
        if [ $size -gt 100000 ]; then
            local kb=$((size / 1024))
            warning "Large file (${kb}KB): ${file}"
        fi
    fi
}

# ============================================================================
# Run All Validations
# ============================================================================

log "Running validation checks on: ${file_path}"

check_root_files "$file_path"
check_source_location "$file_path"
check_test_location "$file_path"
check_allowed_directories "$file_path"
check_naming_conventions "$file_path"
check_file_size "$file_path"

log "Validation passed: ${file_path}"

# ============================================================================
# Success
# ============================================================================

exit 0
