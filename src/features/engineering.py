"""
Feature engineering module for code and text features
"""

import logging
from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re

logger = logging.getLogger(__name__)


class CodeFeatureExtractor:
    """Extract features from code snippets"""
    
    @staticmethod
    def extract_code_metrics(code: str) -> Dict[str, float]:
        """
        Extract code metrics.
        
        Args:
            code: Code string
            
        Returns:
            Dictionary with code metrics
        """
        lines = code.split('\n')
        
        metrics = {
            'num_lines': len(lines),
            'num_functions': code.count('def '),
            'num_classes': code.count('class '),
            'num_imports': code.count('import '),
            'code_length': len(code),
            'avg_line_length': np.mean([len(line) for line in lines]) if lines else 0,
            'num_comments': sum(1 for line in lines if line.strip().startswith('#')),
            'indent_levels': CodeFeatureExtractor._count_max_indent(code),
        }
        
        return metrics
    
    @staticmethod
    def _count_max_indent(code: str) -> int:
        """Count maximum indentation level"""
        max_indent = 0
        for line in code.split('\n'):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)  # Assuming 4-space indent
        return max_indent
    
    @staticmethod
    def extract_keywords(code: str, language: str = 'python') -> List[str]:
        """
        Extract programming keywords from code.
        
        Args:
            code: Code string
            language: Programming language
            
        Returns:
            List of keywords found
        """
        keywords = {
            'python': ['def', 'class', 'import', 'from', 'if', 'else', 'for', 'while', 
                      'try', 'except', 'with', 'return', 'lambda', 'async', 'await'],
            'javascript': ['function', 'const', 'let', 'var', 'class', 'import', 'export',
                          'async', 'await', 'if', 'else', 'for', 'while', 'return'],
            'java': ['class', 'public', 'private', 'protected', 'static', 'void', 'int',
                    'String', 'List', 'Map', 'Set', 'import', 'return'],
        }
        
        keywords_list = keywords.get(language.lower(), [])
        found_keywords = [kw for kw in keywords_list if kw in code]
        
        return found_keywords


class TextFeatureExtractor:
    """Extract features from text descriptions"""
    
    def __init__(self):
        """Initialize text feature extractor"""
        self.tfidf_vectorizer = None
        self.count_vectorizer = None
    
    def fit_tfidf(self, texts: List[str], max_features: int = 1000):
        """
        Fit TF-IDF vectorizer on texts.
        
        Args:
            texts: List of text strings
            max_features: Maximum number of features
        """
        self.tfidf_vectorizer = TfidfVectorizer(max_features=max_features)
        self.tfidf_vectorizer.fit(texts)
        logger.info(f"Fitted TF-IDF vectorizer with {max_features} features")
    
    def fit_count(self, texts: List[str], max_features: int = 1000):
        """
        Fit count vectorizer on texts.
        
        Args:
            texts: List of text strings
            max_features: Maximum number of features
        """
        self.count_vectorizer = CountVectorizer(max_features=max_features)
        self.count_vectorizer.fit(texts)
        logger.info(f"Fitted count vectorizer with {max_features} features")
    
    def extract_text_metrics(self, text: str) -> Dict[str, float]:
        """
        Extract text metrics.
        
        Args:
            text: Text string
            
        Returns:
            Dictionary with text metrics
        """
        words = text.split()
        sentences = text.split('.')
        
        metrics = {
            'num_words': len(words),
            'num_sentences': len([s for s in sentences if s.strip()]),
            'text_length': len(text),
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'unique_words': len(set(words)),
            'diversity': len(set(words)) / len(words) if words else 0,
        }
        
        return metrics
    
    def transform_tfidf(self, texts: List[str]):
        """Transform texts using fitted TF-IDF vectorizer"""
        if self.tfidf_vectorizer is None:
            raise ValueError("TF-IDF vectorizer not fitted")
        return self.tfidf_vectorizer.transform(texts)
    
    def transform_count(self, texts: List[str]):
        """Transform texts using fitted count vectorizer"""
        if self.count_vectorizer is None:
            raise ValueError("Count vectorizer not fitted")
        return self.count_vectorizer.transform(texts)


class FeatureEngineer:
    """Combine code and text features"""
    
    def __init__(self):
        """Initialize feature engineer"""
        self.code_extractor = CodeFeatureExtractor()
        self.text_extractor = TextFeatureExtractor()
    
    def create_features(
        self,
        code: str,
        description: str,
        language: str = 'python'
    ) -> Dict[str, Any]:
        """
        Create combined features from code and text.
        
        Args:
            code: Code string
            description: Description text
            language: Programming language
            
        Returns:
            Dictionary with all extracted features
        """
        features = {
            'code_metrics': self.code_extractor.extract_code_metrics(code),
            'code_keywords': self.code_extractor.extract_keywords(code, language),
            'text_metrics': self.text_extractor.extract_text_metrics(description),
        }
        
        return features


if __name__ == '__main__':
    # Example usage
    code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    
    description = "Write a function to compute the nth Fibonacci number using recursion"
    
    engineer = FeatureEngineer()
    features = engineer.create_features(code, description, 'python')
    
    print("Extracted Features:")
    for key, value in features.items():
        print(f"  {key}: {value}")
