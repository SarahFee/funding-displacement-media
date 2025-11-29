# Contributing to Humanitarian Funding Analysis

Thank you for your interest in contributing to this project! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/humanitarian-funding-analysis.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add meaningful commit message"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting: `black src/`
- Run linter: `flake8 src/`
- Add docstrings to all functions
- Include type hints where appropriate

## Testing

- Write tests for new features in `tests/`
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Areas for Contribution

### Data Sources
- Add new data sources (ACLED, ReliefWeb, HDX)
- Improve API clients with error handling
- Add caching mechanisms

### Analysis
- Country-level analysis
- Different GDELT keywords
- Lag analysis between variables
- Additional statistical methods

### Visualization
- Interactive plots (Plotly, Altair)
- Dashboard development
- Animation of time series

### Documentation
- Improve Quarto documentation
- Add tutorials
- Create example notebooks
- Translate documentation

### Infrastructure
- CI/CD pipeline
- Docker containerization
- Automated testing
- Performance optimization

## Questions?

Open an issue or reach out via GitHub discussions.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.
