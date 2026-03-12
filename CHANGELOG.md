# Changelog

All notable changes to this project are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-03-12

### Added
- `src/models/evaluator.py`: `ModelEvaluator` (classification + regression metrics) and `MetricsComputer` (code similarity via SequenceMatcher) - previously missing, causing import failures
- `src/models/__init__.py`: models sub-package exporting both classes
- `train_demo.py`: lightweight TF-IDF + RandomForestClassifier demo - no GPU or model download required
- `models/bigcode_demo.pkl`: trained demo model bundle (tfidf + scaler + RF + metrics)
- `streamlit_app.py`: four-tab interactive dashboard (Code Quality Predictor, Model Dashboard, Code Explorer, LLM Pipeline)
- `.streamlit/config.toml`: dark-theme Streamlit configuration
- `runtime.txt` / `packages.txt` for Streamlit Cloud deployment

### Fixed
- `src/data/loader.py`: wrapped top-level `from datasets import ...` in `try/except ImportError` so the module loads in CI environments where `datasets` is not installed
- `flask_app.py` `before_request`: skips automatic model loading when `app.config['TESTING']` is True, allowing all Flask tests to run without downloading CodeBERT
- `flask_app.py` `/api/predict`: changed `request.get_json()` to `request.get_json(silent=True)` so requests with no Content-Type header return 400 instead of 500
- All 3 test files now collect and run successfully (previously 2 collection errors blocked the entire suite)

### Changed
- CI upgraded: `actions/checkout@v4`, `actions/setup-python@v5` (built-in pip cache), `codecov/codecov-action@v5`
- Python matrix updated from `3.9/3.10/3.11` to `3.10/3.11/3.12`
- Removed redundant `actions/cache@v3` step (replaced by `setup-python@v5` cache option)
- `requirements.txt` replaced with Streamlit Cloud runtime only (numpy, pandas, scikit-learn, streamlit, plotly)
- `requirements-ci.txt` unpinned and trimmed to only packages needed for the test + lint suite
- `.gitignore` created from scratch with `models/*.pkl` exclusion and `!models/bigcode_demo.pkl` exception