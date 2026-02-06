# Contributing to BigCodeBench LLM Project

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a Contributor Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### 1. Report Issues

If you find a bug or have a suggestion:

- **Check existing issues** to avoid duplicates
- **Create a detailed issue** including:
  - Clear title and description
  - Steps to reproduce (for bugs)
  - Expected vs actual behavior
  - Python version and OS
  - Relevant code/logs

### 2. Submit Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project.git
   cd bigcodebench-llm-project
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # If dev extras are available
   ```

4. **Make your changes**
   - Follow the code style (see below)
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests locally**
   ```bash
   pytest tests/ -v
   pytest --cov=src  # Check coverage
   ```

6. **Format and lint code**
   ```bash
   black src/ tests/
   isort src/ tests/
   flake8 src/ tests/
   ```

7. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: description of changes"
   ```

8. **Push and open a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for formatting: `black src/`
- Use [isort](https://pycqa.github.io/isort/) for imports: `isort src/`
- Use [flake8](https://flake8.pycqa.org/) for linting: `flake8 src/`

### Key Style Points

- **Docstrings**: Use Google-style docstrings
  ```python
  def function(param1, param2):
      """Brief description.
      
      Longer description if needed.
      
      Args:
          param1 (str): Description of param1.
          param2 (int): Description of param2.
          
      Returns:
          bool: Description of return value.
          
      Raises:
          ValueError: When something is wrong.
      """
  ```

- **Type Hints**: Use type annotations
  ```python
  def add(a: int, b: int) -> int:
      return a + b
  ```

- **Comments**: Write meaningful comments
  ```python
  # Use comments to explain "why", not "what"
  user_data = process_user(user)  # Convert user dict to model instance
  ```

### Variable Naming

- **Classes**: `PascalCase` (e.g., `CodeBERTModel`)
- **Functions/Variables**: `snake_case` (e.g., `load_dataset`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_SEQUENCE_LENGTH`)
- **Private**: Leading underscore (e.g., `_internal_method`)

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data.py

# Run specific test
pytest tests/test_data.py::test_loader

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v
```

### Writing Tests

- Use `pytest` framework
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive names that explain what is tested

Example:
```python
import pytest
from src.data.loader import load_bigcodebench

def test_load_bigcodebench_returns_dataset():
    """Test that load_bigcodebench returns a dataset."""
    dataset = load_bigcodebench()
    assert dataset is not None
    assert "train" in dataset

def test_load_bigcodebench_with_invalid_split():
    """Test that invalid splits raise an error."""
    with pytest.raises(ValueError):
        load_bigcodebench(split="invalid")
```

## Documentation

### Update When

- Adding new features
- Changing existing functionality
- Adding new modules/classes
- Fixing user-facing bugs

### Documentation Files

- **Code**: Add docstrings to all public functions/classes
- **Features**: Update [README.md](README.md)
- **Setup**: Update [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Workflows**: Update relevant documentation

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference related issues with `#issue-number`
- Start with a verb: "Add", "Fix", "Update", "Refactor", "Remove"

Examples:
```
Add feature: data caching mechanism
Fix bug: incorrect token padding #123
Update documentation for setup process
Refactor: simplify tokenizer logic
Remove deprecated API endpoint
```

## Pull Request Process

1. **Update your branch** with latest main
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Ensure tests pass**
   ```bash
   pytest tests/ -v
   ```

3. **Update CHANGELOG** if needed

4. **Fill PR template** with:
   - Description of changes
   - Related issues
   - Type of change (feature/bugfix/docs)
   - Testing done
   - Screenshots (if UI changes)

5. **Request review** from maintainers

## Development Workflow

### Setting Up Dev Environment

```bash
# Clone repo
git clone https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project.git
cd bigcodebench-llm-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode

# Set up git hooks (optional, for auto-formatting)
# pip install pre-commit
# pre-commit install
```

### Common Tasks

```bash
# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Check coverage
pytest --cov=src

# Build documentation
# cd docs
# make html

# Run Flask app locally
python flask_app.py

# Run MLOps pipeline
python mlops_pipeline.py
```

## Getting Help

- **Documentation**: See [README.md](README.md) and other docs
- **Issues**: Search [existing issues](https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project/issues)
- **Discussions**: Start a [discussion](https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project/discussions)
- **Email**: mfarooqshafee333@gmail.com

## Recognition

Contributors will be recognized in:
- Pull request comments
- Release notes
- Contributors list in README

Thank you for contributing! 🎉
