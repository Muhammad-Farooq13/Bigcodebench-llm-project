"""Utility helper functions"""

import os
import pickle
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import hashlib
import time
from functools import wraps


def ensure_dir(path: str) -> Path:
    """
    Ensure directory exists and create if needed.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def save_json(data: Any, path: str, pretty: bool = True):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        path: Output file path
        pretty: Whether to pretty-print
    """
    ensure_dir(Path(path).parent)
    
    with open(path, 'w') as f:
        if pretty:
            json.dump(data, f, indent=2, default=str)
        else:
            json.dump(data, f, default=str)


def load_json(path: str) -> Any:
    """
    Load data from JSON file.
    
    Args:
        path: Input file path
        
    Returns:
        Loaded data
    """
    with open(path, 'r') as f:
        return json.load(f)


def save_pickle(data: Any, path: str):
    """
    Save data to pickle file.
    
    Args:
        data: Data to save
        path: Output file path
    """
    ensure_dir(Path(path).parent)
    
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(path: str) -> Any:
    """
    Load data from pickle file.
    
    Args:
        path: Input file path
        
    Returns:
        Loaded data
    """
    with open(path, 'rb') as f:
        return pickle.load(f)


def compute_file_hash(path: str, algorithm: str = 'md5') -> str:
    """
    Compute hash of a file.
    
    Args:
        path: File path
        algorithm: Hash algorithm ('md5', 'sha256', etc.)
        
    Returns:
        Hash string
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def timer(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds")
        return result
    return wrapper


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nested items
        sep: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)


def batch_iterator(iterable: List, batch_size: int):
    """
    Create batches from an iterable.
    
    Args:
        iterable: List to batch
        batch_size: Size of each batch
        
    Yields:
        Batch items
    """
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]


def get_system_info() -> Dict[str, Any]:
    """
    Get system information.
    
    Returns:
        Dictionary with system info
    """
    import platform
    import psutil
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),
        'total_memory_gb': psutil.virtual_memory().total / (1024**3),
        'available_memory_gb': psutil.virtual_memory().available / (1024**3),
    }


class CachedProperty:
    """Decorator for cached properties"""
    
    def __init__(self, func):
        self.func = func
        self.value = None
        self.cached = False
    
    def __get__(self, obj, objtype=None):
        if not self.cached:
            self.value = self.func(obj)
            self.cached = True
        return self.value


if __name__ == '__main__':
    # Test utilities
    print("Testing utilities...")
    
    # Test directory creation
    test_dir = ensure_dir('./test_data')
    print(f"Created directory: {test_dir}")
    
    # Test JSON save/load
    test_data = {'key': 'value', 'number': 42}
    save_json(test_data, './test_data/test.json')
    loaded_data = load_json('./test_data/test.json')
    print(f"Saved and loaded JSON: {loaded_data}")
    
    # Clean up
    import shutil
    shutil.rmtree('./test_data')
    print("Cleaned up test files")
