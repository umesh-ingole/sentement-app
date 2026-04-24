# Deploy to Render

## Quick Deploy Guide

### Step 1: Connect GitHub Repository
1. Go to [render.com](https://render.com)
2. Sign in with GitHub account
3. Click "New +" > "Web Service"
4. Connect your GitHub repository

### Step 2: Configure Service
- **Name:** sentiment-analysis-api
- **Environment:** Docker
- **Region:** Choose closest to you
- **Branch:** main

### Step 3: Environment Variables (Optional)
No environment variables required for this app.

### Step 4: Deploy
Click "Create Web Service" and Render will:
1. Build Docker image
2. Deploy automatically
3. Assign you a public URL

### Deployment Status
Your API will be available at:
```
https://your-service-name.onrender.com
```

### Test Your Deployment
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Make prediction
curl -X POST https://your-service-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'
```

### Troubleshooting

**Build Fails:**
- Check Dockerfile syntax
- Ensure all files are in git (not in .gitignore)
- Check requirements.txt for version conflicts

**Service Won't Start:**
- Check logs in Render dashboard
- Verify app is listening on 0.0.0.0:5000
- Check for missing dependencies

**Slow First Request:**
- First request loads the model (~10 seconds)
- Subsequent requests are faster

## Local Testing Before Deploy

```bash
# Build Docker image
docker build -t sentiment-api .

# Run locally
docker run -p 5000:5000 sentiment-api

# Test
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Great product!"}'
```
