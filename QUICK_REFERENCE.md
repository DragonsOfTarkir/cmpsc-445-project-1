# QUICK_REFERENCE.md

# Quick Reference Guide

## Command Cheat Sheet

### Installation & Setup
```bash
# Install dependencies
pip install pandas numpy scikit-learn xgboost matplotlib seaborn requests scipy jupyter

# Clone or navigate to project
cd /workspaces/cmpsc-445-project-1
```

### Running the Pipeline

```bash
# Test run (synthetic data) - recommended first step
python test_pipeline.py

# Full analysis (real data from NOAA/NASA/OWID)
python main_analysis.py

# Individual components
python data_collection/noaa_data.py    # Collect NOAA data
python data_collection/nasa_data.py    # Collect NASA data
python data_collection/owid_data.py    # Collect OWID data
python data_preprocessing/preprocessor.py  # Preprocess data
python models/regressor.py             # Train models
```

### Checking Results

```bash
# View processed data
head -20 data/processed/climate_data_processed.csv

# View model results
cat models/model_results.json

# List generated plots
ls -lh reports/figures/

# View analysis report
cat reports/ANALYSIS_REPORT.md
```

---

## File Locations

| Item | Location |
|------|----------|
| Raw data (from sources) | `data/raw/` |
| Processed data (final) | `data/processed/climate_data_processed.csv` |
| Model metrics | `models/model_results.json` |
| Generated plots | `reports/figures/` |
| Analysis report | `reports/ANALYSIS_REPORT.md` |
| Code | `data_collection/`, `data_preprocessing/`, `models/`, `visualizations/` |

---

## Key Classes & Methods

### Data Collection

```python
from data_collection.noaa_data import NOAACollector
from data_collection.nasa_data import NASACollector
from data_collection.owid_data import OWIDCollector

# NOAA
collector = NOAACollector()
df = collector.collect_all()  # Returns merged DataFrame

# NASA
collector = NASACollector()
df = collector.collect_all()

# OWID
collector = OWIDCollector()
df = collector.collect_all()
```

### Preprocessing

```python
from data_preprocessing.preprocessor import DataPreprocessor

preprocessor = DataPreprocessor()
df, samples = preprocessor.process()
# Returns: (processed DataFrame, first 3 rows for report)
```

### Modeling

```python
from models.regressor import TemperatureRegressor

regressor = TemperatureRegressor()
results = regressor.train_all_models()
# Returns: {models, results, feature_importances, ...}
```

### Visualization

```python
from visualizations.plotter import ClimatePlotter

plotter = ClimatePlotter()
plotter.plot_greenhouse_gas_trends(df)
plotter.plot_temperature_vs_co2(df)
plotter.plot_feature_importance(importances)
```

---

## Common Tasks

### Task 1: Run Full Analysis
```bash
# Everything in one command
python main_analysis.py
```

### Task 2: Just Get Raw Data
```bash
# Run only data collection
python data_collection/noaa_data.py
python data_collection/nasa_data.py  
python data_collection/owid_data.py
# Then check: ls data/raw/
```

### Task 3: Preprocess Data You Already Downloaded
```python
from data_preprocessing.preprocessor import DataPreprocessor
p = DataPreprocessor()
df, samples = p.process()
print(samples)  # View first 3 rows
```

### Task 4: Train Models on Your Data
```python
from models.regressor import TemperatureRegressor
r = TemperatureRegressor("path/to/processed/data.csv")
results = r.train_all_models()
print(results['results'])  # See metrics
```

### Task 5: Create Specific Visualization
```python
from visualizations.plotter import ClimatePlotter
import pandas as pd

df = pd.read_csv("data/processed/climate_data_processed.csv")
plotter = ClimatePlotter()
plotter.plot_temperature_vs_co2(df)
# Check: reports/figures/temperature_vs_co2.png
```

---

## Expected Output

### After `test_pipeline.py`:
```
reports/
├── TEST_REPORT.md              # Analysis results
└── figures/
    └── (All PNG plots)

models/
└── model_results.json           # R², RMSE, MAE

data/
├── raw/
│   ├── noaa_combined.csv
│   ├── nasa_combined.csv
│   └── owid_combined.csv
└── processed/
    └── climate_data_processed.csv
```

### After `main_analysis.py`:
```
Same as above, but with REAL data from NOAA/NASA/OWID
```

---

## Important Paths

| Path | Purpose |
|------|---------|
| `data/raw/` | Raw data from sources (before processing) |
| `data/processed/` | Final merged, cleaned dataset |
| `models/` | Trained model results and metrics |
| `reports/` | Final analysis and visualizations |
| `reports/figures/` | All PNG plots |
| `reports/ANALYSIS_REPORT.md` | Main written report |

---

## Feature List

### Greenhouse Gases (Sources)
- CO₂ (ppm) - NOAA
- CH₄ (ppb) - NOAA
- N₂O (ppb) - NOAA

### Climate Variables (Sources)
- Temperature Anomaly (°C) - NASA GISS
- Solar Irradiance (W/m²) - NOAA
- CO₂ Emissions (GtCO₂) - OWID
- Aerosol Optical Depth - OWID (proxy)

### Engineered Features
- Years since baseline (1980)
- CO₂ growth rate (%)
- CH₄ growth rate (%)
- 12-month moving averages
- GHG combined index
- Solar irradiance index
- CO₂ anomaly from baseline

---

## Models Trained

| Model | Best For | Speed |
|-------|----------|-------|
| Linear Regression | Interpretability | Fast |
| Random Forest | Accuracy + Robustness | Medium |
| XGBoost | Maximum Accuracy | Medium |

**Recommendation**: Use Random Forest feature importance for best balance

---

## Interpreting Feature Importance

### High Importance (>0.1)
→ Strong predictor of temperature
→ Likely a major driver

### Medium Importance (0.05-0.1)
→ Moderate contribution
→ Secondary drivers

### Low Importance (<0.05)
→ Weak predictor
→ Minor or no effect

### Example Results
```
CO₂ concentration:    0.32  ← Dominant
CO₂ growth rate:      0.22  ← Strong
CH₄ concentration:    0.18  ← Medium
Solar irradiance:     0.02  ← Weak
Aerosol optical depth: 0.01  ← Very weak
```

**Interpretation**: Anthropogenic (human) factors are dominant

---

## Troubleshooting

### Problem: Import Error
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution**: 
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn
```

### Problem: Data Not Found
```
FileNotFoundError: data/raw/noaa_combined.csv
```
**Solution**: Run data collection first
```bash
python data_collection/noaa_data.py
```

### Problem: Network Error During Collection
```
requests.exceptions.ConnectionError: ...
```
**Solution**: Check internet, retry later, or use synthetic data
```bash
python test_pipeline.py  # Uses synthetic data
```

### Problem: Plots Not Created
```
No PNG files in reports/figures/
```
**Solution**: Create directory first
```bash
mkdir -p reports/figures
python main_analysis.py
```

---

## File Sizes (Approximate)

| File | Size | Note |
|------|------|------|
| noaa_combined.csv | 10 KB | Monthly, 1980-2023 |
| nasa_combined.csv | 5 KB | Yearly, 1880-2023 |
| owid_combined.csv | 2 KB | Yearly, 1990-2023 |
| climate_data_processed.csv | 5 KB | Merged, yearly |
| model_results.json | 1 KB | Metrics only |
| All PNG plots | 2-3 MB | 8-10 plots, 300 DPI |

**Total Project Size**: <10 MB

---

## Execution Times

| Task | Time |
|------|------|
| Data collection (network) | 2-5 min |
| Preprocessing | <1 sec |
| Model training | 5-10 sec |
| Visualization | 10-20 sec |
| **Total** | **5-15 min** |

---

## Deliverables for Submission

### Required Files
- [ ] GitHub repo link (public)
- [ ] `reports/ANALYSIS_REPORT.md` (main report)
- [ ] `data/processed/climate_data_processed.csv` (processed data)
- [ ] `data_collection/*.py` (collection scripts)
- [ ] All models and visualizations

### Report Must Include
- [ ] Data sources description
- [ ] Sample data (3 rows)
- [ ] Model performance (R², RMSE, MAE)
- [ ] Feature importance ranking
- [ ] Human vs natural factors discussion
- [ ] Figure references/captions
- [ ] Limitations acknowledged
- [ ] AI usage disclosed

---

## Important Concepts

### Feature Importance
- How much each variable contributes to predictions
- Higher = more important
- Consistent across models = more reliable

### R² Score
- Explained variance ratio (0-1)
- 0.85+ is considered very good
- Shows model fit quality

### RMSE (Root Mean Squared Error)
- Prediction error in same units as target (°C)
- Smaller is better
- 0.15-0.25°C is reasonable for climate data

### MAE (Mean Absolute Error)
- Average absolute prediction error
- More interpretable than RMSE
- Useful for comparing model error

---

## Links

**Documentation**:
- README.md - Project overview
- IMPLEMENTATION_GUIDE.md - How to use code
- PROJECT_OVERVIEW.md - Complete project details
- CODE_QUALITY.md - Architecture & design
- This file - Quick reference

**Data Sources**:
- NOAA: https://gml.noaa.gov/
- NASA: https://data.giss.nasa.gov/
- OWID: https://ourworldindata.org/

---

## Minimal Viable Run

Fastest way to verify everything works:

```bash
# 1. Install
pip install pandas numpy scikit-learn xgboost matplotlib seaborn

# 2. Test with synthetic data
python test_pipeline.py  # ~3 minutes

# 3. Check outputs
ls reports/figures/      # See generated plots
cat reports/TEST_REPORT.md # View results
```

Done! Now ready for real data with `python main_analysis.py`

---

**Last Updated**: 2024
**Python Version**: 3.8+
**Status**: Ready for use
