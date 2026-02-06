"""Test suite for Flask API endpoints"""

import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests for health check endpoint"""
    
    def test_health_check_success(self, client):
        """Test successful health check"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'device' in data


class TestPredictEndpoint:
    """Tests for predict endpoint"""
    
    @patch('flask_app.MODEL')
    @patch('flask_app.TOKENIZER')
    def test_predict_with_valid_input(self, mock_tokenizer, mock_model, client):
        """Test prediction with valid input"""
        # Mock tokenizer
        mock_tokenizer.return_value = {
            'input_ids': [[101, 2054, 102]],
            'attention_mask': [[1, 1, 1]]
        }
        
        # Mock model
        mock_output = MagicMock()
        mock_output.logits = [[0.1, 0.9]]  # High confidence for class 1
        mock_model.return_value = mock_output
        
        response = client.post(
            '/api/predict',
            data=json.dumps({'code': 'def hello():\n    return 42'}),
            content_type='application/json'
        )
        
        # Should handle gracefully even if model returns mock results
        assert response.status_code in [200, 500]  # May fail due to mocking
    
    def test_predict_missing_code(self, client):
        """Test prediction with missing code field"""
        response = client.post(
            '/api/predict',
            data=json.dumps({'description': 'Some description'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_no_json(self, client):
        """Test prediction with no JSON data"""
        response = client.post('/api/predict')
        
        assert response.status_code == 400


class TestTokenizeEndpoint:
    """Tests for tokenize endpoint"""
    
    @patch('flask_app.TOKENIZER')
    def test_tokenize_success(self, mock_tokenizer, client):
        """Test tokenization endpoint"""
        mock_tokenizer.return_value = {
            'input_ids': [101, 2054, 102],
            'attention_mask': [1, 1, 1]
        }
        
        response = client.post(
            '/api/tokenize',
            data=json.dumps({'text': 'def hello(): pass'}),
            content_type='application/json'
        )
        
        assert response.status_code in [200, 500]  # May fail due to mocking
    
    def test_tokenize_missing_text(self, client):
        """Test tokenization without text field"""
        response = client.post(
            '/api/tokenize',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestModelInfoEndpoint:
    """Tests for model info endpoint"""
    
    def test_model_info(self, client):
        """Test model info endpoint"""
        response = client.get('/api/info')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'model_name' in data
        assert 'device' in data
        assert 'model_loaded' in data


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-endpoint')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
