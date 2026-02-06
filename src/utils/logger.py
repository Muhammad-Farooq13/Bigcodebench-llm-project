"""Logging utilities"""

import logging
import logging.config
import os
from pathlib import Path
import json
from datetime import datetime

# Default logging configuration
DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(funcName)s(): %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(timestamp)s %(level)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': './logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': './logs/error.log',
            'maxBytes': 10485760,
            'backupCount': 5
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO'
        },
        'src': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'transformers': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}


def setup_logging(
    config_file: str = './config/logging_config.yaml',
    log_dir: str = './logs',
    log_level: str = 'INFO'
) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        config_file: Path to logging config file
        log_dir: Directory for log files
        log_level: Default logging level
        
    Returns:
        Root logger instance
    """
    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Update default config with log directory
    DEFAULT_LOGGING_CONFIG['handlers']['file']['filename'] = os.path.join(log_dir, 'app.log')
    DEFAULT_LOGGING_CONFIG['handlers']['error_file']['filename'] = os.path.join(log_dir, 'error.log')
    
    # Set log level from environment or parameter
    env_level = os.getenv('LOG_LEVEL', log_level).upper()
    DEFAULT_LOGGING_CONFIG['handlers']['console']['level'] = env_level
    DEFAULT_LOGGING_CONFIG['loggers']['']['level'] = env_level
    
    # Load config file if exists, otherwise use defaults
    if os.path.exists(config_file):
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            logging.config.dictConfig(config)
        except Exception as e:
            print(f"Error loading logging config from {config_file}: {e}")
            print("Using default logging configuration")
            logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    else:
        logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    
    root_logger = logging.getLogger()
    root_logger.info(f"Logging initialized (level={env_level})")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerContextManager:
    """Context manager for temporary logging changes"""
    
    def __init__(self, logger_name: str, level: int = logging.DEBUG):
        """
        Initialize context manager.
        
        Args:
            logger_name: Name of logger to modify
            level: Temporary log level
        """
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level
        self.level = level
    
    def __enter__(self):
        """Enter context and change log level"""
        self.logger.setLevel(self.level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original log level"""
        self.logger.setLevel(self.original_level)


if __name__ == '__main__':
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Logging system initialized")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
