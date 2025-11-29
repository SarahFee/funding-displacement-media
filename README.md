# Project Overview
This repository contains the analytical pipeline and methodology for investigating whether humanitarian funding follows actual displacement needs or is driven by media visibility patterns.
It is the sript behind the Medium's blog Post: [When Aid Funding Ignores the Data It Pays For](https://medium.com/@fekih.sarah/when-aid-ignores-its-own-data-f412eaf04633)

# Quick Start Guide

##  Getting Started in 5 Minutes

### Step 1: Run Setup

```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run setup
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create directory structure

### Step 2: Run the Analysis

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the pipeline
python src/main.py
```

The pipeline will:
1. Fetch data from FTS, DTM, and GDELT APIs
2. Process and normalize the data
3. Calculate correlations
4. Generate visualizations
5. Save results to `data/outputs/`

## View Results

After running the analysis, check:

- **Visualizations**: `data/outputs/*.png`
- **Correlation Results**: `data/outputs/correlation_results.csv`
- **Detailed Report**: `data/outputs/correlation_report.txt`


## Customize the Analysis

### Change Date Range

Edit `src/main.py`:

```python
START_DATE = "2020-01-01"  # Your start date
END_DATE = "2023-12-31"    # Your end date
```

### Change GDELT Keyword

```python
GDELT_KEYWORD = "Refugee Crisis"  # Or "Humanitarian Crisis", etc.
```

### Add Countries to DTM Analysis

```python
COUNTRY_LIST = [
    "LBY", "AFG", "SYR",  # Add more ISO3 codes
    # ...
]
```

## Troubleshooting

### Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Prophet Installation Issues

Prophet requires specific C++ compilers. If installation fails:

```bash
# On macOS
brew install cmake

# On Ubuntu/Debian
sudo apt-get install python3-dev

# Then reinstall
pip install prophet
```


## Contributing

See `CONTRIBUTING.md` for guidelines on:
- Code style
- Testing
- Pull requests
- Areas for contribution


## Common Tasks

### Just want to see the analysis?

```bash
# View the original notebook
jupyter notebook notebooks/analysis_example.ipynb
```

### Want to test individual components?

```python
# Test FTS fetcher
python src/data_acquisition/fetch_fts.py

# Test displacement processor
python src/processing/process_displacement.py
```

### Want to modify visualizations?

Edit `src/visualization/plots.py` and customize:
- Colors
- Figure sizes
- Plot types
- Labels and titles
