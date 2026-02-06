"""Test suite for data loading and preprocessing"""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from src.data.loader import BigCodeBenchLoader, load_bigcodebench
from src.data.preprocessor import CodeBenchPreprocessor, DataValidator


class TestBigCodeBenchLoader:
    """Tests for BigCodeBenchLoader"""
    
    def test_loader_initialization(self):
        """Test loader initialization"""
        loader = BigCodeBenchLoader(cache_dir='./test_data')
        assert loader.cache_dir == './test_data'
    
    def test_clean_code(self):
        """Test code cleaning"""
        preprocessor = CodeBenchPreprocessor()
        
        code = "def hello():\n    # This is a comment\n    return 42"
        cleaned = preprocessor.clean_code(code)
        
        assert 'def hello()' in cleaned
        assert 'return 42' in cleaned
    
    def test_clean_text(self):
        """Test text cleaning"""
        preprocessor = CodeBenchPreprocessor()
        
        text = "Write  a  function   to  compute  sum"
        cleaned = preprocessor.clean_text(text)
        
        assert 'Write' in cleaned
        assert 'sum' in cleaned
        assert '  ' not in cleaned  # Extra spaces removed


class TestDataValidator:
    """Tests for DataValidator"""
    
    def test_valid_sample(self):
        """Test sample validation"""
        sample = {
            'input_ids': [101, 2054, 2003, 102],
            'attention_mask': [1, 1, 1, 1],
        }
        
        assert DataValidator.validate_sample(sample) is True
    
    def test_invalid_sample_missing_field(self):
        """Test validation with missing field"""
        sample = {
            'input_ids': [101, 2054, 2003, 102],
        }
        
        assert DataValidator.validate_sample(sample) is False
    
    def test_invalid_sample_empty_input(self):
        """Test validation with empty input"""
        sample = {
            'input_ids': [],
            'attention_mask': [],
        }
        
        assert DataValidator.validate_sample(sample) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
