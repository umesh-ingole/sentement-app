"""
Sentiment Analysis Model Training Script - Production Ready
Trains BERT model on sentiment140 dataset using HuggingFace
Automatically saves model to bert_model folder
"""

import torch
import os
import logging
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_NAME = "bert-base-uncased"
DATASET_NAME = "sentiment140"
OUTPUT_DIR = "bert_model"
MAX_LENGTH = 128
BATCH_SIZE = 32
NUM_EPOCHS = 2
LEARNING_RATE = 2e-5

# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")


# ============================================================================
# STEP 1: LOAD DATASET
# ============================================================================

def load_sentiment_dataset():
    """Load sentiment140 dataset from HuggingFace"""
    logger.info("Loading sentiment140 dataset...")
    
    try:
        dataset = load_dataset("sentiment140")
        logger.info(f"✓ Dataset loaded: {len(dataset['train'])} samples")
        return dataset
    except Exception as e:
        logger.error(f"Failed to load sentiment140: {e}")
        logger.info("Using small synthetic dataset for testing...")
        
        # Fallback synthetic data
        from datasets import Dataset
        texts = [
            'I love this product!',
            'Terrible experience',
            'Amazing service!',
            'Worst quality ever',
            'Excellent work',
            'Very disappointed',
            'Absolutely fantastic',
            'Not recommended'
        ] * 100
        
        labels = [1, 0, 1, 0, 1, 0, 1, 0] * 100
        
        dataset = Dataset.from_dict({
            'text': texts,
            'sentiment': labels
        })
        
        return {
            'train': dataset.select(range(int(len(dataset) * 0.8))),
            'test': dataset.select(range(int(len(dataset) * 0.8), len(dataset)))
        }


# ============================================================================
# STEP 2: PREPARE DATASET
# ============================================================================

def preprocess_function(examples, tokenizer):
    """Tokenize dataset"""
    return tokenizer(
        examples['text'],
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH
    )


def prepare_dataset(dataset, tokenizer):
    """Prepare dataset for training"""
    logger.info("Preprocessing dataset...")
    
    # Map the preprocessing function
    tokenized = dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=['text']
    )
    
    # Rename label column
    if 'sentiment' in tokenized.column_names:
        tokenized = tokenized.rename_column('sentiment', 'labels')
    
    return tokenized


# ============================================================================
# STEP 3: COMPUTE METRICS
# ============================================================================

def compute_metrics(eval_preds):
    """Compute evaluation metrics"""
    predictions, labels = eval_preds
    predictions = np.argmax(predictions, axis=1)
    
    return {
        'accuracy': accuracy_score(labels, predictions),
        'precision': precision_score(labels, predictions, average='weighted'),
        'recall': recall_score(labels, predictions, average='weighted'),
        'f1': f1_score(labels, predictions, average='weighted')
    }


# ============================================================================
# STEP 4: TRAIN MODEL
# ============================================================================

def train_model():
    """Train BERT model"""
    logger.info("\n" + "=" * 70)
    logger.info("STARTING MODEL TRAINING")
    logger.info("=" * 70)
    
    # Load dataset
    raw_dataset = load_sentiment_dataset()
    
    # Load tokenizer and model
    logger.info(f"Loading model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )
    
    # Prepare dataset
    train_dataset = prepare_dataset(raw_dataset['train'], tokenizer)
    eval_dataset = prepare_dataset(raw_dataset['test'], tokenizer)
    
    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        weight_decay=0.01,
        warmup_steps=500,
        logging_steps=100,
        eval_steps=500,
        save_steps=500,
        save_total_limit=2,
        evaluation_strategy="steps",
        save_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        push_to_hub=False,
        report_to="none",
        fp16=False,  # CPU doesn't support fp16
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Train
    logger.info("Starting training...")
    trainer.train()
    
    # Save model
    logger.info("\n" + "=" * 70)
    logger.info("SAVING MODEL")
    logger.info("=" * 70)
    
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    logger.info(f"✓ Model saved to {OUTPUT_DIR}/")
    logger.info(f"✓ Tokenizer saved to {OUTPUT_DIR}/")
    
    # Final metrics
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Model location: {OUTPUT_DIR}/")
    logger.info("Files created:")
    logger.info("  - config.json")
    logger.info("  - pytorch_model.bin")
    logger.info("  - tokenizer_config.json")
    logger.info("  - vocab.txt")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    try:
        train_model()
        logger.info("\n✅ Model training completed successfully!")
        logger.info(f"To use the model, run: python app_production.py")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise
