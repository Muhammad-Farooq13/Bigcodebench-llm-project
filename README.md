# BigCodeBench LLM Project

A comprehensive Large Language Model (LLM) project built on the BigCodeBench dataset from Hugging Face. This project demonstrates best practices in machine learning operations (MLOps), model development, and deployment.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset Overview](#dataset-overview)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Model Development](#model-development)
- [Deployment](#deployment)
- [Testing](#testing)
- [MLOps & CI/CD](#mlops--cicd)
- [Contributing](#contributing)

## 🎯 Project Overview

This project aims to build and evaluate Large Language Models for code understanding and generation tasks using the BigCodeBench dataset. The dataset contains a collection of programming problems and solutions across multiple programming languages.

### Objectives
- Load and explore the BigCodeBench dataset
- Preprocess and tokenize code and natural language samples
- Fine-tune pre-trained language models (CodeBERT, GraphCodeBERT, CodeT5)
- Evaluate model performance on code-related tasks
- Deploy the model as a REST API using Flask
- Implement continuous integration and monitoring

### Tech Stack
- **Language Models**: Hugging Face Transformers (CodeBERT, GraphCodeBERT, CodeT5)
- **Framework**: PyTorch
- **Web Server**: Flask + Gunicorn
- **Containerization**: Docker
- **Experimentation**: MLflow
- **Monitoring**: Weights & Biases (W&B)
- **Testing**: Pytest

## 📊 Dataset Overview

### BigCodeBench Dataset

**Source**: [Hugging Face Datasets - bigcode/bigcodebench](https://huggingface.co/datasets/bigcode/bigcodebench)

**Description**: BigCodeBench is a comprehensive dataset for evaluating code understanding and generation capabilities of language models. It includes:

- **Code Samples**: Multiple programming languages (Python, Java, C++, JavaScript, etc.)
- **Problem Descriptions**: Natural language descriptions of programming tasks
- **Solutions**: Reference implementations and solutions
- **Metadata**: Language, difficulty level, tags, and more

### Features
- `problem_id`: Unique identifier for each problem
- `title`: Title of the programming problem
- `description`: Natural language description
- `language`: Programming language
- `starter_code`: Template/starter code
- `solutions`: List of valid solutions
- `test_cases`: Test cases to validate solutions
- `difficulty`: Problem difficulty level
- `tags`: Topic tags (e.g., arrays, strings, graphs)

### Data Preprocessing Steps
1. **Tokenization**: Convert code and text to token IDs using model-specific tokenizers
2. **Padding**: Standardize sequence lengths
3. **Filtering**: Remove duplicates and samples with invalid UTF-8 encoding
4. **Splitting**: Create train/validation/test splits (80/10/10)
5. **Caching**: Store processed data for faster loading

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda
- Git
- Docker (optional, for containerized deployment)
- CUDA/GPU (optional, recommended for faster training)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project.git
   cd bigcodebench-llm-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Hugging Face authentication**
   ```bash
   huggingface-cli login
   ```
   Or set the environment variable:
   ```bash
   export HUGGINGFACEHUB_API_TOKEN=your_token_here
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## 📁 Project Structure

```
bigcodebench-llm-project/
├── data/
│   ├── raw/                 # Raw dataset files
│   └── processed/           # Processed and tokenized data
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_evaluation.ipynb
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py        # Dataset loading utilities
│   │   ├── preprocessor.py  # Data preprocessing
│   │   └── tokenizer.py     # Text tokenization
│   ├── features/
│   │   ├── __init__.py
│   │   └── engineering.py   # Feature engineering
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py          # Base model classes
│   │   ├── trainer.py       # Model training loops
│   │   └── evaluator.py     # Evaluation metrics
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── plots.py         # Visualization utilities
│   └── utils/
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       ├── logger.py        # Logging setup
│       └── helpers.py       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_data.py         # Data module tests
│   ├── test_models.py       # Model tests
│   └── test_api.py          # API endpoint tests
├── config/
│   ├── config.yaml          # Main configuration
│   └── logging_config.yaml  # Logging configuration
├── .github/
│   └── workflows/
│       ├── ci.yml           # GitHub Actions CI
│       └── cd.yml           # Continuous deployment
├── flask_app.py             # Flask application entry point
├── mlops_pipeline.py        # MLOps pipeline orchestration
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Multi-container setup
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore patterns
├── setup.py                # Python package setup
└── requirements.txt        # Python dependencies
```

## 🏃 Quick Start

### 1. Load and Explore Data

```python
from src.data.loader import load_bigcodebench
import pandas as pd

# Load dataset
ds = load_bigcodebench()
print(f"Dataset splits: {ds.keys()}")
print(f"Training samples: {len(ds['train'])}")

# Explore first sample
sample = ds['train'][0]
print(f"Problem: {sample['title']}")
print(f"Language: {sample['language']}")
```

### 2. Preprocess and Tokenize

```python
from src.data.preprocessor import CodeBenchPreprocessor
from transformers import AutoTokenizer

# Initialize preprocessor
preprocessor = CodeBenchPreprocessor()
tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')

# Process dataset
processed_ds = ds.map(
    lambda x: preprocessor.process(x, tokenizer),
    batched=True,
    batch_size=32
)
```

### 3. Train Model

```python
from src.models.trainer import ModelTrainer
from transformers import AutoModelForSequenceClassification

# Load pre-trained model
model = AutoModelForSequenceClassification.from_pretrained('microsoft/codebert-base')

# Create trainer
trainer = ModelTrainer(model, tokenizer, config)

# Train
trainer.train(processed_ds['train'], processed_ds['validation'])
```

### 4. Evaluate Performance

```python
from src.models.evaluator import ModelEvaluator

# Evaluate
evaluator = ModelEvaluator(model, tokenizer)
metrics = evaluator.evaluate(processed_ds['test'])
print(f"Accuracy: {metrics['accuracy']:.4f}")
print(f"F1 Score: {metrics['f1']:.4f}")
```

### 5. Run Flask API

```bash
python flask_app.py
```

Access the API at `http://localhost:5000`

## 🧠 Model Development

### Supported Models

- **CodeBERT**: Microsoft CodeBERT for code and natural language understanding
- **GraphCodeBERT**: Enhanced version with code structure information
- **CodeT5**: Unified text-to-code and code-to-text model

### Hyperparameter Tuning

Configuration file: `config/config.yaml`

```yaml
training:
  learning_rate: 2e-5
  batch_size: 32
  num_epochs: 3
  warmup_steps: 500
  weight_decay: 0.01
  
model:
  name: "microsoft/codebert-base"
  hidden_dropout_prob: 0.1
  attention_probs_dropout_prob: 0.1
```

Run hyperparameter tuning:
```bash
python -m src.models.trainer --tune
```

### Model Comparison

Compare multiple models on the same dataset:
```bash
python -m src.models.evaluator --compare-models
```

## 🐳 Deployment

### Local Flask Deployment

1. **Run development server**
   ```bash
   python flask_app.py
   ```

2. **API Endpoints**
   
   **Predict (POST)**
   ```bash
   curl -X POST http://localhost:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"code": "def hello(): return 42"}'
   ```

   **Health Check (GET)**
   ```bash
   curl http://localhost:5000/health
   ```

### Docker Deployment

1. **Build Docker image**
   ```bash
   docker build -t bigcodebench-llm:latest .
   ```

2. **Run container**
   ```bash
   docker run -p 5000:5000 \
     -e HUGGINGFACEHUB_API_TOKEN=your_token \
     bigcodebench-llm:latest
   ```

3. **Docker Compose (with Redis cache)**
   ```bash
   docker-compose up -d
   ```

### Production Deployment

Use Gunicorn with multiple workers:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

Or with Nginx reverse proxy (see docker-compose.yml)

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Suite

```bash
pytest tests/test_data.py -v
pytest tests/test_models.py -v
pytest tests/test_api.py -v
```

### Test Coverage

```bash
pytest --cov=src --cov-report=html
```

## 🚄 MLOps & CI/CD

### MLflow Experiment Tracking

```python
import mlflow

mlflow.set_experiment("bigcodebench-training")

with mlflow.start_run():
    mlflow.log_param("model", "codebert-base")
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_artifact("model.pt")
```

View experiments:
```bash
mlflow ui
```

### Weights & Biases Integration

```python
import wandb

wandb.init(project="bigcodebench-llm")
wandb.log({"accuracy": accuracy, "loss": loss})
```

### GitHub Actions CI/CD

See `.github/workflows/` for automated testing and deployment pipelines:

- `ci.yml`: Runs tests and linting on every push
- `cd.yml`: Builds and pushes Docker image on release

## 📈 Model Monitoring

Monitor model performance in production:

```bash
python -m src.utils.monitor
```

Tracks:
- Prediction latency
- Error rates
- Data drift
- Model performance degradation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Quality

- Format code: `black src/`
- Sort imports: `isort src/`
- Lint: `flake8 src/`
- Type checking: `mypy src/`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for the Datasets library and BigCodeBench
- Microsoft for CodeBERT and related models
- OpenAI for transformer architecture foundations

## 📧 Contact

For questions or suggestions, please open an issue or contact the maintainers.

---

**Last Updated**: February 2026
**Version**: 1.0.0
