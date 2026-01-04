---
name: railway
description: Railway deployment and troubleshooting procedures
version: 1.0.0
---

# Railway Deployment Skill

Procedural knowledge for deploying, debugging, and managing Railway services.

## Prerequisites

- Railway CLI installed: `npm install -g @railway/cli`
- Authenticated: `railway login`
- Project linked: `railway link`

## Quick Reference

### Deployment Commands
```bash
railway up                    # Deploy current directory
railway up --detach           # Deploy without streaming logs
railway deploy                # Trigger deployment from linked repo
railway redeploy              # Redeploy current service
```

### Inspection Commands
```bash
railway status                # Current project/service status
railway logs                  # Stream live logs
railway logs --latest         # Most recent deployment logs
railway logs -d <id>          # Specific deployment logs
railway logs -d <id> --build  # Build-phase logs only
```

### Environment Management
```bash
railway variables             # List all variables
railway variables set KEY=val # Set variable
railway variables get KEY     # Get specific variable
railway run <cmd>             # Run command with Railway env
```

### Service Management
```bash
railway service               # List services in project
railway domain                # Manage custom domains
railway volume                # Manage persistent volumes
```

## Debugging Decision Tree

```
Deploy Failed?
├── Build Phase Failed
│   ├── Check: railway logs -d <id> --build
│   ├── Missing deps? → Update package.json/requirements.txt
│   ├── Wrong runtime? → Set NIXPACKS_NODE_VERSION or similar
│   └── OOM during build? → Contact Railway for larger builder
│
├── Runtime Crash
│   ├── Check: railway logs --latest
│   ├── Port binding? → Ensure binding to 0.0.0.0:$PORT
│   ├── Missing env var? → railway variables set KEY=value
│   └── Health check fail? → Verify /health returns 200
│
└── Networking Issue
    ├── Domain not working? → Check DNS with: dig <domain>
    ├── SSL pending? → Wait 5-10 min for Let's Encrypt
    └── Service-to-service? → Use RAILWAY_PRIVATE_DOMAIN
```

## Configuration Files

### railway.json (Legacy)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```

### railway.toml (Preferred)
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "npm start"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

## Common Fixes

### Port Binding (Node.js)
```javascript
const port = process.env.PORT || 3000;
app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});
```

### Port Binding (Python/FastAPI)
```python
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
```

### Health Check Endpoint
```javascript
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});
```

### Database Connection (with retry)
```javascript
const connectWithRetry = async () => {
  const maxRetries = 5;
  for (let i = 0; i < maxRetries; i++) {
    try {
      await db.connect(process.env.DATABASE_URL);
      console.log('Database connected');
      return;
    } catch (err) {
      console.log(`DB connection attempt ${i + 1} failed, retrying...`);
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  throw new Error('Database connection failed after retries');
};
```
