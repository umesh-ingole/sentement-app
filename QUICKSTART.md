# 🚀 Quick Start Guide - Sentiment Analysis API

## 30 Seconds to Running API

### Step 1: Install Dependencies
```bash
pip install -r requirements_production.txt
```

### Step 2: Train Model (First Time Only)
```bash
python train_production.py
```
⏱️ Takes ~45 minutes on CPU (creates `bert_model/` folder)

### Step 3: Start API
```bash
python app_production.py
```

### Step 4: Test API
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this!"}'
```

✅ Done! You should see:
```json
{
  "prediction": "Positive",
  "confidence": 0.95,
  "success": true
}
```

---

## 🐳 Quick Docker Start

```bash
# Build image
docker build -t sentiment-api .

# Run container
docker run -p 5000:5000 sentiment-api
```

Or with docker-compose:
```bash
docker-compose up
```

---

## 🌐 Deploy to Hugging Face Spaces

1. Create new Space on [Hugging Face](https://huggingface.co/new-space)
   - Choose **Docker** runtime
   - Choose **Unlimited** resources

2. Push these files to your Space:
   ```
   app_production.py
   train_production.py
   requirements_production.txt
   Dockerfile
   .dockerignore
   ```

3. Space will auto-deploy!

---

## 📊 Test Different Inputs

```bash
# Positive
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This is amazing!"}'

# Negative
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Terrible product"}'

# Check Health
curl http://localhost:5000/health

# Check Status
curl http://localhost:5000/
```

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| `bert_model not found` | Run `python train_production.py` |
| `Port 5000 in use` | Change port in code or kill process on 5000 |
| `Module not found` | Run `pip install -r requirements_production.txt` |
| `Slow predictions` | Use GPU or reduce MAX_LENGTH in code |

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Ready? Start with:** `python train_production.py` → `python app_production.py`
