from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
import pickle

app = Flask(__name__)

# Load pre-trained sentiment analysis pipeline (no torch needed)
try:
    print("Loading sentiment analysis pipeline...")
    classifier = pipeline(
        'sentiment-analysis',
        model='distilbert-base-uncased-finetuned-sst-2-english'
    )
    print("✓ Sentiment classifier loaded successfully")
except Exception as e:
    print(f"Error loading classifier: {e}")
    classifier = None

# Try to load model info for reference
try:
    if os.path.exists("bert_model/model_info.pkl"):
        with open("bert_model/model_info.pkl", "rb") as f:
            model_info = pickle.load(f)
        print(f"✓ Model info loaded: {model_info.get('description', 'N/A')}")
    else:
        model_info = {'label_names': ['Negative', 'Positive']}
except Exception as e:
    print(f"Could not load model info: {e}")
    model_info = {'label_names': ['Negative', 'Positive']}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict sentiment for the given text"""
    try:
        # Detect if this is a form submission or JSON API request
        is_form_submission = bool(request.form)
        
        # Get text from form or JSON
        if request.form:
            text = request.form.get('text', '').strip()
        else:
            data = request.get_json() or {}
            text = data.get('text', '').strip()
        
        if not text:
            error_msg = 'Please enter some text'
            if is_form_submission:
                return render_template('index.html', prediction=error_msg, error=True)
            return jsonify({'error': error_msg, 'success': False}), 400
        
        # Use classifier pipeline for inference
        if not classifier:
            error_msg = 'Classifier not available'
            if is_form_submission:
                return render_template('index.html', prediction=error_msg, error=True)
            return jsonify({
                'error': error_msg,
                'success': False
            }), 503
        
        result = classifier(text[:512])[0]  # Limit to 512 chars
        
        # Get prediction
        sentiment = "Positive" if result['label'] == 'POSITIVE' else "Negative"
        confidence = result['score']
        
        # Return HTML for form submissions, JSON for API requests
        if is_form_submission:
            return render_template('index.html', prediction=sentiment, text=text)
        
        return jsonify({
            'sentiment': sentiment,
            'confidence': round(confidence, 4),
            'text': text,
            'success': True
        })
    
    except Exception as e:
        error_msg = f'Error: {str(e)}'
        if request.form:
            return render_template('index.html', prediction=error_msg, error=True)
        return jsonify({'error': error_msg, 'success': False}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = 'healthy' if classifier else 'degraded'
    return jsonify({
        'status': status,
        'message': 'Sentiment Analysis API is running'
    }), 200

@app.route('/info', methods=['GET'])
def info():
    """Get API information"""
    return jsonify({
        'name': 'Sentiment Analysis API',
        'version': '1.0',
        'model': model_info.get('model_type', 'DistilBERT'),
        'labels': model_info.get('label_names', ['Negative', 'Positive']),
        'endpoints': {
            'GET /': 'Main web interface',
            'POST /predict': 'Predict sentiment (form or JSON)',
            'GET /health': 'Health check',
            'GET /info': 'API information'
        },
        'usage': {
            'form': 'POST /predict with text field',
            'json': 'POST /predict with {"text": "your text"}'
        }
    }), 200

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SENTIMENT ANALYSIS FLASK APP")
    print("=" * 70)
    print("✓ Model loaded and ready")
    print("✓ Starting Flask app on http://127.0.0.1:5000")
    print("=" * 70 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
