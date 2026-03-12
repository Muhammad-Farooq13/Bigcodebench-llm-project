# BigCodeBench LLM Project

[![CI](https://github.com/Muhammad-Farooq13/Bigcodebench-llm-project/actions/workflows/ci.yml/badge.svg)](https://github.com/Muhammad-Farooq13/Bigcodebench-llm-project/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://www.python.org)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/Muhammad-Farooq13/Bigcodebench-llm-project/main/streamlit_app.py)

An end-to-end pipeline for evaluating Large Language Models on **BigCodeBench** - a comprehensive Python coding benchmark. The project provides a modular architecture for data loading, tokenisation, model inference, evaluation, and REST API serving.

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/Muhammad-Farooq13/Bigcodebench-llm-project/main/streamlit_app.py)

Four interactive tabs:
- **Code Quality Predictor** - paste Python code and get an instant quality score
- **Model Dashboard** - accuracy, ROC-AUC, feature importances, class distribution
- **Code Explorer** - per-metric distributions, box plots, correlation heatmap
- **LLM Pipeline** - full architecture overview, API docs, supported model backends

## Dataset

| Property | Value |
|---|---|
| Source | bigcode/bigcodebench (HuggingFace Hub) |
| Task | Code quality classification (binary) |
| Primary model | microsoft/codebert-base |
| Demo model | TF-IDF + RandomForestClassifier (CPU, no download needed) |

## Project Structure

`
Bigcodebench-llm-project/
├── src/
│   ├── data/           # BigCodeBenchLoader, CodeBenchPreprocessor, TokenizerManager
│   ├── features/       # CodeFeatureExtractor, TextFeatureExtractor, FeatureEngineer
│   ├── models/         # ModelEvaluator, MetricsComputer
│   ├── utils/          # config, helpers, logger
│   └── visualization/  # DataVisualizer, MetricsVisualizer
├── tests/              # pytest suite - 18 tests, all passing
├── flask_app.py        # REST API (Flask + CodeBERT inference)
├── streamlit_app.py    # Interactive Streamlit dashboard
├── train_demo.py       # Lightweight demo model training script
├── models/
│   └── bigcode_demo.pkl
├── config/config.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt        # Streamlit Cloud runtime
├── requirements-ci.txt     # CI-safe dependencies
└── .github/workflows/ci.yml
`

## Quick Start

### 1. Clone and install (CI-safe, no GPU needed)

`ash
git clone https://github.com/Muhammad-Farooq13/Bigcodebench-llm-project.git
cd Bigcodebench-llm-project
pip install -r requirements-ci.txt
`

### 2. Train the demo model

`ash
python train_demo.py
`

### 3. Launch the Streamlit dashboard

`ash
streamlit run streamlit_app.py
`

### 4. Run the Flask API (requires transformers + model download)

`ash
export MODEL_NAME=microsoft/codebert-base
python flask_app.py
`

API endpoints:

| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check - device + model-loaded status |
| /api/predict | POST | Single code snippet classification |
| /api/predict_batch | POST | Batch inference |
| /api/tokenize | POST | Tokenize text, return token IDs |
| /api/info | GET | Model metadata and parameter count |

### 5. Run tests

`ash
pytest tests/ -v
`

### 6. Docker

`ash
docker-compose up --build
`

## Supported Model Backends

| Alias | HuggingFace ID |
|---|---|
| codebert | microsoft/codebert-base |
| graphcodebert | microsoft/graphcodebert-base |
| codet5 | Salesforce/codet5-base |
| codeberta | huggingface/CodeBERTa-small-v1 |
| gpt2 | gpt2 |

## CI/CD

GitHub Actions workflow (.github/workflows/ci.yml):

- Matrix: Python 3.10, 3.11, 3.12
- actions/checkout@v4 - actions/setup-python@v5 (pip cache)
- Lint (flake8) -> Test (pytest + coverage) -> Codecov upload
- Security scan with bandit + safety

## License

MIT