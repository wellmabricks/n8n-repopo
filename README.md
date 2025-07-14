# n8n GitOps Deployment on Render

🚀 **Production-ready n8n deployment with automated workflow and credential management**

This repository enables you to deploy n8n on Render's free tier with automatic import of workflows and credentials directly from your Git repository. Push to deploy!

## ✨ Key Features

- **GitOps Workflow**: Push workflows/credentials to Git → Auto-deploy to Render
- **Persistent Storage**: Uses Supabase PostgreSQL (free tier)
- **Zero-Config Security**: Encrypted credentials, no plaintext secrets
- **Free Tier Optimized**: Runs entirely on Render's free tier
- **Auto-Import**: Workflows and credentials imported on every deploy

## 🗂️ How It Works

1. **Add Files**: Drop workflow JSON files in `/workflows/` and encrypted credential files in `/credentials/`
2. **Push to Git**: Commit and push your changes to the main branch
3. **Auto-Deploy**: Render automatically rebuilds and deploys your n8n instance
4. **Auto-Import**: On startup, all workflows and credentials are imported into n8n

## 🚀 Quick Start

### 1. Setup Repository
```bash
# Clone or fork this repository
git clone <your-repo-url>
cd n8n-render-deployment

# Create the required directories
mkdir -p workflows credentials
```

### 2. Configure Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New > Blueprint**
3. Connect your GitHub repository
4. **Important**: Add your Supabase password as an environment variable:
   - Key: `DB_POSTGRESDB_PASSWORD`
   - Value: Your actual Supabase database password

### 3. Deploy
Push any change to trigger your first deployment:
```bash
git add .
git commit -m "Initial n8n deployment"
git push origin main
```

## 📁 Adding Workflows

### Method 1: Export from Existing n8n
1. In your n8n instance, go to any workflow
2. Click the **3-dot menu** → **Export** → **Download**
3. Save the JSON file to the `/workflows/` directory
4. Commit and push

### Method 2: Create New Workflow Files
Create JSON files in `/workflows/` with this structure:
```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "active": true
}
```

## 🔐 Adding Credentials (Secure Method)

**⚠️ NEVER commit plaintext credentials to Git!**

### Step 1: Generate Encrypted Credential Files
1. Set up a local n8n instance with the **same** `N8N_ENCRYPTION_KEY`
2. Add your credentials in the local n8n UI
3. Export them using:
   ```bash
   n8n export:credential --output=./credentials/ --all
   ```

### Step 2: Commit Encrypted Files
```bash
git add credentials/
git commit -m "Add encrypted credentials"
git push origin main
```

The encrypted files are safe to commit because they can only be decrypted with your encryption key.

## 📋 Available Scripts

Run these from the shell in your Render service:

- `./export_workflows.sh` - Backup all workflows
- `./import_workflows.sh /path/to/backup` - Restore from backup
- `./check_health.sh` - Diagnostic health check

## 🔧 Configuration

### Environment Variables
Set these in your Render Dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `WEBHOOK_URL` | `https://your-app.onrender.com/` | Your public Render URL |
| `DB_POSTGRESDB_PASSWORD` | `your-supabase-password` | **Keep this secret!** |
| `N8N_ENCRYPTION_KEY` | `your-encryption-key` | 32+ char random string |

### Free Tier Limitations
- **Spin-down**: Service sleeps after 15 minutes of inactivity
- **Cold starts**: First request after sleep takes ~30-60 seconds
- **Build time**: ~2-3 minutes per deploy

## 🔄 Typical Workflow

1. **Develop locally** or in your live n8n instance
2. **Export workflows** to `/workflows/` directory
3. **Export credentials** to `/credentials/` directory (encrypted)
4. **Commit and push** to trigger auto-deployment
5. **Verify** the changes in your live n8n instance

## 🛠️ Troubleshooting

### Common Issues
- **502 errors**: Usually cold start delays, wait 60 seconds
- **Import failures**: Check that JSON files are valid
- **Database connection**: Verify Supabase password is set correctly

### Debug Commands
```bash
# Check service logs in Render Dashboard
# Run health check
./check_health.sh

# Manually test database connection
nc -z aws-0-us-east-2.pooler.supabase.com 6543
```

## 🎯 Production Tips

1. **Pin n8n version**: Change `n8nio/n8n:latest` to `n8nio/n8n:1.45.1` in Dockerfile
2. **Enable auth**: Set `N8N_BASIC_AUTH_ACTIVE=true` for production
3. **Monitor usage**: Track Supabase database size and Render build minutes
4. **Regular backups**: Run `./export_workflows.sh` weekly

## 🏗️ Architecture

```
GitHub Repo → Render Build → Docker Image → n8n Container
     ↓              ↓              ↓              ↓
  workflows/   →  entrypoint.sh  →  Auto-import  →  n8n Database
  credentials/ →      script      →     to       →   (Supabase)
```

---

**🎉 You're all set!** Your n8n instance now automatically stays in sync with your Git repository.