#!/bin/bash
# rename-templates.sh - Rename IPE templates to ACK and update content
set -e

TEMPLATES_DIR="$HOME/code/ack/ack-src/templates"

echo "=== ACK Templates Rename Script ==="
echo ""

# 1. Rename artifact files
echo "1. Renaming artifact files..."
cd "$TEMPLATES_DIR/artifacts"

for f in ipe-demo-*.md; do
    if [ -f "$f" ]; then
        newname="${f/ipe-demo-/ack-}"
        echo "   $f → $newname"
        mv "$f" "$newname"
    fi
done

# 2. Update content in all artifact files (IPE → ACK)
echo ""
echo "2. Updating IPE references to ACK in content..."
for f in ack-*.md; do
    if [ -f "$f" ]; then
        # Replace common IPE references
        sed -i '' \
            -e 's/IPE/ACK/g' \
            -e 's/ipe-/ack-/g' \
            -e 's/Integrated Planning Environment/Agent Context Kit/g' \
            "$f"
        echo "   Updated: $f"
    fi
done

# 3. Fix typo in project-scaffolds
echo ""
echo "3. Fixing project-scaffolds..."
cd "$TEMPLATES_DIR/project-scaffolds"

if [ -f "repo-steup.md" ]; then
    mv "repo-steup.md" "repo-setup.md"
    echo "   Fixed typo: repo-steup.md → repo-setup.md"
fi

# 4. Delete zip files
echo ""
echo "4. Removing zip exports..."
rm -f *.zip && echo "   Deleted zip files" || echo "   No zip files found"

# 5. Delete empty placeholder directories
echo ""
echo "5. Cleaning up empty directories..."
cd "$TEMPLATES_DIR"
rmdir config 2>/dev/null && echo "   Removed: config/" || true
rmdir stages 2>/dev/null && echo "   Removed: stages/" || true

# 6. Summary
echo ""
echo "=== Complete ==="
echo ""
echo "Renamed templates:"
ls -1 "$TEMPLATES_DIR/artifacts/"
echo ""
echo "Project scaffolds:"
ls -1 "$TEMPLATES_DIR/project-scaffolds/"
echo ""
echo "NOTE: Review templates thoroughly for alignment with ACK methodology"
