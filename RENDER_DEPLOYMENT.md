# Deploy Sentiment Analysis API to Render

## 🚀 Quick Start (5 Minutes)

### Step 1: Connect Repository
1. Go to [render.com](https://render.com) and sign in with GitHub
2. Click **New +** → **Web Service**
3. Select your GitHub repository `sentement-app`
4. Click **Connect**

### Step 2: Configure Service
Fill in the deployment form:
- **Name:** sentiment-analysis-api
- **Environment:** Docker
- **Region:** Choose nearest to you
- **Plan:** Free (sufficient for testing)
- Leave other options as default

### Step 3: Deploy
Click **Create Web Service** and wait for build to complete (~5-10 minutes)

### Step 4: Get Your URL
Once deployed, your API is available at:
```
https://sentiment-analysis-api.onrender.com
```

---

## 🧪 Test Your Deployment

### Health Check
```bash
curl https://sentiment-analysis-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "sentiment-analysis",
  "version": "1.0"
}
```

### Make a Prediction
```bash
curl -X POST https://sentiment-analysis-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I absolutely love this product!"}'
```

Expected response:
```json
{
  "prediction": "Positive",
  "confidence": 0.9876,
  "success": true
}
```

---

## ⚙️ Configuration

### Environment Variables
Render automatically sets these from Dockerfile:
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

### Custom Environment Variables (Optional)
1. Go to your service on Render dashboard
2. Click **Environment**
3. Add any custom variables
4. Service redeploys automatically

---

## 🔧 Troubleshooting

### Build Fails with "pip install failed"
**Solution:**
1. Check Dockerfile syntax (valid JSON array in CMD)
2. Ensure all files are committed to git
3. Verify requirements_production.txt exists
4. Try rebuilding: Dashboard → **Manual Deploy**

### Service Won't Start ("503 Service Unavailable")
**Possible causes:**
1. App crashed - check **Logs** in Render dashboard
2. Port not exposed - ensure `EXPOSE 5000` in Dockerfile
3. Health check failing - ensure `/health` endpoint exists

Check logs:
```
Dashboard → Your Service → Logs
```

### First Request Slow (10+ seconds)
This is **normal** - the model is loading. Subsequent requests are ~100ms.

### Model Not Found Error
**This is fine!** The app uses a pre-trained model by default:
- Falls back to `distilbert-base-uncased-finetuned-sst-2-english`
- Predictions still work perfectly
- To use custom model, train locally and commit `bert_model/` (or use Docker volume)

---

## 📊 Performance Notes

- **Memory:** ~2GB (model loading)
- **Startup:** ~60 seconds (first request loads model)
- **Inference:** ~100-150ms per prediction
- **Concurrent:** Handles ~10-20 simultaneous requests
- **Free tier sleep:** Render free tier goes to sleep after 15 min of inactivity
  - Next request takes ~30 seconds to wake up (normal)

---

## 🔄 Auto-Deploy from GitHub

Every push to `master` automatically redeploys:

```bash
git add .
git commit -m "Your changes"
git push origin master
```

Render watches the repo and rebuilds automatically.

---

## 📁 What Gets Deployed

Render builds a Docker image with:
- ✅ Python 3.9 slim image
- ✅ Flask API (app_production.py)
- ✅ All dependencies from requirements_production.txt
- ✅ Templates for web UI (optional)
- ✅ Training script (for manual use if needed)

What's **NOT** deployed:
- ❌ `.venv/` folder (too large)
- ❌ `__pycache__/` (auto-generated)
- ❌ `bert_model/` (in .gitignore, uses fallback instead)

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build timeout | Increase timeout or reduce requirements |
| Port conflict | Use port 5000 (default) |
| No module error | Check requirements_production.txt |
| Memory error | Free tier has 0.5GB (model needs ~2GB) → upgrade to paid |
| SSL error | Render provides free SSL automatically |

---

## 📈 Upgrade from Free Tier

To use custom BERT model or need more resources:

1. Upgrade plan: **Dashboard → Instance Type → Upgrade**
2. Options:
   - **Starter:** $7/month, 0.5GB RAM, 1 CPU
   - **Standard:** $12/month, 2GB RAM, 2 CPU
   - **Pro:** Higher specs available

---

## 🔐 Security

- HTTPS/SSL: ✅ Automatic (enabled by Render)
- No authentication: ⚠️ API is public
- To add authentication:
  1. Edit `app_production.py`
  2. Add Flask-HTTPAuth or API key middleware
  3. Redeploy

---

## 📝 Monitoring

### View Logs
```
Dashboard → Your Service → Logs
```

### Check Health
```
Dashboard → Your Service → Health
```

### Restart Service
```
Dashboard → Your Service → Restart
```

---

## 🤝 Need Help?

- **Render Docs:** https://render.com/docs
- **GitHub Issues:** https://github.com/umesh-ingole/sentement-app/issues
- **Flask Docs:** https://flask.palletsprojects.com/
- **Gunicorn Docs:** https://gunicorn.org/
