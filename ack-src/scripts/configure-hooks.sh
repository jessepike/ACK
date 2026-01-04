#!/bin/bash
# Helper: configure-hooks.sh
# Purpose: Configure IPE hooks in Claude Code settings.json
#
# Usage: ./configure-hooks.sh [--dry-run]
# Creates or updates .claude/settings.json with IPE hook configuration

set -euo pipefail

# ============================================================================
# Configuration
# ============================================================================

SETTINGS_FILE="${CLAUDE_PROJECT_DIR}/.claude/settings.json"
BACKUP_FILE="${CLAUDE_PROJECT_DIR}/.claude/settings.json.backup"
DRY_RUN=false

# Parse arguments
if [ "${1:-}" == "--dry-run" ]; then
    DRY_RUN=true
fi

# Colors
GREEN='\033[0;32m'
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

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# ============================================================================
# Hook Configuration
# ============================================================================

HOOKS_CONFIG=$(cat <<'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/inject-stage-context.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/update-claude-md.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/finalize-stage.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-structure.sh"
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/track-implementation.sh"
          }
        ]
      }
    ]
  }
}
EOF
)

# ============================================================================
# Main Logic
# ============================================================================

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  IPE Hook Configuration Setup"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if settings.json exists
if [ -f "${SETTINGS_FILE}" ]; then
    info "Found existing settings.json"
    
    # Create backup
    if [ "$DRY_RUN" = false ]; then
        cp "${SETTINGS_FILE}" "${BACKUP_FILE}"
        success "Created backup: ${BACKUP_FILE}"
    else
        info "Would create backup: ${BACKUP_FILE}"
    fi
    
    # Check if hooks already configured
    if grep -q '"hooks"' "${SETTINGS_FILE}"; then
        warning "Hooks section already exists in settings.json"
        echo ""
        echo "Options:"
        echo "  1. Merge with existing hooks (manual edit required)"
        echo "  2. Replace hooks section (overwrites existing)"
        echo "  3. Cancel"
        echo ""
        read -p "Choose option (1-3): " choice
        
        case $choice in
            1)
                info "Please manually merge the following configuration:"
                echo ""
                echo "$HOOKS_CONFIG"
                echo ""
                exit 0
                ;;
            2)
                if [ "$DRY_RUN" = false ]; then
                    # Remove existing hooks section and add new one
                    jq 'del(.hooks)' "${SETTINGS_FILE}" | \
                    jq --argjson hooks "$(echo "$HOOKS_CONFIG" | jq .hooks)" \
                       '. + {hooks: $hooks}' > "${SETTINGS_FILE}.tmp"
                    mv "${SETTINGS_FILE}.tmp" "${SETTINGS_FILE}"
                    success "Replaced hooks configuration"
                else
                    info "Would replace hooks configuration"
                fi
                ;;
            3)
                info "Cancelled"
                exit 0
                ;;
            *)
                warning "Invalid choice. Exiting."
                exit 1
                ;;
        esac
    else
        # Add hooks to existing settings
        if [ "$DRY_RUN" = false ]; then
            jq --argjson hooks "$(echo "$HOOKS_CONFIG" | jq .hooks)" \
               '. + {hooks: $hooks}' "${SETTINGS_FILE}" > "${SETTINGS_FILE}.tmp"
            mv "${SETTINGS_FILE}.tmp" "${SETTINGS_FILE}"
            success "Added hooks configuration"
        else
            info "Would add hooks configuration"
        fi
    fi
else
    info "No existing settings.json found"
    
    # Create new settings.json
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$(dirname "${SETTINGS_FILE}")"
        echo "$HOOKS_CONFIG" > "${SETTINGS_FILE}"
        success "Created settings.json with hooks"
    else
        info "Would create new settings.json"
    fi
fi

echo ""
echo "───────────────────────────────────────────────────────────────"
echo ""

# Verify hook scripts exist
info "Verifying hook scripts..."
echo ""

hooks=(
    "inject-stage-context.sh"
    "update-claude-md.sh"
    "finalize-stage.sh"
    "check-structure.sh"
    "track-implementation.sh"
)

missing=0
for hook in "${hooks[@]}"; do
    hook_path="${CLAUDE_PROJECT_DIR}/.claude/hooks/${hook}"
    if [ -f "$hook_path" ]; then
        if [ -x "$hook_path" ]; then
            success "  ${hook} (executable)"
        else
            warning "  ${hook} exists but not executable"
            if [ "$DRY_RUN" = false ]; then
                chmod +x "$hook_path"
                success "  Made ${hook} executable"
            fi
        fi
    else
        warning "  ${hook} not found"
        ((missing++))
    fi
done

if [ $missing -gt 0 ]; then
    echo ""
    warning "Missing $missing hook scripts"
    echo "Copy all hook scripts to: ${CLAUDE_PROJECT_DIR}/.claude/hooks/"
fi

echo ""
echo "───────────────────────────────────────────────────────────────"
echo ""

# Show configuration
info "Current hook configuration:"
echo ""

if [ -f "${SETTINGS_FILE}" ]; then
    jq .hooks "${SETTINGS_FILE}" 2>/dev/null || cat "${SETTINGS_FILE}"
else
    warning "settings.json not found"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

if [ "$DRY_RUN" = true ]; then
    info "DRY RUN - No changes were made"
    echo "Run without --dry-run to apply changes"
else
    success "Hook configuration complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Verify hooks are working:"
    echo "     ./claude/hooks/validate-claude-md.sh"
    echo ""
    echo "  2. Test individual hooks:"
    echo "     ./.claude/hooks/update-claude-md.sh"
    echo ""
    echo "  3. Start Claude Code and check session start output"
fi

echo ""
