# 🚀 Deploy to Hugging Face Spaces

## Quick Deploy (5 Steps)

### Step 1: Create Space on HuggingFace

1. Go to https://huggingface.co/new-space
2. Fill in details:
   - **Space name:** `sentiment-analysis`
   - **License:** OpenRAIL (or your choice)
   - **Space SDK:** Docker
   - **Space hardware:** CPU (Free)
3. Click **Create Space**

### Step 2: Clone Space Repository

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/sentiment-analysis
cd sentiment-analysis
```

### Step 3: Copy Files

Copy these files to your Space directory:

```bash
cp app_production.py .
cp train_production.py .
cp requirements_production.txt .
cp Dockerfile .
cp .dockerignore .
```

Or download from GitHub/local:
- `app_production.py`
- `train_production.py` 
- `requirements_production.txt`
- `Dockerfile`
- `.dockerignore`

### Step 4: Commit & Push

```bash
git add .
git commit -m "Add Sentiment Analysis API"
git push
```

### Step 5: Wait for Deploy

- HF Spaces will automatically:
  - Build Docker image (~5-10 minutes)
  - Pull dependencies
  - Start your API
  - Assign you a public URL

---

## 🌐 Access Your API

Once deployed, your API will be available at:

```
https://YOUR_USERNAME-sentiment-analysis.hf.space
```

### Test It

```bash
curl -X POST https://YOUR_USERNAME-sentiment-analysis.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'
```

Response:
```json
{
  "prediction": "Positive",
  "confidence": 0.9876,
  "success": true
}
```

---

## 📊 File Structure in Space

```
sentiment-analysis/
├── app_production.py
├── train_production.py
├── requirements_production.txt
├── Dockerfile
├── .dockerignore
└── README.md (optional)
```

---

## ⚙️ Configuration

### Increase Computing Power

If you need more resources:

1. Go to Space settings
2. Select **Hardware:**
   - **CPU (Free)** - Limited resources
   - **GPU (Paid)** - Faster predictions (~30ms)
   - **A100 (Premium)** - Very fast inference

### Restart Space

If deployment fails:

1. Go to Space settings
2. Click **Restart Space**
3. Check build logs if it fails again

---

## 🐛 Troubleshooting

### Build Fails

**Check logs:**
1. Go to Space page
2. Click **View logs**
3. Look for error messages

**Common issues:**
- Missing requirements file
- Invalid Dockerfile syntax
- Port already in use

**Solution:**
```bash
# Fix locally first
docker build -t test .

# Then push again
git add .
git commit -m "Fix build"
git push
```

### API Not Responding

**Check health endpoint:**
```bash
curl https://YOUR_USERNAME-sentiment-analysis.hf.space/health
```

**If not responding:**
1. Check Space logs
2. Model might be loading (first time ~2 minutes)
3. Try refreshing after 5 minutes

### Slow Predictions

**First request slow?** - Model is loading (~2 minutes on CPU)

**Requests still slow?**
- Upgrade to GPU hardware
- Reduce MAX_LENGTH in app_production.py to 64

---

## 🔗 Share Your API

### Create a Gradio Interface (Optional)

Create `gradio_interface.py`:

```python
import gradio as gr
import requests
import json

API_URL = "http://localhost:5000"  # Will be Space URL

def predict_sentiment(text):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},
            timeout=30
        )
        data = response.json()
        
        if data.get('success'):
            return f"Prediction: {data['prediction']}\nConfidence: {data['confidence']:.4f}"
        else:
            return f"Error: {data.get('error')}"
    except Exception as e:
        return f"Error: {str(e)}"

interface = gr.Interface(
    fn=predict_sentiment,
    inputs="text",
    outputs="text",
    title="Sentiment Analysis"
)

interface.launch()
```

Then update your Dockerfile to include Gradio.

---

## 📈 Monitor Your Space

### View Logs

```bash
# SSH into Space (if available)
# Or check web logs

# Container logs show:
- Model loading progress
- API requests
- Errors and warnings
```

### Health Monitoring

```bash
# Regular health checks
curl -X GET https://YOUR_USERNAME-sentiment-analysis.hf.space/health
```

---

## 💰 Cost Estimation

| Hardware | Cost | Inference Time |
|----------|------|-----------------|
| CPU (Free) | Free | 100-150ms |
| T4 GPU | ~$0.50/hour | 20-30ms |
| A100 GPU | ~$2/hour | 5-10ms |

---

## 🔐 Security

HuggingFace Spaces provides:
- ✅ HTTPS by default
- ✅ DDoS protection
- ✅ Rate limiting (optional)
- ✅ Private spaces (pro feature)

---

## 🎯 Best Practices

1. **Always test locally first**
   ```bash
   docker build -t test .
   docker run -p 5000:5000 test
   ```

2. **Use git tags for versions**
   ```bash
   git tag -a v1.0 -m "Production release"
   git push origin v1.0
   ```

3. **Monitor logs regularly**
   - Check for errors
   - Monitor resource usage
   - Track prediction counts

4. **Add README to Space**
   - Link to full documentation
   - Usage examples
   - API documentation

---

## 📝 Space Readme Template

Create `README.md` in your Space:

```markdown
# Sentiment Analysis API

A production-ready API for sentiment analysis using BERT.

## Usage

**Positive Sentiment:**
```json
{
  "text": "I absolutely love this product!"
}
```

**Negative Sentiment:**
```json
{
  "text": "This is terrible and doesn't work."
}
```

## Response

```json
{
  "prediction": "Positive",
  "confidence": 0.95,
  "success": true
}
```

## Documentation

- [Full README](https://github.com/YOUR_REPO)
- [API Docs](https://github.com/YOUR_REPO/README.md)
- [Source Code](https://github.com/YOUR_REPO)

## Deployed at

This API is deployed on Hugging Face Spaces.
```

---

## 🚀 Advanced: Custom Domain

HuggingFace Pro users can add custom domain:

1. Get a domain (e.g., sentiment-api.com)
2. Go to Space settings
3. Add custom domain
4. Configure DNS records

---

## 📞 Support

**Issues?** Check:
- HF Spaces documentation: https://huggingface.co/docs/hub/spaces
- Docker documentation: https://docs.docker.com/
- Flask documentation: https://flask.palletsprojects.com/

**Still stuck?** 
- Check Space logs for error messages
- Restart Space and rebuild
- Delete and recreate if necessary

---

## ✅ Deployment Checklist

- [ ] Created HF Space
- [ ] Cloned Space repository
- [ ] Copied all required files
- [ ] Committed changes
- [ ] Pushed to Space
- [ ] Build completed successfully
- [ ] Tested health endpoint
- [ ] Made first prediction
- [ ] Shared Space URL
- [ ] Added documentation

---

**Your Space is Live at:**

```
https://YOUR_USERNAME-sentiment-analysis.hf.space
```

**Share this link with others!**

---

**Need help?** See [README.md](README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)
