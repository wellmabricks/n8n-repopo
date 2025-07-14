# Use the official n8n Docker image
FROM n8nio/n8n:latest

# Set working directory
WORKDIR /app

# Copy workflow and credential directories
COPY --chown=node:node ./workflows ./workflows
COPY --chown=node:node ./credentials ./credentials

# Copy and make executable the entrypoint script
COPY --chown=node:node ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Use custom entrypoint that imports files before starting n8n
ENTRYPOINT ["/app/entrypoint.sh"]