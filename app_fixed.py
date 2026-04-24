from flask import Flask, render_template, request, jsonify
import os
import pickle
import random
import re

app = Flask(__name__)

# Simple sentiment analyzer (fallback when transformers/torch not available)
class SimpleSentimentAnalyzer:
    """Basic sentiment analysis using keyword matching"""
    def __init__(self):
        self.positive_words = {
            'love', 'amazing', 'excellent', 'great', 'good', 'wonderful', 'fantastic',
            'best', 'awesome', 'perfect', 'satisfied', 'happy', 'brilliant', 'outstanding',
            'superb', 'recommend', 'delighted', 'impressed', 'beautiful', 'quality'
        }
        self.negative_words = {
            'hate', 'terrible', 'awful', 'bad', 'poor', 'worst', 'horrible',
            'disgusting', 'waste', 'disappointed', 'annoyed', 'frustrated', 'angry',
            'mediocre', 'broken', 'defective', 'useless', 'regret', 'never', 'avoid'
        }
    
    def predict(self, text):
        """Predict sentiment using keyword matching"""
        text_lower = text.lower()
        # Remove punctuation and split
        words = re.findall(r'\b\w+\b', text_lower)
        
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        
        total = pos_count + neg_count
        if total == 0:
            # Neutral - random between 0.5 and 0.6 confidence
            confidence = random.uniform(0.5, 0.6)
            sentiment = "Positive" if confidence > 0.55 else "Negative"
        else:
            confidence = pos_count / total
            sentiment = "Positive" if confidence >= 0.5 else "Negative"
        
        return {
            'sentiment': sentiment,
            'confidence': min(0.99, max(0.5, abs(confidence - 0.5) * 2 + 0.5))  # Scale to 0.5-0.99
        }

# Initialize the simple analyzer as fallback
analyzer = SimpleSentimentAnalyzer()

# Try to load model info
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

# Try to load advanced classifier (from transformers)
classifier = None
try:
    from transformers import pipeline
    print("Attempting to load transformer pipeline...")
    classifier = pipeline(
        'sentiment-analysis',
        model='distilbert-base-uncased-finetuned-sst-2-english',
        truncation=True
    )
    print("✓ Transformer pipeline loaded")
except Exception as e:
    print(f"⚠ Could not load transformer pipeline: {e}")
    print("Using simple keyword-based analyzer as fallback")
    classifier = None

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
        
        # Use transformer classifier if available, otherwise use simple analyzer
        if classifier:
            try:
                result = classifier(text[:512])[0]
                sentiment = "Positive" if result['label'] == 'POSITIVE' else "Negative"
                confidence = result['score']
            except Exception as e:
                print(f"Error using transformer: {e}, falling back to simple analyzer")
                result = analyzer.predict(text)
                sentiment = result['sentiment']
                confidence = result['confidence']
        else:
            result = analyzer.predict(text)
            sentiment = result['sentiment']
            confidence = result['confidence']
        
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
    classifier_status = 'available' if classifier else 'using fallback'
    return jsonify({
        'status': 'healthy',
        'message': f'Sentiment Analysis API is running ({classifier_status})',
        'classifier': classifier_status
    }), 200

@app.route('/info', methods=['GET'])
def info():
    """Get API information"""
    return jsonify({
        'name': 'Sentiment Analysis API',
        'version': '1.0',
        'model': model_info.get('model_type', 'DistilBERT/Simple Fallback'),
        'labels': model_info.get('label_names', ['Negative', 'Positive']),
        'classifier_mode': 'Transformer' if classifier else 'Simple Keyword-Based (Fallback)',
        'endpoints': {
            'GET /': 'Main web interface',
            'POST /predict': 'Predict sentiment (form or JSON)',
            'GET /health': 'Health check',
            'GET /info': 'API information'
        }
    })

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("SENTIMENT ANALYSIS API STARTING")
    print("=" * 70)
    print(f"Model: {model_info.get('model_type', 'Unknown')}")
    print(f"Classifier: {'Transformer (advanced)' if classifier else 'Simple keyword-based (fallback)'}")
    print(f"Interface: http://localhost:5000")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
