"""
Tokenization utilities for code and natural language
"""

import logging
from typing import Dict, List, Optional, Union
from transformers import AutoTokenizer, PreTrainedTokenizer

logger = logging.getLogger(__name__)

# Popular code-aware tokenizers
CODE_TOKENIZERS = {
    'codebert': 'microsoft/codebert-base',
    'graphcodebert': 'microsoft/graphcodebert-base',
    'codet5': 'Salesforce/codet5-base',
    'codeberta': 'huggingface/CodeBERTa-small-v1',
    'gpt2': 'gpt2',
    'gptneo': 'EleutherAI/gpt-neo-125m',
}


class TokenizerManager:
    """Manage tokenizers for code and text encoding."""
    
    def __init__(self, model_name: str = 'microsoft/codebert-base'):
        """
        Initialize tokenizer.
        
        Args:
            model_name: Model identifier or alias
        """
        # Resolve alias if provided
        if model_name in CODE_TOKENIZERS:
            model_name = CODE_TOKENIZERS[model_name]
        
        self.model_name = model_name
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info(f"Loaded tokenizer: {model_name}")
            logger.info(f"Vocab size: {len(self.tokenizer)}")
        except Exception as e:
            logger.error(f"Error loading tokenizer: {str(e)}")
            raise
    
    def encode(
        self,
        text: Union[str, List[str]],
        max_length: int = 512,
        padding: str = 'max_length',
        truncation: bool = True,
        return_tensors: Optional[str] = None,
        **kwargs
    ) -> Union[Dict, List[int]]:
        """
        Encode text to token IDs.
        
        Args:
            text: Text or list of texts to encode
            max_length: Maximum sequence length
            padding: Padding strategy
            truncation: Whether to truncate
            return_tensors: Return as 'pt', 'tf', etc. or None for lists
            **kwargs: Additional tokenizer arguments
            
        Returns:
            Encoded tokens or tokenized output
        """
        return self.tokenizer(
            text,
            max_length=max_length,
            padding=padding,
            truncation=truncation,
            return_tensors=return_tensors,
            **kwargs
        )
    
    def decode(
        self,
        token_ids: Union[List[int], 'torch.Tensor'],
        skip_special_tokens: bool = True,
        **kwargs
    ) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            token_ids: Token IDs to decode
            skip_special_tokens: Whether to skip special tokens
            **kwargs: Additional tokenizer arguments
            
        Returns:
            Decoded text
        """
        return self.tokenizer.decode(
            token_ids,
            skip_special_tokens=skip_special_tokens,
            **kwargs
        )
    
    def get_vocab_info(self) -> Dict[str, int]:
        """Get vocabulary information."""
        return {
            'vocab_size': len(self.tokenizer),
            'model_name': self.model_name,
            'bos_token_id': self.tokenizer.bos_token_id,
            'eos_token_id': self.tokenizer.eos_token_id,
            'pad_token_id': self.tokenizer.pad_token_id,
        }


class CodeTokenizer(TokenizerManager):
    """Specialized tokenizer for code with language-aware features."""
    
    def __init__(self, model_name: str = 'microsoft/codebert-base'):
        """
        Initialize code tokenizer.
        
        Args:
            model_name: Code model identifier
        """
        super().__init__(model_name)
    
    def encode_code_with_language(
        self,
        code: str,
        language: str,
        max_length: int = 512,
        **kwargs
    ) -> Dict:
        """
        Encode code with language information.
        
        Args:
            code: Code string
            language: Programming language
            max_length: Maximum length
            **kwargs: Additional arguments
            
        Returns:
            Encoded tokens with metadata
        """
        # Add language marker
        language_marker = f"[LANG:{language.upper()}]"
        combined = f"{language_marker} {code}"
        
        encoded = self.encode(
            combined,
            max_length=max_length,
            **kwargs
        )
        
        encoded['language'] = language
        return encoded
    
    def encode_code_and_text(
        self,
        code: str,
        text: str,
        max_length: int = 512,
        code_ratio: float = 0.6,
        **kwargs
    ) -> Dict:
        """
        Encode code and natural language description together.
        
        Args:
            code: Code string
            text: Natural language text
            max_length: Maximum length
            code_ratio: Proportion of max_length for code
            **kwargs: Additional arguments
            
        Returns:
            Encoded tokens
        """
        code_max = int(max_length * code_ratio)
        text_max = max_length - code_max
        
        # Tokenize separately with different max lengths
        code_tokens = self.encode(
            code,
            max_length=code_max,
            truncation=True,
            return_tensors=None
        )
        
        text_tokens = self.encode(
            text,
            max_length=text_max,
            truncation=True,
            return_tensors=None
        )
        
        # Combine tokens
        combined_ids = (
            code_tokens['input_ids'] + 
            text_tokens['input_ids'][1:]  # Skip CLS token from text
        )
        
        # Pad to max_length
        if len(combined_ids) < max_length:
            pad_length = max_length - len(combined_ids)
            combined_ids = combined_ids + [self.tokenizer.pad_token_id] * pad_length
        else:
            combined_ids = combined_ids[:max_length]
        
        return {
            'input_ids': combined_ids,
            'token_type_ids': code_tokens.get('token_type_ids', []),
        }


def get_tokenizer(
    model_name: str = 'microsoft/codebert-base',
    code_aware: bool = True
) -> Union[CodeTokenizer, TokenizerManager]:
    """
    Get a tokenizer instance.
    
    Args:
        model_name: Model name or alias
        code_aware: Whether to use code-aware tokenizer
        
    Returns:
        Tokenizer instance
    """
    if code_aware:
        return CodeTokenizer(model_name)
    else:
        return TokenizerManager(model_name)


if __name__ == "__main__":
    # Example usage
    tokenizer = get_tokenizer('codebert')
    
    code = "def hello():\n    return 'world'"
    text = "A function that returns hello world"
    
    # Encode code with language
    encoded = tokenizer.encode_code_with_language(code, 'python')
    print("Encoded code:", encoded)
    
    # Encode code and text together
    combined = tokenizer.encode_code_and_text(code, text)
    print("Combined encoding:", combined)
