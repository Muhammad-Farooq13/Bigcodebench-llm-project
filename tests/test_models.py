"""Test suite for model training and evaluation"""

import pytest
import numpy as np
import torch
from unittest.mock import Mock, patch, MagicMock
from src.models.evaluator import ModelEvaluator, MetricsComputer


class TestModelEvaluator:
    """Tests for ModelEvaluator"""
    
    def test_classification_metrics(self):
        """Test classification metrics computation"""
        evaluator = ModelEvaluator(None, None)
        
        predictions = np.array([0, 1, 1, 0, 1, 0])
        references = np.array([0, 1, 0, 0, 1, 1])
        
        metrics = evaluator.evaluate_classification(predictions, references)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1' in metrics
        assert 'confusion_matrix' in metrics
        
        # All metrics should be floats or lists
        assert isinstance(metrics['accuracy'], float)
        assert isinstance(metrics['f1'], float)
    
    def test_regression_metrics(self):
        """Test regression metrics computation"""
        evaluator = ModelEvaluator(None, None)
        
        predictions = np.array([1.0, 2.0, 3.0, 4.0])
        references = np.array([1.1, 1.9, 3.1, 3.9])
        
        metrics = evaluator.evaluate_regression(predictions, references)
        
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2' in metrics
        
        # Metrics should be reasonable
        assert metrics['mse'] >= 0
        assert metrics['mae'] >= 0


class TestMetricsComputer:
    """Tests for MetricsComputer"""
    
    def test_code_similarity(self):
        """Test code similarity computation"""
        code1 = "def hello():\n    return 42"
        code2 = "def hello():\n    return 42"
        
        similarity = MetricsComputer.compute_code_similarity(code1, code2)
        
        assert 0 <= similarity <= 1
        assert similarity == 1.0  # Identical codes should have similarity 1.0
    
    def test_code_similarity_different(self):
        """Test code similarity with different codes"""
        code1 = "def add(a, b):\n    return a + b"
        code2 = "def mul(a, b):\n    return a * b"
        
        similarity = MetricsComputer.compute_code_similarity(code1, code2)
        
        assert 0 < similarity < 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
