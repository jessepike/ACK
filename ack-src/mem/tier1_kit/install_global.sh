#!/bin/bash
# Tier-1 Memory Kit - Global Installation Script
# Installs global memory files to ~/.claude/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_DIR="$HOME/.claude"
RULES_DIR="$GLOBAL_DIR/rules"

echo "=== Tier-1 Memory Kit: Global Installation ==="
echo ""

# Check if ~/.claude exists
if [ -d "$GLOBAL_DIR" ]; then
    echo "⚠️  ~/.claude already exists."
    read -p "Overwrite existing files? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Create directories
mkdir -p "$RULES_DIR"

# Copy files
echo "Installing global memory files..."

cp "$SCRIPT_DIR/global/CLAUDE.md" "$GLOBAL_DIR/"
echo "  ✓ ~/.claude/CLAUDE.md"

cp "$SCRIPT_DIR/global/rules/constitution.md" "$RULES_DIR/"
echo "  ✓ ~/.claude/rules/constitution.md"

cp "$SCRIPT_DIR/global/rules/preferences.md" "$RULES_DIR/"
echo "  ✓ ~/.claude/rules/preferences.md"

cp "$SCRIPT_DIR/global/rules/workflows.md" "$RULES_DIR/"
echo "  ✓ ~/.claude/rules/workflows.md"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Global memory installed to: $GLOBAL_DIR"
echo ""
echo "Next steps:"
echo "  1. Review and customize ~/.claude/rules/*.md"
echo "  2. Update ~/.claude/CLAUDE.md with your info"
echo "  3. For projects, copy tier1_kit/project/ to .claude/"
echo ""
