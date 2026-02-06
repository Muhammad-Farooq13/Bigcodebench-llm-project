"""
Visualization utilities for data exploration and model analysis
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)


class DataVisualizer:
    """Visualize dataset statistics and distributions"""
    
    @staticmethod
    def plot_class_distribution(labels: List[int], title: str = 'Class Distribution'):
        """Plot distribution of classes"""
        unique, counts = np.unique(labels, return_counts=True)
        
        plt.figure(figsize=(10, 6))
        plt.bar(unique, counts)
        plt.xlabel('Class')
        plt.ylabel('Count')
        plt.title(title)
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_sequence_lengths(lengths: List[int], title: str = 'Sequence Length Distribution'):
        """Plot distribution of sequence lengths"""
        plt.figure(figsize=(10, 6))
        plt.hist(lengths, bins=50, edgecolor='black')
        plt.xlabel('Sequence Length')
        plt.ylabel('Frequency')
        plt.title(title)
        plt.axvline(np.mean(lengths), color='r', linestyle='--', label=f'Mean: {np.mean(lengths):.0f}')
        plt.axvline(np.median(lengths), color='g', linestyle='--', label=f'Median: {np.median(lengths):.0f}')
        plt.legend()
        plt.tight_layout()
        return plt.gcf()


class MetricsVisualizer:
    """Visualize model metrics and performance"""
    
    @staticmethod
    def plot_confusion_matrix(cm: np.ndarray, labels: Optional[List[str]] = None):
        """Plot confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_metrics_comparison(metrics: Dict[str, float]):
        """Plot comparison of metrics"""
        plt.figure(figsize=(10, 6))
        names = list(metrics.keys())
        values = list(metrics.values())
        
        plt.bar(names, values)
        plt.ylabel('Score')
        plt.title('Model Metrics Comparison')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_training_history(history: Dict[str, List[float]]):
        """Plot training history"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        if 'loss' in history:
            axes[0].plot(history['loss'], label='Training Loss')
            if 'val_loss' in history:
                axes[0].plot(history['val_loss'], label='Validation Loss')
            axes[0].set_xlabel('Epoch')
            axes[0].set_ylabel('Loss')
            axes[0].set_title('Training Loss')
            axes[0].legend()
            axes[0].grid(True)
        
        if 'accuracy' in history:
            axes[1].plot(history['accuracy'], label='Training Accuracy')
            if 'val_accuracy' in history:
                axes[1].plot(history['val_accuracy'], label='Validation Accuracy')
            axes[1].set_xlabel('Epoch')
            axes[1].set_ylabel('Accuracy')
            axes[1].set_title('Training Accuracy')
            axes[1].legend()
            axes[1].grid(True)
        
        plt.tight_layout()
        return fig


class CodeVisualization:
    """Visualize code-related statistics"""
    
    @staticmethod
    def plot_language_distribution(languages: List[str]):
        """Plot distribution of programming languages"""
        from collections import Counter
        
        lang_counts = Counter(languages)
        
        plt.figure(figsize=(12, 6))
        langs = list(lang_counts.keys())
        counts = list(lang_counts.values())
        
        plt.bar(langs, counts)
        plt.xlabel('Programming Language')
        plt.ylabel('Count')
        plt.title('Dataset Language Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.gcf()
    
    @staticmethod
    def plot_code_length_by_language(code_lengths: Dict[str, List[int]]):
        """Plot code length distribution by language"""
        plt.figure(figsize=(12, 6))
        
        data = [lengths for lengths in code_lengths.values()]
        labels = list(code_lengths.keys())
        
        plt.boxplot(data, labels=labels)
        plt.ylabel('Code Length')
        plt.title('Code Length Distribution by Language')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.gcf()


def save_figure(fig, path: str):
    """Save figure to disk"""
    fig.savefig(path, dpi=300, bbox_inches='tight')
    logger.info(f"Figure saved to {path}")


if __name__ == '__main__':
    # Example usage
    viz = DataVisualizer()
    labels = np.random.randint(0, 3, 100)
    fig = viz.plot_class_distribution(labels)
    save_figure(fig, './test_distribution.png')
