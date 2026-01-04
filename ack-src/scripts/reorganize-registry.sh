#!/bin/bash
# Reorganize registry into structured hierarchy
# Run from: ~/code/ack/ack-src/scripts/

set -e

REGISTRY_DIR="$HOME/code/ack/ack-src/registry"
cd "$REGISTRY_DIR"

echo "Reorganizing registry at: $REGISTRY_DIR"
echo ""

# 1. Create directory structure
echo "Creating directory structure..."
mkdir -p agents
mkdir -p skills/railway skills/supabase skills/nextjs skills/github
mkdir -p tools
mkdir -p commands
mkdir -p prompts
mkdir -p policies

# 2. Move agents
echo "Moving agents..."
mv github-expert.md agents/ 2>/dev/null || true
mv railway-expert.md agents/ 2>/dev/null || true
mv supabase-expert.md agents/ 2>/dev/null || true
mv nextjs-expert.md agents/ 2>/dev/null || true

# 3. Move skills
echo "Moving skills..."
mv github-SKILL.md skills/github/SKILL.md 2>/dev/null || true
# Original skills may already be in skills/ subdirs

# 4. Move tools
echo "Moving tools..."
mv github.md tools/ 2>/dev/null || true
mv railway.md tools/ 2>/dev/null || true
mv supabase.md tools/ 2>/dev/null || true
mv nextjs-cli.md tools/ 2>/dev/null || true

# 5. Move commands
echo "Moving commands..."
mv github-debug.md commands/ 2>/dev/null || true
mv branch.md commands/ 2>/dev/null || true
mv pr.md commands/ 2>/dev/null || true
mv railway-debug.md commands/ 2>/dev/null || true
mv supabase-debug.md commands/ 2>/dev/null || true
mv nextjs-debug.md commands/ 2>/dev/null || true
mv commit.md commands/ 2>/dev/null || true

# 6. Move prompts
echo "Moving prompts..."
mv branch-name.md prompts/ 2>/dev/null || true
mv pr-description.md prompts/ 2>/dev/null || true
mv commit-message.md prompts/ 2>/dev/null || true
mv code-review.md prompts/ 2>/dev/null || true
mv error-diagnosis.md prompts/ 2>/dev/null || true
mv documentation.md prompts/ 2>/dev/null || true

# 7. Convert guides to READMEs
echo "Setting up README files..."
mv SKILL_CREATION_GUIDE.md skills/README.md 2>/dev/null || true
mv BUILTIN_COMMANDS_REFERENCE.md commands/README.md 2>/dev/null || true
mv MCP_INVENTORY.md tools/README.md 2>/dev/null || true

# 8. Delete deprecated files
echo "Cleaning up deprecated files..."
rm -f review.md HANDOFF.md

# 9. Clean up old empty directories
rmdir docs domains templates 2>/dev/null || true

echo ""
echo "Done! Final structure:"
echo ""
ls -la
echo ""
echo "Subdirectories:"
for dir in agents skills tools commands prompts policies; do
    if [ -d "$dir" ]; then
        echo ""
        echo "=== $dir/ ==="
        ls -la "$dir"
    fi
done
