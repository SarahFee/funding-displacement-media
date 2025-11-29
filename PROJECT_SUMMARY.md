# Project Summary: Humanitarian Funding Analysis

## Overview

This repository contains a complete analytical pipeline examining the relationship between humanitarian funding flows, displacement patterns, and media coverage from 2022-2024. The project is designed for reproducibility, modularity, and extensibility.

## Key Components

### 1. Data Acquisition (`src/data_acquisition/`)

Three independent API clients:

- **FTS Client** (`fetch_fts.py`): Fetches funding data from OCHA's Financial Tracking Service
- **DTM Client** (`fetch_dtm.py`): Fetches displacement data from IOM's Displacement Tracking Matrix
- **GDELT Client** (`fetch_gdelt.py`): Fetches media coverage and sentiment from GDELT Project

All clients include:
- Error handling and logging
- Rate limiting where appropriate
- Raw data caching
- Retry mechanisms

### 2. Data Processing (`src/processing/`)

Modular processing pipelines:

- **Funding Processor** (`process_funding.py`): 
  - Prophet time series modeling
  - Quarterly seasonality extraction
  - Log transformation for variance stabilization
  - MinMaxScaler normalization

- **Displacement Processor** (`process_displacement.py`):
  - Quarterly aggregation across 44 countries
  - Date parsing and filtering
  - Normalization to [0,1] range

- **GDELT Processor** (`process_gdelt.py`):
  - Volume and tone data handling
  - Quarterly averaging
  - Normalization

### 3. Statistical Analysis (`src/modeling/`)

- **Correlation Analysis** (`correlation_analysis.py`):
  - Pearson correlation calculation
  - P-value significance testing
  - Temporal alignment of datasets
  - Results export (CSV and TXT reports)

### 4. Visualization (`src/visualization/`)

Publication-quality plots:

- Funding vs. Displacement trends
- Funding vs. Media Volume
- Displacement vs. Media Coverage
- Funding vs. Media Sentiment

All visualizations:
- 300 DPI resolution
- Professional color schemes
- Normalized [0,1] scales for comparison
- Saved as PNG

### 5. Pipeline Orchestration (`src/main.py`)

Complete end-to-end pipeline:
1. Data acquisition from all sources
2. Processing and transformation
3. Correlation analysis
4. Visualization generation
5. Results summary logging

## Documentation

### Quarto Website (`docs/`)

Three comprehensive documents:

1. **Index** (`index.qmd`): 
   - Project overview
   - Key findings
   - Quick start guide
   - Research context

2. **Methodology** (`methodology.qmd`):
   - Detailed data sources
   - Processing steps explained
   - Statistical methods
   - Limitations and assumptions
   - Reproducibility instructions

3. **API Reference** (`api_reference.qmd`):
   - Function documentation
   - Parameter descriptions
   - Code examples
   - Configuration options

### Notebooks (`notebooks/`)

- Original Jupyter notebook preserved
- Example analysis workflow
- Interactive exploration

## File Structure

```
humanitarian-funding-analysis/
├── README.md                    # Project overview
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Python dependencies
├── setup.sh                     # Setup script
├── .gitignore                   # Git ignore rules
├── .github/
│   └── workflows/
│       └── deploy-docs.yml      # GitHub Pages deployment
├── data/
│   ├── raw/                     # Raw API responses (gitignored)
│   ├── processed/               # Processed data (gitignored)
│   └── outputs/                 # Visualizations (gitignored)
├── src/
│   ├── main.py                  # Pipeline orchestrator
│   ├── data_acquisition/
│   │   ├── __init__.py
│   │   ├── fetch_fts.py
│   │   ├── fetch_dtm.py
│   │   └── fetch_gdelt.py
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── process_funding.py
│   │   ├── process_displacement.py
│   │   └── process_gdelt.py
│   ├── modeling/
│   │   ├── __init__.py
│   │   └── correlation_analysis.py
│   └── visualization/
│       ├── __init__.py
│       └── plots.py
├── scripts/
│   └── original_analysis.py     # Original monolithic script
├── notebooks/
│   └── analysis_example.ipynb   # Jupyter notebook
└── docs/
    ├── _quarto.yml              # Quarto configuration
    ├── index.qmd
    ├── methodology.qmd
    └── api_reference.qmd
```

## Technical Stack

**Core:**
- Python 3.8+
- pandas, numpy, scipy

**Time Series:**
- Prophet (Meta's forecasting library)

**Data Acquisition:**
- requests
- gdeltdoc

**Visualization:**
- matplotlib
- seaborn

**Documentation:**
- Quarto

**Development:**
- Git
- pytest (testing)
- black (formatting)

## Key Features

### Modularity
- Each component is independently testable
- Easy to swap data sources
- Extensible architecture

### Reproducibility
- Complete pipeline automation
- Version-controlled code
- Documented methodology
- Public APIs only

### Documentation
- Comprehensive Quarto website
- API reference with examples
- Inline code comments
- Docstrings for all functions

### Professional Quality
- Publication-ready visualizations
- Statistical rigor (p-values, correlation coefficients)
- Error handling and logging
- Clean code structure

## Research Context

This project supports research into:

1. **Funding Stress Index (FSI)**: Predicting humanitarian funding volatility
2. **Parametric Insurance**: Applying insurance mechanisms to humanitarian finance
3. **Data-Driven Advocacy**: Evidence-based donor engagement
4. **Media-Funding Dynamics**: Understanding visibility bias in crisis response

## Main Findings

The analysis reveals:

- **Weak correlation** between funding and displacement (actual need)
- **Moderate to strong correlation** between funding and media coverage
- Funding lags behind media attention peaks
- High-profile crises attract disproportionate resources

**Implication**: Humanitarian funding is more responsive to visibility than to data-driven needs assessment.

## Usage Scenarios

### For Researchers
- Extend analysis to additional countries
- Test different time periods
- Add new data sources
- Develop predictive models

### For Practitioners
- Monitor funding gaps in real-time
- Identify underfunded crises
- Advocate for data-driven allocation
- Demonstrate visibility bias

### For Developers
- Contribute new features
- Improve API clients
- Add visualization options
- Enhance documentation

## Next Steps

### Immediate
1. Publish to GitHub
2. Deploy Quarto documentation
3. Add unit tests
4. Create Docker container

### Short-term
1. Country-level analysis
2. Different GDELT keywords
3. Lag correlation analysis
4. Interactive dashboards

### Long-term
1. Real-time monitoring system
2. Predictive funding models
3. Integration with operational tools
4. Multi-year analysis (5-10 years)

## Contact

**Author**: Sarah Fekih  
**Role**: Data Scientist & AI Agents Consultant  
**Organization**: International Organization for Migration (IOM)

**GitHub**: [humanitarian-funding-analysis](https://github.com/yourusername/humanitarian-funding-analysis)

## Citation

```bibtex
@misc{fekih2025humanitarian,
  author = {Fekih, Sarah},
  title = {Humanitarian Funding Analysis: Examining the Data-Action Gap},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/yourusername/humanitarian-funding-analysis}
}
```

## License

MIT License - see LICENSE file for details.
