#!/bin/bash
# Installation script for IPE hooks
# Usage: ./install.sh

set -euo pipefail

echo "IPE Hook Installation"
echo "===================="
echo ""

# Determine project directory
if [ -z "${CLAUDE_PROJECT_DIR:-}" ]; then
    CLAUDE_PROJECT_DIR="$(pwd)"
    echo "CLAUDE_PROJECT_DIR not set, using current directory: $CLAUDE_PROJECT_DIR"
fi

HOOKS_DIR="${CLAUDE_PROJECT_DIR}/.claude/hooks"

# Create hooks directory
echo "Creating hooks directory..."
mkdir -p "$HOOKS_DIR"

# Copy hooks (assumes scripts are in same directory as install.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Copying hook scripts..."
for script in check-structure.sh configure-hooks.sh finalize-stage.sh inject-stage-context.sh test-hooks.sh track-implementation.sh update-claude-md.sh validate-claude-md.sh; do
    if [ -f "${SCRIPT_DIR}/${script}" ]; then
        cp "${SCRIPT_DIR}/${script}" "${HOOKS_DIR}/"
        echo "  ✓ ${script}"
    else
        echo "  ✗ ${script} not found"
    fi
done

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x "${HOOKS_DIR}"/*.sh

# Copy README
if [ -f "${SCRIPT_DIR}/README.md" ]; then
    cp "${SCRIPT_DIR}/README.md" "${HOOKS_DIR}/"
    echo "  ✓ README.md"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Configure hooks: ${HOOKS_DIR}/configure-hooks.sh"
echo "  2. Test hooks: ${HOOKS_DIR}/test-hooks.sh"
echo "  3. Validate setup: ${HOOKS_DIR}/validate-claude-md.sh"
echo ""
