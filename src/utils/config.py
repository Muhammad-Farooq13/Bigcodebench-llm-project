"""Configuration management utilities"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    """Training configuration"""
    learning_rate: float = 2e-5
    batch_size: int = 32
    eval_batch_size: int = 64
    num_epochs: int = 3
    warmup_steps: int = 500
    weight_decay: float = 0.01
    max_length: int = 512
    gradient_accumulation_steps: int = 1


@dataclass
class ModelConfig:
    """Model configuration"""
    name: str = 'microsoft/codebert-base'
    task: str = 'classification'
    num_labels: int = 2
    hidden_dropout_prob: float = 0.1
    attention_probs_dropout_prob: float = 0.1


@dataclass
class DataConfig:
    """Data configuration"""
    raw_data_dir: str = './data/raw'
    processed_data_dir: str = './data/processed'
    dataset_name: str = 'bigcode/bigcodebench'
    splits: list = None
    
    def __post_init__(self):
        if self.splits is None:
            self.splits = ['train', 'validation', 'test']


class ConfigManager:
    """Manage project configuration from files and environment variables"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to config YAML file
        """
        self.config_path = config_path or './config/config.yaml'
        self.training_config = TrainingConfig()
        self.model_config = ModelConfig()
        self.data_config = DataConfig()
        
        # Load from files and environment
        load_dotenv()
        self._load_from_file()
        self._load_from_env()
    
    def _load_from_file(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}")
            return
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
            
            # Update training config
            if 'training' in config:
                for key, value in config['training'].items():
                    if hasattr(self.training_config, key):
                        setattr(self.training_config, key, value)
            
            # Update model config
            if 'model' in config:
                for key, value in config['model'].items():
                    if hasattr(self.model_config, key):
                        setattr(self.model_config, key, value)
            
            # Update data config
            if 'data' in config:
                for key, value in config['data'].items():
                    if hasattr(self.data_config, key):
                        setattr(self.data_config, key, value)
            
            logger.info(f"Loaded config from {self.config_path}")
            
        except Exception as e:
            logger.error(f"Error loading config file: {str(e)}")
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Model configuration
        if model_name := os.getenv('MODEL_NAME'):
            self.model_config.name = model_name
        if task := os.getenv('TASK'):
            self.model_config.task = task
        
        # Training configuration
        if lr := os.getenv('LEARNING_RATE'):
            self.training_config.learning_rate = float(lr)
        if batch_size := os.getenv('BATCH_SIZE'):
            self.training_config.batch_size = int(batch_size)
        if epochs := os.getenv('NUM_EPOCHS'):
            self.training_config.num_epochs = int(epochs)
        
        # Data configuration
        if data_dir := os.getenv('DATA_DIR'):
            self.data_config.raw_data_dir = os.path.join(data_dir, 'raw')
            self.data_config.processed_data_dir = os.path.join(data_dir, 'processed')
    
    def get_training_config(self) -> TrainingConfig:
        """Get training configuration"""
        return self.training_config
    
    def get_model_config(self) -> ModelConfig:
        """Get model configuration"""
        return self.model_config
    
    def get_data_config(self) -> DataConfig:
        """Get data configuration"""
        return self.data_config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert all configurations to dictionary"""
        return {
            'training': asdict(self.training_config),
            'model': asdict(self.model_config),
            'data': asdict(self.data_config),
        }
    
    def save_config(self, path: str):
        """Save current configuration to file"""
        config_dict = self.to_dict()
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False)
        
        logger.info(f"Config saved to {path}")


# Singleton instance
_config_manager = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """Get or create configuration manager singleton"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager


if __name__ == '__main__':
    config_manager = get_config_manager()
    print("Training Config:", asdict(config_manager.get_training_config()))
    print("Model Config:", asdict(config_manager.get_model_config()))
    print("Data Config:", asdict(config_manager.get_data_config()))
