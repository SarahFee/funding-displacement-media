# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Extract the Repository

```bash
# Extract the archive
tar -xzf humanitarian-funding-analysis.tar.gz
cd humanitarian-funding-analysis
```

### Step 2: Run Setup

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

### Step 3: Run the Analysis

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

## 📊 View Results

After running the analysis, check:

- **Visualizations**: `data/outputs/*.png`
- **Correlation Results**: `data/outputs/correlation_results.csv`
- **Detailed Report**: `data/outputs/correlation_report.txt`

## 📚 Generate Documentation

```bash
# Install Quarto first: https://quarto.org/docs/get-started/

# Render documentation
quarto render docs/

# View locally
quarto preview docs/
```

## 🔧 Customize the Analysis

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

## 🐛 Troubleshooting

### API Connection Issues

If you get network errors:
- Check internet connection
- Some APIs may have rate limits
- Try again later or reduce batch sizes

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

## 📖 Next Steps

1. **Read the methodology**: `docs/methodology.qmd`
2. **Explore the API**: `docs/api_reference.qmd`
3. **Run the notebook**: `jupyter notebook notebooks/analysis_example.ipynb`
4. **Customize visualizations**: Edit `src/visualization/plots.py`
5. **Add new data sources**: Create new fetchers in `src/data_acquisition/`

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines on:
- Code style
- Testing
- Pull requests
- Areas for contribution

## 📧 Need Help?

- Open an issue on GitHub
- Check the documentation
- Review the PROJECT_SUMMARY.md

## 🎯 Common Tasks

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

## ⚡ Pro Tips

1. **Cache API responses**: Raw data is saved to `data/raw/` automatically
2. **Skip fetching**: Use cached data by commenting out fetch calls in `main.py`
3. **Parallel processing**: Modify DTM fetcher to use concurrent requests
4. **Custom analysis**: Create new notebooks in `notebooks/` directory

---

Happy analyzing! 🎉
