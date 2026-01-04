#!/bin/bash
# Hook: validate-claude-md.sh
# Event: Manual (can also be used in CI/CD)
# Purpose: Validate CLAUDE.md structure, imports, and token budget
#
# Usage: ./validate-claude-md.sh [--strict]
# Exit: 0 if valid, 1 if errors found

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

CLAUDE_MD="${CLAUDE_PROJECT_DIR}/.claude/CLAUDE.md"
STRICT_MODE=false

# Parse arguments
if [ "${1:-}" == "--strict" ]; then
    STRICT_MODE=true
fi

# Token budget limits
TOKEN_BUDGET_TARGET=20000
TOKEN_BUDGET_MAX=50000
TOKEN_BUDGET_WARNING=30000

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# Functions
# ============================================================================

error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ============================================================================
# Validation Functions
# ============================================================================

check_file_exists() {
    if [ ! -f "${CLAUDE_MD}" ]; then
        error "CLAUDE.md not found at ${CLAUDE_MD}"
        return 1
    fi
    success "CLAUDE.md file exists"
    return 0
}

check_required_sections() {
    local missing=0
    
    info "Checking required sections..."
    
    # Required sections for IPE integration
    local required_sections=(
        "## Current Stage"
        "## Completed Stages"
        "## Key Decisions"
        "## Critical Rules"
        "## Artifact Imports"
    )
    
    for section in "${required_sections[@]}"; do
        if grep -q "^${section}" "${CLAUDE_MD}"; then
            success "  Found: ${section}"
        else
            error "  Missing: ${section}"
            ((missing++))
        fi
    done
    
    if [ $missing -gt 0 ]; then
        error "Missing $missing required sections"
        return 1
    fi
    
    return 0
}

check_token_budget() {
    info "Checking token budget..."
    
    # Rough estimate: 1 char ≈ 0.25 tokens (GPT-4 tokenization)
    local chars=$(wc -c < "${CLAUDE_MD}")
    local estimated_tokens=$((chars / 4))
    
    echo "  Characters: ${chars}"
    echo "  Estimated tokens: ~${estimated_tokens}"
    
    if [ $estimated_tokens -lt $TOKEN_BUDGET_TARGET ]; then
        success "  Under target (${TOKEN_BUDGET_TARGET} tokens)"
    elif [ $estimated_tokens -lt $TOKEN_BUDGET_WARNING ]; then
        warning "  Approaching warning threshold (${TOKEN_BUDGET_WARNING} tokens)"
    elif [ $estimated_tokens -lt $TOKEN_BUDGET_MAX ]; then
        warning "  Exceeds warning threshold but under max (${TOKEN_BUDGET_MAX} tokens)"
        if [ "$STRICT_MODE" = true ]; then
            return 1
        fi
    else
        error "  Exceeds maximum budget (${TOKEN_BUDGET_MAX} tokens)"
        return 1
    fi
    
    return 0
}

check_imports() {
    local broken=0
    
    info "Checking artifact imports..."
    
    # Find all import statements (@path/to/file.md)
    local imports=$(grep -n "^@" "${CLAUDE_MD}" | sed 's/:.*$//' || echo "")
    
    if [ -z "$imports" ]; then
        warning "  No imports found (is this intentional?)"
        return 0
    fi
    
    while IFS= read -r line_num; do
        if [ -n "$line_num" ]; then
            local import_line=$(sed -n "${line_num}p" "${CLAUDE_MD}")
            local import_path=$(echo "$import_line" | sed 's/^@//')
            local full_path="${CLAUDE_PROJECT_DIR}/${import_path}"
            
            if [ -f "$full_path" ]; then
                success "  ✓ ${import_path}"
            else
                error "  ✗ Broken import at line ${line_num}: ${import_path}"
                ((broken++))
            fi
        fi
    done <<< "$imports"
    
    if [ $broken -gt 0 ]; then
        error "Found $broken broken imports"
        return 1
    fi
    
    success "All imports valid"
    return 0
}

check_syntax_errors() {
    info "Checking for syntax errors..."
    
    local errors=0
    
    # Check for unclosed code blocks
    local backticks=$(grep -c '```' "${CLAUDE_MD}" || echo "0")
    if [ $((backticks % 2)) -ne 0 ]; then
        error "  Unclosed code block (odd number of ```)"
        ((errors++))
    fi
    
    # Check for malformed frontmatter (if any)
    if grep -q "^---$" "${CLAUDE_MD}"; then
        local frontmatter_markers=$(grep -c "^---$" "${CLAUDE_MD}")
        if [ $((frontmatter_markers % 2)) -ne 0 ]; then
            error "  Malformed frontmatter (odd number of --- markers)"
            ((errors++))
        fi
    fi
    
    # Check for orphaned brackets
    local open_brackets=$(grep -o '\[' "${CLAUDE_MD}" | wc -l)
    local close_brackets=$(grep -o '\]' "${CLAUDE_MD}" | wc -l)
    if [ $open_brackets -ne $close_brackets ]; then
        warning "  Mismatched brackets ([]: ${open_brackets} vs ${close_brackets})"
        # Not a critical error
    fi
    
    if [ $errors -eq 0 ]; then
        success "No syntax errors found"
        return 0
    else
        error "Found $errors syntax errors"
        return 1
    fi
}

check_content_quality() {
    info "Checking content quality..."
    
    local issues=0
    
    # Check for very long lines (may indicate formatting issues)
    local long_lines=$(awk 'length > 120' "${CLAUDE_MD}" | wc -l)
    if [ $long_lines -gt 10 ]; then
        warning "  ${long_lines} lines exceed 120 characters (consider wrapping)"
    fi
    
    # Check for excessive repetition (same line multiple times)
    local duplicates=$(sort "${CLAUDE_MD}" | uniq -d | wc -l)
    if [ $duplicates -gt 5 ]; then
        warning "  ${duplicates} duplicate lines found (may indicate copy-paste errors)"
    fi
    
    # Check if sections are empty
    while IFS= read -r section; do
        local section_name=$(echo "$section" | sed 's/^## //')
        local line_num=$(grep -n "^## ${section_name}" "${CLAUDE_MD}" | cut -d: -f1)
        local next_line_num=$((line_num + 1))
        local next_content=$(sed -n "${next_line_num}p" "${CLAUDE_MD}")
        
        if [ -z "$next_content" ]; then
            warning "  Section may be empty: ${section_name}"
        fi
    done < <(grep "^## " "${CLAUDE_MD}" || true)
    
    # All quality checks are warnings only
    if [ $issues -eq 0 ]; then
        success "Content quality checks passed"
    fi
    
    return 0
}

check_stage_consistency() {
    info "Checking stage consistency..."
    
    local errors=0
    
    # Extract current stage
    local current_stage=$(grep -m1 "^Stage [0-9]:" "${CLAUDE_MD}" | \
                         sed -E 's/^Stage ([0-9]):.*/\1/' || echo "")
    
    if [ -z "$current_stage" ]; then
        error "  Could not determine current stage"
        return 1
    fi
    
    success "  Current stage: ${current_stage}"
    
    # Count completed stages
    local completed=$(grep -c "^✅ Stage" "${CLAUDE_MD}" || echo "0")
    
    # Verify completed stages are sequential
    if [ "$completed" -gt 0 ]; then
        for i in $(seq 1 $completed); do
            if ! grep -q "^✅ Stage ${i}:" "${CLAUDE_MD}"; then
                error "  Stage ${i} not marked complete but later stages are"
                ((errors++))
            fi
        done
    fi
    
    # Check current stage is not already marked complete
    if grep -q "^✅ Stage ${current_stage}:" "${CLAUDE_MD}"; then
        error "  Current stage (${current_stage}) already marked complete"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        success "Stage consistency verified"
        return 0
    else
        return 1
    fi
}

generate_report() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  CLAUDE.md Validation Report"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "File: ${CLAUDE_MD}"
    echo "Mode: $([ "$STRICT_MODE" = true ] && echo "STRICT" || echo "NORMAL")"
    echo "Time: $(date)"
    echo ""
}

# ============================================================================
# Main Validation
# ============================================================================

generate_report

# Run all validations
validation_errors=0

check_file_exists || ((validation_errors++))
echo ""

check_required_sections || ((validation_errors++))
echo ""

check_token_budget || ((validation_errors++))
echo ""

check_imports || ((validation_errors++))
echo ""

check_syntax_errors || ((validation_errors++))
echo ""

check_content_quality || true  # Quality checks are informational
echo ""

check_stage_consistency || ((validation_errors++))
echo ""

# ============================================================================
# Final Result
# ============================================================================

echo "═══════════════════════════════════════════════════════════════"

if [ $validation_errors -eq 0 ]; then
    echo -e "${GREEN}"
    echo "  ✓ VALIDATION PASSED"
    echo -e "${NC}"
    echo "  CLAUDE.md is valid and ready for use"
    exit 0
else
    echo -e "${RED}"
    echo "  ✗ VALIDATION FAILED"
    echo -e "${NC}"
    echo "  Found ${validation_errors} error(s)"
    echo ""
    echo "  Fix the errors above and run validation again."
    exit 1
fi
