#!/usr/bin/env bash

# A diagnostic script to check the health of the n8n environment on Render.
# It verifies key environment variables and tests the connection to the Supabase database.

set -euo pipefail

echo "🚀 Running n8n Diagnostic Health Check..."
echo "-------------------------------------"

# 1. Check for critical environment variables
echo "1. Verifying key environment variables..."
CRITICAL_VARS=("WEBHOOK_URL" "DB_TYPE" "DB_POSTGRESDB_HOST" "N8N_RUNNERS_ENABLED")
ALL_OK=true

for VAR in "${CRITICAL_VARS[@]}"; do
    if [ -z "${!VAR-}" ]; then
        echo "   ❌ FAIL: $VAR is not set."
        ALL_OK=false
    else
        echo "   ✅ OK: $VAR is set."
    fi
done

if ! $ALL_OK; then
    echo "   Critical environment variables are missing. Please check your Render service configuration."
fi
echo "-------------------------------------"

# 2. Check the database connection
# The n8n Docker image (based on Alpine) has the 'nc' (netcat) utility.
echo "2. Testing connection to Supabase..."
DB_HOST=$DB_POSTGRESDB_HOST
DB_PORT=$DB_POSTGRESDB_PORT

if nc -z -w 5 "$DB_HOST" "$DB_PORT"; then
    echo "   ✅ Success: Successfully connected to $DB_HOST on port $DB_PORT."
else
    echo "   ❌ FAIL: Could not connect to the database at $DB_HOST on port $DB_PORT."
    echo "      - Check your DB host, port, and Render's firewall/outbound rules."
fi
echo "-------------------------------------"
echo "Diagnostic check complete."