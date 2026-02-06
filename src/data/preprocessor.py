"""
Data preprocessing utilities for code and text samples
"""

import logging
from typing import Dict, List, Optional, Any
import re
from pathlib import Path

logger = logging.getLogger(__name__)


class CodeBenchPreprocessor:
    """Preprocess code and text samples from BigCodeBench dataset."""
    
    def __init__(self, max_length: int = 512, remove_comments: bool = False):
        """
        Initialize preprocessor.
        
        Args:
            max_length: Maximum sequence length
            remove_comments: Whether to remove code comments
        """
        self.max_length = max_length
        self.remove_comments = remove_comments
        
    def clean_code(self, code: str) -> str:
        """
        Clean code string.
        
        Args:
            code: Raw code string
            
        Returns:
            Cleaned code
        """
        if not isinstance(code, str):
            return ""
        
        # Remove extra whitespace
        code = code.strip()
        
        # Remove comments if requested
        if self.remove_comments:
            code = self._remove_comments(code)
        
        return code
    
    def _remove_comments(self, code: str) -> str:
        """Remove Python-style comments from code."""
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove single-line comments
            if '#' in line:
                code_part = line.split('#')[0]
                cleaned_lines.append(code_part.rstrip())
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def clean_text(self, text: str) -> str:
        """
        Clean text string (description, problem, etc.).
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\:]', '', text)
        
        return text.strip()
    
    def process_sample(
        self,
        sample: Dict[str, Any],
        tokenizer,
        lang_column: str = 'language',
        code_column: str = 'starter_code',
        description_column: str = 'description',
        label_column: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a single sample.
        
        Args:
            sample: Sample dictionary
            tokenizer: Tokenizer for encoding
            lang_column: Column name for language
            code_column: Column name for code
            description_column: Column name for description
            label_column: Optional label column
            
        Returns:
            Processed sample with tokenized features
        """
        # Extract and clean components
        code = self.clean_code(sample.get(code_column, ""))
        description = self.clean_text(sample.get(description_column, ""))
        language = sample.get(lang_column, "unknown")
        
        # Create combined input
        combined_text = f"[LANG: {language}] {description} [CODE] {code}"
        
        # Tokenize
        try:
            encoded = tokenizer(
                combined_text,
                max_length=self.max_length,
                padding='max_length',
                truncation=True,
                return_tensors=None
            )
            
            result = {
                'input_ids': encoded['input_ids'],
                'attention_mask': encoded['attention_mask'],
                'language': language
            }
            
            # Add label if available
            if label_column and label_column in sample:
                result['label'] = sample[label_column]
            
            return result
            
        except Exception as e:
            logger.warning(f"Error processing sample: {str(e)}")
            return {}
    
    def process_batch(
        self,
        examples: Dict[str, List],
        tokenizer,
        **kwargs
    ) -> Dict[str, List]:
        """
        Process a batch of samples.
        
        Args:
            examples: Batch of samples
            tokenizer: Tokenizer for encoding
            **kwargs: Additional arguments for process_sample
            
        Returns:
            Batch of processed samples
        """
        batch_size = len(examples.get(list(examples.keys())[0], []))
        processed = {
            'input_ids': [],
            'attention_mask': [],
            'language': [],
        }
        
        for i in range(batch_size):
            sample = {k: v[i] for k, v in examples.items()}
            processed_sample = self.process_sample(sample, tokenizer, **kwargs)
            
            for key, value in processed_sample.items():
                if key not in processed:
                    processed[key] = []
                processed[key].append(value)
        
        return processed


class DataValidator:
    """Validate preprocessed data quality."""
    
    @staticmethod
    def validate_sample(sample: Dict[str, Any]) -> bool:
        """
        Validate a single sample.
        
        Args:
            sample: Sample to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ['input_ids', 'attention_mask']
        
        for field in required_fields:
            if field not in sample or sample[field] is None:
                return False
        
        # Check for non-empty input
        if not sample['input_ids']:
            return False
        
        return True
    
    @staticmethod
    def get_statistics(dataset) -> Dict[str, Any]:
        """
        Get statistics about dataset.
        
        Args:
            dataset: Dataset to analyze
            
        Returns:
            Dictionary with statistics
        """
        if len(dataset) == 0:
            return {}
        
        stats = {
            'total_samples': len(dataset),
            'valid_samples': sum(1 for s in dataset if DataValidator.validate_sample(s)),
        }
        
        # Length statistics
        lengths = [len(s.get('input_ids', [])) for s in dataset]
        if lengths:
            stats['avg_length'] = sum(lengths) / len(lengths)
            stats['max_length'] = max(lengths)
            stats['min_length'] = min(lengths)
        
        return stats


if __name__ == "__main__":
    # Example usage
    from transformers import AutoTokenizer
    
    preprocessor = CodeBenchPreprocessor()
    tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
    
    sample = {
        'language': 'python',
        'description': 'Write a function to sum two numbers',
        'starter_code': 'def add(a, b): # TODO: implement',
    }
    
    processed = preprocessor.process_sample(sample, tokenizer)
    print("Processed sample:", processed)
