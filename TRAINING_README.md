# Sentiment Analysis BERT Training Script

A simplified Python script for training a BERT-based sentiment classifier using the Sentiment140 dataset from Hugging Face.

## Quick Start

### 1. Install Dependencies
```bash
pip install transformers torch datasets scikit-learn pandas
```

### 2. Run Training
```bash
python train_sentiment_model.py
```

The script will automatically:
- Download Sentiment140 dataset from Hugging Face
- Use 20,000 samples for faster training
- Train for 2 epochs
- Save the model and tokenizer to `bert_model/` folder

## Requirements

- Python 3.7+
- PyTorch 2.0+ (CPU or GPU)
- Hugging Face Transformers 4.30+
- Hugging Face Datasets 2.10+
- scikit-learn 1.3+
- pandas 2.0+

## Features

✅ **Auto Dataset Loading:**
- Automatically downloads Sentiment140 from Hugging Face
- No manual CSV download required
- Falls back to synthetic data if download fails

✅ **Tokenization:**
- BERT tokenizer (bert-base-uncased)
- Max length: 128 tokens
- Automatic padding and truncation

✅ **Training:**
- 2 epochs (quick training)
- Batch size: 8
- AdamW optimizer (lr=2e-5)
- 20,000 samples for faster iteration

✅ **Evaluation:**
- Classification report with precision, recall, F1
- Supports negative/positive label mapping

✅ **Model Saving:**
- Saves model to `bert_model/` folder
- Saves tokenizer to `bert_model/` folder
- Ready to use with transformers library

## Output

Training produces:
- Loss per epoch
- Progress tracking every 100 batches
- Final classification report
- Saved model weights and tokenizer

## Using the Trained Model

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load
model = BertForSequenceClassification.from_pretrained("bert_model")
tokenizer = BertTokenizer.from_pretrained("bert_model")

# Predict
text = "I love this product!"
inputs = tokenizer(text, return_tensors="pt", max_length=128, truncation=True, padding=True)

with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

result = "Positive" if prediction == 1 else "Negative"
print(result)
```

## Troubleshooting

**No dataset connection?**
- Script automatically creates synthetic data for testing
- For real training, ensure internet connection

**Out of Memory?**
- Reduce batch size: change `batch_size=8` to `batch_size=4`
- Use fewer samples: modify line with `sample_size`

**Slow training?**
- CPU training is normal (5-10 min for 20k samples)
- Use GPU if available for faster training
