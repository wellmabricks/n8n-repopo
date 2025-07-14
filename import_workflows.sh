#!/usr/bin/env bash

# Restores all n8n workflows and credentials from a specified backup directory.
# Usage: ./import_workflows.sh /path/to/your/backup_folder

set -euo pipefail

# Check if a backup directory path is provided as an argument.
if [ -z "${1-}" ]; then
    echo "❌ Error: Please provide the full path to the backup directory."
    echo "   Usage: ./import_workflows.sh /home/node/.n8n/n8n_backup_2025-07-14_12-00-00"
    exit 1
fi

BACKUP_DIR=$1

# Verify that the provided directory exists inside the container.
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Error: Backup directory not found at '$BACKUP_DIR'."
    exit 1
fi

echo "🚀 Starting n8n import process..."
echo "-------------------------------------"
echo "Source Directory: ${BACKUP_DIR}"
echo "WARNING: This will overwrite any existing workflows with the same ID."
echo "-------------------------------------"
read -p "Do you want to continue? (y/n): " -n 1 -r
echo # Move to a new line

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Import cancelled."
    exit 0
fi

# Use the n8n CLI to import from the backup directory.
# The encryption key is automatically read from the environment variables.
n8n import:workflow --separate --input="$BACKUP_DIR"

echo "✅ Success! Workflows and credentials have been imported."