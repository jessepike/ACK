#!/bin/bash
# validate-ipe.sh - Complete IPE project validation
# Usage: ./scripts/validate-ipe.sh [options]

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Options
VERBOSE=false
DRY_RUN=false
STAGE=""
JSON_OUTPUT=false
FIX_ISSUES=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# ============================================================================
# Functions
# ============================================================================

log() {
    echo -e "${BLUE}ℹ${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "  ${BLUE}→${NC} $1"
    fi
}

section() {
    echo ""
    echo -e "${BOLD}$1${NC}"
    echo "─────────────────────────────────────────────────────────────────"
}

show_help() {
    cat << EOF
IPE Validation Script

Usage: ./scripts/validate-ipe.sh [options]

Options:
  --stage N       Validate only stage N (1-5)
  --dry-run       Show what would be checked without checking
  --verbose       Show detailed output
  --json          Output results as JSON
  --fix           Auto-fix simple issues (use with caution)
  --help          Show this help message

Exit codes:
  0 - All validations passed
  1 - One or more validations failed
  2 - Script error or invalid usage

Examples:
  ./scripts/validate-ipe.sh                    # Validate entire IPE
  ./scripts/validate-ipe.sh --stage 3          # Validate only Stage 3
  ./scripts/validate-ipe.sh --verbose          # Detailed output
  ./scripts/validate-ipe.sh --json > report.json

EOF
}

# ============================================================================
# Stage Validation Functions
# ============================================================================

validate_stage_1() {
    section "Stage 1: Discovery"
    
    local stage_dir=".ipe/discovery"
    
    # Check directory exists
    if [ ! -d "$stage_dir" ]; then
        fail "Discovery directory not found: $stage_dir"
        return 1
    fi
    verbose "Discovery directory exists"
    
    # Required artifacts
    local required=(
        "discovery-synthesis.md"
        "stakeholders.md"
        "requirements.md"
        "constraints.md"
        "success-criteria.md"
    )
    
    for artifact in "${required[@]}"; do
        local file="$stage_dir/$artifact"
        
        if [ ! -f "$file" ]; then
            fail "Missing required artifact: $artifact"
            continue
        fi
        verbose "Found: $artifact"
        
        # Check for finalized status
        if grep -q "status: finalized" "$file"; then
            success "$artifact is finalized"
        else
            fail "$artifact is not finalized"
        fi
        
        # Check frontmatter exists
        if ! head -1 "$file" | grep -q "^---$"; then
            warn "$artifact missing YAML frontmatter"
        fi
    done
    
    # Content validation
    if [ -f "$stage_dir/stakeholders.md" ]; then
        local stakeholder_count=$(grep -c "^### " "$stage_dir/stakeholders.md" || echo "0")
        if [ "$stakeholder_count" -ge 3 ]; then
            success "Found $stakeholder_count stakeholders (minimum 3)"
        else
            warn "Only $stakeholder_count stakeholders (recommend 3+)"
        fi
    fi
    
    if [ -f "$stage_dir/requirements.md" ]; then
        local req_count=$(grep -c "^## R-" "$stage_dir/requirements.md" || echo "0")
        if [ "$req_count" -ge 5 ]; then
            success "Found $req_count requirements (minimum 5)"
        else
            warn "Only $req_count requirements (recommend 5+)"
        fi
    fi
}

validate_stage_2() {
    section "Stage 2: Solution Design"
    
    local stage_dir=".ipe/solution-design"
    
    if [ ! -d "$stage_dir" ]; then
        fail "Solution design directory not found: $stage_dir"
        return 1
    fi
    verbose "Solution design directory exists"
    
    local required=(
        "architecture.md"
        "stack.md"
        "data-model.md"
        "design-decisions.md"
    )
    
    for artifact in "${required[@]}"; do
        local file="$stage_dir/$artifact"
        
        if [ ! -f "$file" ]; then
            fail "Missing required artifact: $artifact"
            continue
        fi
        verbose "Found: $artifact"
        
        if grep -q "status: finalized" "$file"; then
            success "$artifact is finalized"
        else
            fail "$artifact is not finalized"
        fi
    done
    
    # Check stack.md has technology selections
    if [ -f "$stage_dir/stack.md" ]; then
        if grep -qi "language:" "$stage_dir/stack.md" && \
           grep -qi "framework:" "$stage_dir/stack.md" && \
           grep -qi "database:" "$stage_dir/stack.md"; then
            success "Stack selections documented"
        else
            warn "Stack.md may be incomplete (language/framework/database)"
        fi
    fi
}

validate_stage_3() {
    section "Stage 3: Environment Setup"
    
    local stage_dir=".ipe/environment-setup"
    
    if [ ! -d "$stage_dir" ]; then
        fail "Environment setup directory not found: $stage_dir"
        return 1
    fi
    verbose "Environment setup directory exists"
    
    local required=(
        "repo-structure.md"
        "environment-config.md"
        "setup-guide.md"
    )
    
    for artifact in "${required[@]}"; do
        local file="$stage_dir/$artifact"
        
        if [ ! -f "$file" ]; then
            fail "Missing required artifact: $artifact"
            continue
        fi
        verbose "Found: $artifact"
        
        if grep -q "status: finalized" "$file"; then
            success "$artifact is finalized"
        else
            fail "$artifact is not finalized"
        fi
    done
    
    # Check environment-manifest.json exists
    if [ -f "$stage_dir/environment-manifest.json" ]; then
        if jq empty "$stage_dir/environment-manifest.json" 2>/dev/null; then
            success "environment-manifest.json is valid JSON"
        else
            fail "environment-manifest.json is not valid JSON"
        fi
    else
        warn "environment-manifest.json not found (optional but recommended)"
    fi
    
    # Check repository structure exists
    section "Repository Structure Validation"
    
    if [ -d "src" ]; then
        success "src/ directory exists"
    else
        warn "src/ directory not found"
    fi
    
    if [ -d "tests" ]; then
        success "tests/ directory exists"
    else
        warn "tests/ directory not found"
    fi
    
    if [ -f ".gitignore" ]; then
        success ".gitignore exists"
    else
        warn ".gitignore not found"
    fi
    
    if [ -f "README.md" ]; then
        success "README.md exists"
    else
        warn "README.md not found"
    fi
}

validate_stage_4() {
    section "Stage 4: Workflow Configuration"
    
    local stage_dir=".ipe/workflow-config"
    
    if [ ! -d "$stage_dir" ]; then
        fail "Workflow config directory not found: $stage_dir"
        return 1
    fi
    verbose "Workflow config directory exists"
    
    # Governed artifacts (must be finalized)
    section "Governed Artifacts"
    local governed=(
        "dev-workflow.md"
        "environment-variants.md"
        "context-management.md"
        "claude-config.md"
    )
    
    for artifact in "${governed[@]}"; do
        local file="$stage_dir/$artifact"
        
        if [ ! -f "$file" ]; then
            fail "Missing governed artifact: $artifact"
            continue
        fi
        verbose "Found: $artifact"
        
        if grep -q "status: finalized" "$file"; then
            success "$artifact is finalized"
        else
            fail "$artifact is not finalized (governed artifacts must be finalized)"
        fi
    done
    
    # Continuous artifacts (must exist but can evolve)
    section "Continuous Artifacts"
    
    if [ -f ".claude/claude.md" ]; then
        success ".claude/claude.md exists"
    else
        fail ".claude/claude.md not found"
    fi
    
    if [ -f ".agent/agent.md" ]; then
        success ".agent/agent.md exists"
    else
        warn ".agent/agent.md not found (recommended for multi-agent support)"
    fi
    
    if [ -f "$stage_dir/operations-playbook.md" ]; then
        success "operations-playbook.md exists"
    else
        warn "operations-playbook.md not found (recommended)"
    fi
    
    # Generated artifacts
    section "Generated Artifacts"
    
    if [ -f ".claude/CLAUDE.md" ]; then
        success ".claude/CLAUDE.md exists"
        
        # Validate CLAUDE.md if validation script exists
        if [ -x ".claude/hooks/validate-claude-md.sh" ]; then
            verbose "Running CLAUDE.md validation..."
            if ./.claude/hooks/validate-claude-md.sh >/dev/null 2>&1; then
                success "CLAUDE.md validation passed"
            else
                fail "CLAUDE.md validation failed (run .claude/hooks/validate-claude-md.sh for details)"
            fi
        fi
    else
        fail ".claude/CLAUDE.md not found (should be generated from claude-config.md)"
    fi
    
    # Hooks configuration
    section "Hooks Configuration"
    
    if [ -f ".claude/settings.json" ]; then
        success ".claude/settings.json exists"
        
        if jq -e '.hooks' ".claude/settings.json" >/dev/null 2>&1; then
            success "Hooks configured in settings.json"
        else
            warn "Hooks section not found in settings.json"
        fi
    else
        warn ".claude/settings.json not found (hooks won't run)"
    fi
    
    # Check hook scripts exist
    local hooks=(
        "update-claude-md.sh"
        "finalize-stage.sh"
        "inject-stage-context.sh"
        "check-structure.sh"
        "track-implementation.sh"
        "validate-claude-md.sh"
    )
    
    local missing_hooks=0
    for hook in "${hooks[@]}"; do
        if [ -f ".claude/hooks/$hook" ]; then
            if [ -x ".claude/hooks/$hook" ]; then
                verbose "Hook $hook is executable"
            else
                warn "Hook $hook exists but is not executable"
            fi
        else
            ((missing_hooks++))
        fi
    done
    
    if [ $missing_hooks -eq 0 ]; then
        success "All 6 hook scripts present"
    else
        warn "$missing_hooks hook scripts missing"
    fi
}

validate_stage_5() {
    section "Stage 5: Implementation Planning"
    
    local stage_dir=".ipe/implementation"
    
    if [ ! -d "$stage_dir" ]; then
        fail "Implementation directory not found: $stage_dir"
        return 1
    fi
    verbose "Implementation directory exists"
    
    # All artifacts must be locked
    local required=(
        "phases.md"
        "tasks.md"
        "dependencies.md"
        "effort-estimates.md"
        "skills-and-agents.md"
    )
    
    for artifact in "${required[@]}"; do
        local file="$stage_dir/$artifact"
        
        if [ ! -f "$file" ]; then
            fail "Missing required artifact: $artifact"
            continue
        fi
        verbose "Found: $artifact"
        
        if grep -q "status: locked" "$file"; then
            success "$artifact is locked"
        else
            fail "$artifact is not locked (implementation plan must be locked)"
        fi
    done
    
    # Validate tasks if validation script exists
    if [ -f "$SCRIPT_DIR/validate-tasks.py" ] && [ -f "$stage_dir/tasks.md" ]; then
        verbose "Running task validation..."
        if python3 "$SCRIPT_DIR/validate-tasks.py" "$stage_dir/tasks.md" >/dev/null 2>&1; then
            success "All tasks have required fields"
        else
            fail "Task validation failed (run scripts/validate-tasks.py for details)"
        fi
    fi
    
    # Check for circular dependencies if script exists
    if [ -f "$SCRIPT_DIR/check-cycles.py" ] && [ -f "$stage_dir/dependencies.md" ]; then
        verbose "Checking for circular dependencies..."
        if python3 "$SCRIPT_DIR/check-cycles.py" "$stage_dir/dependencies.md" >/dev/null 2>&1; then
            success "No circular dependencies detected"
        else
            fail "Circular dependencies detected (run scripts/check-cycles.py for details)"
        fi
    fi
}

# ============================================================================
# Cross-Stage Validation
# ============================================================================

validate_cross_stage() {
    section "Cross-Stage Validation"
    
    # Check requirement coverage if script exists
    if [ -f "$SCRIPT_DIR/coverage-check.py" ]; then
        verbose "Checking requirement coverage..."
        if python3 "$SCRIPT_DIR/coverage-check.py" >/dev/null 2>&1; then
            success "All requirements covered by tasks"
        else
            warn "Some requirements may not have corresponding tasks"
        fi
    fi
    
    # Check CLAUDE.md token budget if script exists
    if [ -f "$SCRIPT_DIR/check-token-budget.py" ] && [ -f ".claude/CLAUDE.md" ]; then
        verbose "Checking CLAUDE.md token budget..."
        if python3 "$SCRIPT_DIR/check-token-budget.py" >/dev/null 2>&1; then
            success "CLAUDE.md within token budget"
        else
            warn "CLAUDE.md may exceed recommended token budget"
        fi
    fi
    
    # Validate cross-references
    local broken_refs=0
    
    if [ -f ".claude/CLAUDE.md" ]; then
        verbose "Checking for broken imports in CLAUDE.md..."
        while IFS= read -r line; do
            if [[ $line =~ ^@(.+)$ ]]; then
                local ref="${BASH_REMATCH[1]}"
                if [ ! -f "$ref" ]; then
                    fail "Broken import in CLAUDE.md: $ref"
                    ((broken_refs++))
                fi
            fi
        done < ".claude/CLAUDE.md"
        
        if [ $broken_refs -eq 0 ]; then
            success "All CLAUDE.md imports valid"
        fi
    fi
}

# ============================================================================
# Main Execution
# ============================================================================

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --stage)
                STAGE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --json)
                JSON_OUTPUT=true
                shift
                ;;
            --fix)
                FIX_ISSUES=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Run with --help for usage information"
                exit 2
                ;;
        esac
    done
}

main() {
    cd "$PROJECT_ROOT" || exit 2
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  IPE Validation Report"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Project: $(basename "$PROJECT_ROOT")"
    echo "Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    echo ""
    
    if [ "$DRY_RUN" = true ]; then
        log "DRY RUN - No actual validation performed"
        echo ""
    fi
    
    # Run validations
    if [ -n "$STAGE" ]; then
        case $STAGE in
            1) validate_stage_1 ;;
            2) validate_stage_2 ;;
            3) validate_stage_3 ;;
            4) validate_stage_4 ;;
            5) validate_stage_5 ;;
            *)
                echo "Invalid stage: $STAGE (must be 1-5)"
                exit 2
                ;;
        esac
    else
        # Validate all stages
        validate_stage_1 || true
        validate_stage_2 || true
        validate_stage_3 || true
        validate_stage_4 || true
        validate_stage_5 || true
        validate_cross_stage || true
    fi
    
    # Summary
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Validation Summary"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Total Checks:   $TOTAL_CHECKS"
    echo -e "Passed:         ${GREEN}$PASSED_CHECKS${NC}"
    echo -e "Failed:         ${RED}$FAILED_CHECKS${NC}"
    echo -e "Warnings:       ${YELLOW}$WARNING_CHECKS${NC}"
    echo ""
    
    if [ $FAILED_CHECKS -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✅ ALL VALIDATIONS PASSED${NC}"
        echo ""
        echo "IPE project is ready for implementation"
        echo ""
        if [ -f ".ipe/implementation/tasks.md" ]; then
            echo "Next: Start TASK-001"
        fi
        echo ""
        exit 0
    else
        echo -e "${RED}${BOLD}✗ VALIDATION FAILED${NC}"
        echo ""
        echo "Fix the $FAILED_CHECKS error(s) above before proceeding"
        echo ""
        if [ $WARNING_CHECKS -gt 0 ]; then
            echo "Note: $WARNING_CHECKS warning(s) found - review recommended but not blocking"
            echo ""
        fi
        exit 1
    fi
}

# ============================================================================
# Entry Point
# ============================================================================

parse_args "$@"
main
