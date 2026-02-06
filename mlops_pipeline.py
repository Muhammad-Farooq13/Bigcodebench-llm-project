"""
MLOps pipeline orchestration for BigCodeBench LLM Project
"""

import logging
import os
from datetime import datetime
from typing import Dict, Optional
import mlflow
import mlflow.pytorch
from pathlib import Path

from src.utils import get_config_manager, setup_logging
from src.data import load_bigcodebench, CodeBenchPreprocessor
from src.models import ModelTrainer

logger = logging.getLogger(__name__)


class MLOpsPipeline:
    """End-to-end ML pipeline with experiment tracking"""
    
    def __init__(self, experiment_name: str = 'bigcodebench-training'):
        """
        Initialize MLOps pipeline.
        
        Args:
            experiment_name: MLflow experiment name
        """
        # Setup logging
        setup_logging()
        
        # Setup MLflow
        config_manager = get_config_manager()
        mlflow_config = config_manager.to_dict().get('mlflow', {})
        
        tracking_uri = mlflow_config.get('tracking_uri', 'http://localhost:5000')
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        
        self.config_manager = config_manager
        self.experiment_name = experiment_name
        
        logger.info(f"MLOps Pipeline initialized with experiment: {experiment_name}")
    
    def load_data(self) -> Dict:
        """Load and preprocess dataset"""
        logger.info("Loading dataset...")
        
        data_config = self.config_manager.get_data_config()
        
        # Load dataset
        ds = load_bigcodebench()
        logger.info(f"Loaded dataset with splits: {list(ds.keys())}")
        
        return ds
    
    def preprocess_data(self, dataset, split: str = 'train', max_samples: Optional[int] = None):
        """Preprocess dataset"""
        logger.info(f"Preprocessing {split} split...")
        
        preprocessor = CodeBenchPreprocessor()
        split_data = dataset[split]
        
        if max_samples:
            split_data = split_data.select(range(min(max_samples, len(split_data))))
        
        logger.info(f"Preprocessed {len(split_data)} samples")
        
        return split_data
    
    def train_model(
        self,
        train_dataset,
        eval_dataset,
        output_dir: str = './models/checkpoint'
    ):
        """Train model with MLflow tracking"""
        logger.info("Starting model training...")
        
        training_config = self.config_manager.get_training_config()
        model_config = self.config_manager.get_model_config()
        
        with mlflow.start_run(run_name=f"training-{datetime.now().isoformat()}"):
            # Log parameters
            mlflow.log_params(training_config.__dict__)
            mlflow.log_params(model_config.__dict__)
            
            # Create trainer
            trainer = ModelTrainer(
                model_name=model_config.name,
                task=model_config.task,
                num_labels=model_config.num_labels
            )
            
            # Train
            results = trainer.train(
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
                output_dir=output_dir,
                num_epochs=training_config.num_epochs,
                learning_rate=training_config.learning_rate,
                batch_size=training_config.batch_size,
                weight_decay=training_config.weight_decay,
            )
            
            # Log metrics
            for key, value in results.items():
                if isinstance(value, (int, float)):
                    mlflow.log_metric(key, value)
            
            # Log model
            mlflow.pytorch.log_model(trainer.model, "model")
            
            logger.info("Training completed and logged to MLflow")
            
            return trainer, results
    
    def run_full_pipeline(
        self,
        train_samples: Optional[int] = None,
        eval_samples: Optional[int] = None,
    ):
        """Run full MLOps pipeline"""
        logger.info("="*50)
        logger.info("Starting BigCodeBench MLOps Pipeline")
        logger.info("="*50)
        
        # Load data
        dataset = self.load_data()
        
        # Preprocess train split
        train_data = self.preprocess_data(dataset, 'train', max_samples=train_samples)
        
        # Preprocess validation split (if available)
        eval_split = 'validation' if 'validation' in dataset else 'test'
        eval_data = self.preprocess_data(dataset, eval_split, max_samples=eval_samples)
        
        # Train model
        trainer, results = self.train_model(train_data, eval_data)
        
        # Save model
        output_dir = './models/final_model'
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        trainer.save_model(output_dir)
        
        logger.info("="*50)
        logger.info("Pipeline completed successfully!")
        logger.info("="*50)
        
        return trainer, results


def main():
    """Main entry point for MLOps pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description='BigCodeBench MLOps Pipeline')
    parser.add_argument('--experiment', type=str, default='bigcodebench-training',
                       help='MLflow experiment name')
    parser.add_argument('--train-samples', type=int, default=None,
                       help='Number of training samples (for testing)')
    parser.add_argument('--eval-samples', type=int, default=None,
                       help='Number of evaluation samples (for testing)')
    
    args = parser.parse_args()
    
    # Run pipeline
    pipeline = MLOpsPipeline(experiment_name=args.experiment)
    pipeline.run_full_pipeline(
        train_samples=args.train_samples,
        eval_samples=args.eval_samples
    )


if __name__ == '__main__':
    main()
