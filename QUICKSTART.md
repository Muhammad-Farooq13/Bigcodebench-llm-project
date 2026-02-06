# BigCodeBench LLM Project - Quick Start Guide

## 🚀 Getting Started

### 1. **Clone & Setup**
```bash
cd bigcodebench_llm_project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings (model name, tokens, etc.)
```

### 3. **Run Flask API Locally**
```bash
python flask_app.py
# API available at http://localhost:5000
```

### 4. **Test the API**
```bash
# Health check
curl http://localhost:5000/health

# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): return 42"}'
```

### 5. **Run Tests**
```bash
pytest tests/ -v --cov=src
```

### 6. **Train Model with MLOps**
```bash
python mlops_pipeline.py --experiment bigcodebench-training
```

### 7. **Docker Deployment**
```bash
# Build image
docker build -t bigcodebench-llm:latest .

# Run with Docker Compose (includes Redis, MLflow)
docker-compose up -d

# Stop services
docker-compose down
```

## 📁 Project Structure Overview

```
bigcodebench_llm_project/
├── data/                          # Data storage
│   ├── raw/                       # Raw dataset files
│   └── processed/                 # Processed/tokenized data
├── notebooks/                     # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_evaluation.ipynb
├── src/                           # Source code
│   ├── data/                      # Data loading & preprocessing
│   │   ├── loader.py              # Load BigCodeBench dataset
│   │   ├── preprocessor.py        # Clean and preprocess data
│   │   ├── tokenizer.py           # Code-aware tokenization
│   │   └── __init__.py
│   ├── features/                  # Feature engineering
│   │   ├── engineering.py         # Extract code/text features
│   │   └── __init__.py
│   ├── models/                    # Model training & evaluation
│   │   ├── trainer.py             # Training loops
│   │   ├── evaluator.py           # Evaluation metrics
│   │   └── __init__.py
│   ├── visualization/             # Data visualization
│   │   ├── plots.py               # Plotting utilities
│   │   └── __init__.py
│   ├── utils/                     # Utilities
│   │   ├── config.py              # Configuration management
│   │   ├── logger.py              # Logging setup
│   │   ├── helpers.py             # Helper functions
│   │   └── __init__.py
│   └── __init__.py
├── tests/                         # Test suite
│   ├── test_data.py               # Data tests
│   ├── test_models.py             # Model tests
│   ├── test_api.py                # API tests
│   └── __init__.py
├── config/                        # Configuration files
│   ├── config.yaml                # Main configuration
│   └── logging_config.yaml        # Logging configuration
├── .github/
│   └── workflows/                 # GitHub Actions CI/CD
│       ├── ci.yml                 # Testing & linting
│       └── cd.yml                 # Build & deploy
├── flask_app.py                   # Flask application entry point
├── mlops_pipeline.py              # MLOps pipeline orchestration
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Multi-container setup
├── nginx.conf                     # Nginx reverse proxy config
├── setup.py                       # Python package setup
├── requirements.txt               # Python dependencies
├── README.md                      # Comprehensive documentation
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore patterns
└── LICENSE                        # Project license
```

## 🎯 Key Features

### Data Module (`src/data/`)
- **loader.py**: Load BigCodeBench dataset from Hugging Face
- **preprocessor.py**: Clean code/text, remove comments, validate data
- **tokenizer.py**: Code-aware tokenization with language markers

### Models Module (`src/models/`)
- **trainer.py**: Fine-tune transformer models (CodeBERT, GraphCodeBERT, CodeT5)
- **evaluator.py**: Comprehensive evaluation metrics (accuracy, F1, ROUGE, BLEU)

### Features Module (`src/features/`)
- Extract code metrics (lines, functions, imports, indentation)
- Extract text metrics (word count, unique words, diversity)
- Combine code and text features for training

### Flask API (`flask_app.py`)
- `/health` - Health check endpoint
- `/api/predict` - Single prediction
- `/api/batch-predict` - Batch predictions
- `/api/tokenize` - Text tokenization
- `/api/info` - Model information

### MLOps Pipeline (`mlops_pipeline.py`)
- End-to-end training pipeline
- MLflow experiment tracking
- Automatic hyperparameter logging
- Model versioning and artifact management

### Docker & Deployment
- Multi-stage Dockerfile for optimized images
- Docker Compose with Redis, MLflow, and Nginx
- GitHub Actions CI/CD workflows
- Health checks and monitoring

## 📊 Supported Models

- **CodeBERT** (microsoft/codebert-base)
- **GraphCodeBERT** (microsoft/graphcodebert-base)
- **CodeT5** (Salesforce/codet5-base)
- **CodeBERTa** (huggingface/CodeBERTa-small-v1)
- **GPT-2**, **GPT-Neo** for generation tasks

## 🔧 Configuration

Edit `config/config.yaml` to customize:
- Learning rate, batch size, epochs
- Model architecture parameters
- Data preprocessing settings
- MLflow and monitoring configs

## 📈 Monitoring & Logging

- **MLflow**: Track experiments at `http://localhost:5001`
- **Weights & Biases**: Monitor training in real-time
- **Logs**: Check `./logs/` for application logs
- **Health checks**: Docker containers auto-restart on failure

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Coverage report
pytest --cov=src --cov-report=html
```

## 🚢 Production Deployment

1. Set up environment variables in `.env`
2. Build Docker image: `docker build -t bigcodebench-llm:latest .`
3. Run with Docker Compose: `docker-compose up -d`
4. Access API through Nginx reverse proxy on port 80

## 📚 Additional Resources

- [BigCodeBench Dataset](https://huggingface.co/datasets/bigcode/bigcodebench)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MLflow Documentation](https://mlflow.org/docs/)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

**Project Ready for GitHub!** 🎉

This project is structured following MLOps best practices and is ready for production deployment. All code is documented, tested, and includes comprehensive configuration files.
