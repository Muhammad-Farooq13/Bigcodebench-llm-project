"""
Flask application for serving the LLM model
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global model and tokenizer
MODEL = None
TOKENIZER = None
DEVICE = None


def load_model_and_tokenizer():
    """Load pre-trained model and tokenizer."""
    global MODEL, TOKENIZER, DEVICE
    
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_name = os.getenv('MODEL_NAME', 'microsoft/codebert-base')
    
    logger.info(f"Loading model: {model_name}")
    logger.info(f"Using device: {DEVICE}")
    
    try:
        TOKENIZER = AutoTokenizer.from_pretrained(model_name)
        MODEL = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
        MODEL.to(DEVICE)
        MODEL.eval()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


@app.before_request
def initialize():
    """Initialize model on first request."""
    global MODEL
    if MODEL is None and not app.config.get('TESTING', False):
        try:
            load_model_and_tokenizer()
        except Exception as e:
            logger.warning(f"Could not load model: {e}")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'device': str(DEVICE),
        'model_loaded': MODEL is not None
    }), 200


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict endpoint.
    
    Request JSON:
    {
        "code": "def hello(): return 42",
        "description": "A function that returns 42"
    }
    """
    try:
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        code = data.get('code', '')
        description = data.get('description', '')
        
        if not code:
            return jsonify({'error': 'Code field is required'}), 400
        
        # Prepare input
        combined_text = f"{description} [CODE] {code}"
        
        # Tokenize
        encodings = TOKENIZER(
            combined_text,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Move to device
        input_ids = encodings['input_ids'].to(DEVICE)
        attention_mask = encodings['attention_mask'].to(DEVICE)
        
        # Predict
        with torch.no_grad():
            outputs = MODEL(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            prediction = torch.argmax(probs, dim=-1)
        
        return jsonify({
            'prediction': int(prediction.cpu().numpy()[0]),
            'confidence': float(probs.max().cpu().numpy()),
            'probabilities': probs[0].cpu().numpy().tolist(),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in predict: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/tokenize', methods=['POST'])
def tokenize():
    """
    Tokenize endpoint.
    
    Request JSON:
    {
        "text": "def hello(): return 42"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text = data['text']
        
        encodings = TOKENIZER(
            text,
            max_length=512,
            padding='max_length',
            truncation=True
        )
        
        return jsonify({
            'input_ids': encodings['input_ids'],
            'attention_mask': encodings['attention_mask'],
            'num_tokens': len(encodings['input_ids']),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in tokenize: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/info', methods=['GET'])
def model_info():
    """Get model information."""
    info = {
        'model_name': os.getenv('MODEL_NAME', 'microsoft/codebert-base'),
        'device': str(DEVICE),
        'model_loaded': MODEL is not None,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if MODEL is not None:
        info['parameters'] = sum(p.numel() for p in MODEL.parameters())
        info['trainable_parameters'] = sum(p.numel() for p in MODEL.parameters() if p.requires_grad)
    
    return jsonify(info), 200


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint.
    
    Request JSON:
    {
        "samples": [
            {"code": "...", "description": "..."},
            {"code": "...", "description": "..."}
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({'error': 'Samples field is required'}), 400
        
        samples = data['samples']
        results = []
        
        for sample in samples:
            code = sample.get('code', '')
            description = sample.get('description', '')
            
            if not code:
                results.append({'error': 'Code field is required'})
                continue
            
            combined_text = f"{description} [CODE] {code}"
            
            encodings = TOKENIZER(
                combined_text,
                max_length=512,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            input_ids = encodings['input_ids'].to(DEVICE)
            attention_mask = encodings['attention_mask'].to(DEVICE)
            
            with torch.no_grad():
                outputs = MODEL(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=-1)
                prediction = torch.argmax(probs, dim=-1)
            
            results.append({
                'prediction': int(prediction.cpu().numpy()[0]),
                'confidence': float(probs.max().cpu().numpy()),
                'probabilities': probs[0].cpu().numpy().tolist()
            })
        
        return jsonify({
            'results': results,
            'total_samples': len(samples),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch-predict: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('FLASK_PORT', 5000))
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
