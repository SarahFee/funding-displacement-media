# Funding, displacement and media analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A data-driven analysis examining the relationship between humanitarian funding flows, displacement patterns, and media coverage (2022-2024).

## Project Overview

This repository contains the analytical pipeline and methodology for investigating whether humanitarian funding follows actual displacement needs or is driven by media visibility patterns.

**Key Research Questions:**
- Does humanitarian funding correlate with displacement trends?
- How does media coverage influence funding allocation?
- Can we identify the "visibility bias" in humanitarian response?

## Datasets

### 1. FTS (Financial Tracking Service)
- **Source**: [OCHA FTS API](https://fts.unocha.org/)
- **Content**: Global humanitarian funding flows
- **Coverage**: 2022-2024
- **Granularity**: Daily transaction-level data

### 2. DTM (Displacement Tracking Matrix)
- **Source**: [IOM DTM API](https://dtm.iom.int/)
- **Content**: Internal displacement data
- **Coverage**: 44 countries
- **Granularity**: Quarterly aggregated reporting

### 3. GDELT (Global Database of Events, Language, and Tone)
- **Source**: [GDELT Project](https://www.gdeltproject.org/)
- **Content**: Media coverage volume and sentiment
- **Coverage**: Global news articles
- **Granularity**: Daily time-series data

## Repository Structure

```
humanitarian-funding-analysis/
├── data/                      # Data storage (gitignored)
│   ├── raw/                   # Raw API responses
│   ├── processed/             # Cleaned and transformed data
│   └── outputs/               # Generated visualizations
├── src/                       # Source code
│   ├── data_acquisition/      # API clients and data fetchers
│   ├── processing/            # Data transformation pipelines
│   ├── modeling/              # Prophet models and forecasting
│   └── visualization/         # Plotting functions
├── notebooks/                 # Analysis notebooks
├── docs/                      # Quarto documentation
├── tests/                     # Unit tests
└── requirements.txt           # Python dependencies
```

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/humanitarian-funding-analysis.git
cd humanitarian-funding-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
# Run the complete pipeline
python src/main.py

# Or run specific components
python src/data_acquisition/fetch_fts.py
python src/data_acquisition/fetch_dtm.py
python src/data_acquisition/fetch_gdelt.py
```

### Generating Documentation

```bash
# Install Quarto: https://quarto.org/docs/get-started/
quarto render docs/
```

## Methodology

### Data Pipeline

1. **Data Acquisition**: Fetching from three independent APIs
2. **Temporal Alignment**: Normalizing to common date ranges (Feb 2022 - Feb 2024)
3. **Time Series Modeling**: Prophet for funding forecasting with quarterly seasonality
4. **Normalization**: MinMaxScaler for cross-series comparison
5. **Aggregation**: Quarterly resolution for trend analysis
6. **Correlation Analysis**: Pearson coefficients with significance testing

### Statistical Approach

- **Funding Data**: Log-transformed to stabilize variance, modeled with Prophet
- **Displacement Data**: Quarterly aggregation across 44 countries
- **Media Data**: Volume and tone metrics, quarterly averaged
- **Normalization**: All series scaled to [0,1] for visual comparison
- **Correlation**: Pearson correlation with p-value significance testing

## Key Findings

The analysis reveals:
- Funding shows stronger correlation with media patterns than displacement trends
- Media coverage volume and tone significantly influence funding allocation
- High-profile crises receive disproportionate funding compared to displacement severity
- Funding decisions lag behind media attention peaks

For detailed findings, see the [Quarto documentation](docs/).

## Citation

If you use this analysis in your research, please cite:

```bibtex
@misc{fekih2025humanitarian,
  author = {Fekih, Sarah},
  title = {Humanitarian Funding Analysis: Examining the Data-Action Gap},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/yourusername/humanitarian-funding-analysis}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OCHA** for maintaining the FTS API
- **IOM** for the DTM data infrastructure
- **GDELT Project** for comprehensive media monitoring
- **Prophet** team at Meta for the forecasting library

## Contact

Sarah Fekih

Project Link: [https://github.com/SarahFee/funding-displacement](https://github.com/SarahFee/funding-displacement)
Blog Post: [When Aid Ignores Its Own Data](https://medium.com/@fekih.sarah/when-aid-ignores-its-own-data-f412eaf04633) - Medium article discussing the findings and implications

---

**Note**: This is a research project. Findings should be interpreted within the context of the methodology and limitations described in the documentation.
