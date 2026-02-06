# Installation Instructions

The import errors you're seeing are expected if dependencies haven't been installed yet.

## ✅ Solution: Install Dependencies

Run these commands to fix all errors:

### Option 1: Using pip (Recommended)
```bash
cd e:\LLM\bigcodebench_llm_project
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Using conda
```bash
conda create -n bigcodebench python=3.10
conda activate bigcodebench
cd e:\LLM\bigcodebench_llm_project
pip install -r requirements.txt
```

## 📋 What Gets Installed

The `requirements.txt` includes:
- **Core**: numpy, pandas, scikit-learn, scipy
- **Deep Learning**: torch, transformers, datasets, tokenizers
- **API**: flask, flask-cors, gunicorn, python-dotenv
- **MLOps**: mlflow, pydantic
- **ML**: evaluate, rouge-score, bert-score
- **Visualization**: matplotlib, seaborn, plotly
- **Testing**: pytest, pytest-cov, black, flake8, isort
- **Monitoring**: wandb, python-json-logger

## 🔧 Verify Installation

After installation, verify everything works:

```bash
# Test imports
python -c "import torch; import transformers; import flask; print('All imports OK!')"

# Test Flask API
python flask_app.py

# Run tests
pytest tests/ -v

# Run Jupyter notebooks
jupyter notebook notebooks/01_data_exploration.ipynb
```

## ⚙️ About the Import Warnings

The "Import could not be resolved" messages in VS Code are **safe to ignore** - they're just Pylance warnings that the packages aren't installed in your current Python environment. Once you run `pip install -r requirements.txt`, all warnings will disappear.

## 📚 Notebooks Status

✅ **All 4 notebooks have been created:**
- `01_data_exploration.ipynb` - Load and explore dataset
- `02_preprocessing.ipynb` - Data preprocessing and tokenization
- `03_model_training.ipynb` - Model training
- `04_evaluation.ipynb` - Model evaluation and metrics

Each notebook is ready to run once dependencies are installed.

## 🐛 Pickle File Handling

The `src/utils/helpers.py` file has full support for pickle files:
- `save_pickle(data, path)` - Save to pickle file
- `load_pickle(path)` - Load from pickle file

Example usage:
```python
from src.utils.helpers import save_pickle, load_pickle

# Save
data = {'key': 'value', 'numbers': [1, 2, 3]}
save_pickle(data, './data/my_data.pkl')

# Load
loaded_data = load_pickle('./data/my_data.pkl')
```

---

**Next Step:** Install dependencies and run the Flask app!
