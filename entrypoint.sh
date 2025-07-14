#!/bin/sh
# Auto-import workflows and credentials on container startup

set -e

echo "🚀 Starting n8n with auto-import..."
echo "=================================="

# Define source directories
WORKFLOW_DIR="/app/workflows"
CREDENTIAL_DIR="/app/credentials"

# Import workflows if they exist
if [ -d "$WORKFLOW_DIR" ] && [ -n "$(ls -A "$WORKFLOW_DIR" 2>/dev/null)" ]; then
    echo "📁 Importing workflows..."
    for file in "$WORKFLOW_DIR"/*.json; do
        if [ -f "$file" ]; then
            echo "  → $(basename "$file")"
        fi
    done
    n8n import:workflow --input="$WORKFLOW_DIR" --separate
    echo "✅ Workflows imported successfully"
else
    echo "📁 No workflows found, skipping import"
fi

# Import credentials if they exist
if [ -d "$CREDENTIAL_DIR" ] && [ -n "$(ls -A "$CREDENTIAL_DIR" 2>/dev/null)" ]; then
    echo "🔐 Importing credentials..."
    for file in "$CREDENTIAL_DIR"/*.json; do
        if [ -f "$file" ]; then
            echo "  → $(basename "$file")"
        fi
    done
    n8n import:credential --input="$CREDENTIAL_DIR" --separate
    echo "✅ Credentials imported successfully"
else
    echo "🔐 No credentials found, skipping import"
fi

echo "=================================="
echo "🚀 Starting n8n..."

# Start n8n
exec n8n