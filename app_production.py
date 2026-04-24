"""
Sentiment Analysis API - Production Ready
Uses BERT model for sentiment classification
Runs on Flask with JSON API endpoints
"""

import torch
import os
import logging
from flask import Flask, jsonify, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Device configuration
DEVICE = torch.device("cpu")
logger.info(f"Using device: {DEVICE}")

# Load model and tokenizer
def load_model():
    """Load BERT model and tokenizer"""
    try:
        model_path = "bert_model"
        
        # Try to load from saved model
        if os.path.exists(model_path):
            logger.info(f"Loading model from {model_path}...")
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            logger.info("✓ Model loaded from bert_model folder")
        else:
            # Fallback to pre-trained model
            logger.warning("bert_model folder not found, using pre-trained model...")
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            logger.info(f"✓ Model loaded: {model_name}")
        
        # Set model to evaluation mode
        model.eval()
        model.to(DEVICE)
        
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

# Load model and tokenizer at startup
try:
    model, tokenizer = load_model()
    logger.info("✓ Application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize application: {e}")
    raise


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint - API is running"""
    return jsonify({
        'status': 'running',
        'message': 'Sentiment Analysis API is running',
        'version': '1.0'
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict sentiment for given text
    
    Request:
        JSON: {"text": "your text here"}
    
    Response:
        JSON: {
            "prediction": "Positive" or "Negative",
            "confidence": 0.0-1.0,
            "success": true
        }
    """
    try:
        # Get text from JSON request
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        
        # Validate input
        if not text:
            return jsonify({
                'error': 'Missing or empty text field',
                'success': False
            }), 400
        
        if len(text) > 512:
            text = text[:512]
            logger.info("Text truncated to 512 characters")
        
        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            padding='max_length',
            max_length=128
        )
        
        # Move to device
        inputs = {key: val.to(DEVICE) for key, val in inputs.items()}
        
        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get prediction
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=1).item()
        probabilities = torch.softmax(logits, dim=1)
        confidence = probabilities[0][predicted_label].item()
        
        # Convert label to sentiment
        sentiment = "Positive" if predicted_label == 1 else "Negative"
        
        logger.info(f"Prediction: {sentiment} (confidence: {confidence:.4f})")
        
        return jsonify({
            'prediction': sentiment,
            'confidence': round(confidence, 4),
            'success': True
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'sentiment-analysis',
        'version': '1.0'
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'success': False}), 405


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error', 'success': False}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SENTIMENT ANALYSIS API - PRODUCTION")
    print("=" * 70)
    print("✓ Model loaded and ready")
    print("✓ Starting Flask app on 0.0.0.0:5000")
    print("=" * 70 + "\n")
    
    # For production, use gunicorn instead
    # For development/testing:
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )
