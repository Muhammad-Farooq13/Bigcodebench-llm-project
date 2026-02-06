"""
Data loading utilities for BigCodeBench dataset
"""

import logging
from typing import Dict, Optional, Union
from datasets import load_dataset, DatasetDict, Dataset
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class BigCodeBenchLoader:
    """Load and manage BigCodeBench dataset from Hugging Face."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the dataset loader.
        
        Args:
            cache_dir: Directory to cache the dataset locally
        """
        self.cache_dir = cache_dir or "./data/raw"
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
    def load_dataset(
        self,
        name: str = "bigcode/bigcodebench",
        split: Optional[str] = None,
        use_auth_token: bool = True,
        **kwargs
    ) -> Union[DatasetDict, Dataset]:
        """
        Load BigCodeBench dataset from Hugging Face.
        
        Args:
            name: Dataset identifier
            split: Specific split to load (e.g., 'train', 'validation', 'test')
            use_auth_token: Whether to use Hugging Face authentication
            **kwargs: Additional arguments for load_dataset
            
        Returns:
            Dataset or DatasetDict
        """
        try:
            logger.info(f"Loading dataset: {name}")
            
            dataset = load_dataset(
                name,
                split=split,
                cache_dir=self.cache_dir,
                use_auth_token=use_auth_token,
                **kwargs
            )
            
            logger.info(f"Dataset loaded successfully. Shape: {len(dataset)} samples")
            return dataset
            
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
    
    def load_from_disk(self, path: str) -> DatasetDict:
        """
        Load dataset from local disk.
        
        Args:
            path: Path to cached dataset
            
        Returns:
            DatasetDict
        """
        from datasets import load_from_disk
        logger.info(f"Loading dataset from disk: {path}")
        return load_from_disk(path)
    
    def get_dataset_info(self, dataset: Union[DatasetDict, Dataset]) -> Dict:
        """
        Get information about the dataset.
        
        Args:
            dataset: Dataset to analyze
            
        Returns:
            Dictionary with dataset information
        """
        info = {}
        
        if isinstance(dataset, DatasetDict):
            info['splits'] = list(dataset.keys())
            info['split_sizes'] = {k: len(v) for k, v in dataset.items()}
            info['total_samples'] = sum(len(v) for v in dataset.values())
            info['features'] = dataset['train'].features if 'train' in dataset else {}
        else:
            info['total_samples'] = len(dataset)
            info['features'] = dataset.features
            
        return info


def load_bigcodebench(
    cache_dir: Optional[str] = None,
    split: Optional[str] = None
) -> Union[DatasetDict, Dataset]:
    """
    Convenience function to load BigCodeBench dataset.
    
    Args:
        cache_dir: Directory to cache dataset
        split: Specific split to load
        
    Returns:
        Dataset or DatasetDict
    """
    loader = BigCodeBenchLoader(cache_dir=cache_dir)
    return loader.load_dataset(split=split)


if __name__ == "__main__":
    # Example usage
    loader = BigCodeBenchLoader()
    ds = loader.load_dataset()
    info = loader.get_dataset_info(ds)
    print("Dataset Info:", info)
