"""
Model evaluation utilities for BigCodeBench LLM project.
Uses scikit-learn for classification/regression metrics and
difflib for code similarity — no GPU packages required.
"""

import logging
from difflib import SequenceMatcher
from typing import Any, Dict

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate model predictions against ground truth."""

    def __init__(self, model: Any, tokenizer: Any):
        self.model = model
        self.tokenizer = tokenizer

    def evaluate_classification(
        self, predictions: np.ndarray, references: np.ndarray
    ) -> Dict[str, Any]:
        """Compute classification metrics."""
        return {
            "accuracy": float(accuracy_score(references, predictions)),
            "precision": float(
                precision_score(
                    references, predictions, average="weighted", zero_division=0
                )
            ),
            "recall": float(
                recall_score(
                    references, predictions, average="weighted", zero_division=0
                )
            ),
            "f1": float(
                f1_score(
                    references, predictions, average="weighted", zero_division=0
                )
            ),
            "confusion_matrix": confusion_matrix(references, predictions).tolist(),
        }

    def evaluate_regression(
        self, predictions: np.ndarray, references: np.ndarray
    ) -> Dict[str, float]:
        """Compute regression metrics."""
        mse = float(mean_squared_error(references, predictions))
        return {
            "mse": mse,
            "rmse": float(mse ** 0.5),
            "mae": float(mean_absolute_error(references, predictions)),
            "r2": float(r2_score(references, predictions)),
        }


class MetricsComputer:
    """Compute similarity and quality metrics for code."""

    @staticmethod
    def compute_code_similarity(code1: str, code2: str) -> float:
        """Return a normalized similarity ratio in [0, 1]."""
        return SequenceMatcher(None, code1, code2).ratio()
