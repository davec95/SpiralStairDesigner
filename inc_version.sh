#!/bin/bash
# Increment version number in SpiralStairDesigner.html
# Usage: ./inc_version.sh [major|minor|patch|build]

FILE="/home/user/bin/SpiralStairDesigner.html"
REPO_FILE="/home/user/Repos/SpiralStaircase/SpiralStairDesigner.html"

# Get current version
CURRENT=$(grep -oP 'v1\.\K\d+' "$FILE" 2>/dev/null)

if [ -z "$CURRENT" ]; then
    echo "Could not find version number in $FILE"
    exit 1
fi

# Determine increment type
TYPE="${1:-build}"

case "$TYPE" in
    major)
        NEW_MAJOR=$((CURRENT / 10 + 1))
        NEW_MINOR=$((CURRENT % 10))
        VERSION="v${NEW_MAJOR}.${NEW_MINOR}"
        ;;
    minor)
        VERSION="v1.$((CURRENT + 1))"
        ;;
    patch|build)
        VERSION="v1.$((CURRENT + 1))"
        ;;
    *)
        echo "Usage: $0 [major|minor|patch|build]"
        exit 1
        ;;
esac

echo "Updating $FILE from v1.$CURRENT to $VERSION"

# Update the version in the file
sed -i "s/v1\.[0-9]\+/$VERSION/" "$FILE"

# Also update the repo copy
if [ -f "$REPO_FILE" ]; then
    sed -i "s/v1\.[0-9]\+/$VERSION/" "$REPO_FILE"
    echo "Also updated $REPO_FILE"
fi

echo "Version updated to $VERSION"
echo "Don't forget to: cd /home/user/Repos/SpiralStaircase && git add SpiralStairDesigner.html && git commit"
