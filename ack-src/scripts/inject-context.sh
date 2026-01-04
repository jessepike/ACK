#!/bin/bash
# inject-context.sh
# Compiles project context into a single output for pasting into agents
# that don't auto-load CLAUDE.md (browser chat, desktop apps, etc.)

# Usage: ./inject-context.sh [options]
# Options:
#   --full      Include all context files
#   --minimal   Just intent + current focus (default)
#   --copy      Copy to clipboard (macOS)

set -e

# Find project root (look for CLAUDE.md or .context folder)
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/CLAUDE.md" ]] || [[ -d "$dir/.context" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "Error: Not in a project directory (no CLAUDE.md or .context found)" >&2
    exit 1
}

PROJECT_ROOT=$(find_project_root)
PROJECT_NAME=$(basename "$PROJECT_ROOT")

# Default mode
MODE="minimal"
COPY_TO_CLIPBOARD=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --full) MODE="full"; shift ;;
        --minimal) MODE="minimal"; shift ;;
        --copy) COPY_TO_CLIPBOARD=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Build output
output=""

separator() {
    echo ""
    echo "---"
    echo ""
}

add_section() {
    local title="$1"
    local file="$2"
    
    if [[ -f "$file" ]]; then
        output+="## $title"
        output+=$'\n\n'
        output+=$(cat "$file")
        output+=$'\n'
        output+=$(separator)
    fi
}

# Header
output+="# Project Context: $PROJECT_NAME"
output+=$'\n'
output+="Generated: $(date '+%Y-%m-%d %H:%M')"
output+=$'\n'
output+=$(separator)

# Always include CLAUDE.md if it exists
if [[ -f "$PROJECT_ROOT/CLAUDE.md" ]]; then
    output+="## Agent Instructions (CLAUDE.md)"
    output+=$'\n\n'
    output+=$(cat "$PROJECT_ROOT/CLAUDE.md")
    output+=$'\n'
    output+=$(separator)
fi

# Minimal mode: just intent + current focus
if [[ "$MODE" == "minimal" ]]; then
    add_section "Intent" "$PROJECT_ROOT/.context/intent.md"
    add_section "Current Focus" "$PROJECT_ROOT/.context/current-focus.md"
fi

# Full mode: everything
if [[ "$MODE" == "full" ]]; then
    add_section "Intent" "$PROJECT_ROOT/.context/intent.md"
    add_section "Current Focus" "$PROJECT_ROOT/.context/current-focus.md"
    add_section "Key Decisions" "$PROJECT_ROOT/.context/decisions.md"
    add_section "Constraints" "$PROJECT_ROOT/.context/constraints.md"
    add_section "Environment" "$PROJECT_ROOT/.environment/manifest.md"
fi

# Output
if [[ "$COPY_TO_CLIPBOARD" == true ]]; then
    echo "$output" | pbcopy
    echo "Context copied to clipboard ($(echo "$output" | wc -w | tr -d ' ') words)"
else
    echo "$output"
fi
