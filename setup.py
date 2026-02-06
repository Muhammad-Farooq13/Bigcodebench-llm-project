"""Setup configuration for BigCodeBench LLM Project"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="bigcodebench-llm",
    version="1.0.0",
    description="Professional LLM project for code understanding on BigCodeBench dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Muhammad Farooq",
    author_email="mfarooqshafee333@gmail.com",
    url="https://github.com/Muhammad-Farooq-13/bigcodebench-llm-project",
    license="MIT",
    
    packages=find_packages(exclude=["tests", "notebooks", "docs"]),
    python_requires=">=3.8",
    
    install_requires=[
        # Core Data Science Libraries
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "scipy>=1.11.1",
        
        # Deep Learning & LLM Libraries
        "torch>=2.0.1",
        "transformers>=4.32.1",
        "datasets>=2.14.0",
        "tokenizers>=0.13.3",
        
        # Evaluation
        "evaluate>=0.4.0",
        
        # Web Framework
        "flask>=2.3.2",
        "flask-cors>=4.0.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.2.0",
        
        # ML Workflow
        "mlflow>=2.7.0",
        "pydantic>=2.2.0",
        
        # Utils
        "tqdm>=4.65.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
    ],
    
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
        ],
        "viz": [
            "matplotlib>=3.7.2",
            "seaborn>=0.12.2",
            "plotly>=5.15.0",
        ],
        "monitoring": [
            "wandb>=0.15.8",
            "python-json-logger>=2.0.7",
        ],
        "docker": [
            "redis>=4.6.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "bigcodebench-pipeline=mlops_pipeline:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    keywords=[
        "machine-learning",
        "deep-learning",
        "nlp",
        "code-understanding",
        "transformer",
        "hugging-face",
        "mlops",
        "pytorch",
    ],
    
    zip_safe=False,
    include_package_data=True,
)
