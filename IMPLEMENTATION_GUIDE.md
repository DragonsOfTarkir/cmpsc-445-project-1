# Project Implementation Guide

## Project Overview

This is a complete climate change root-cause analysis system that identifies the most influential drivers of global temperature change using regression modeling and feature importance analysis.

## Getting Started

### 1. Installation

```bash
# Clone or navigate to project directory
cd /workspaces/cmpsc-445-project-1

# Install dependencies (flexible versions for compatibility)
pip install pandas numpy scikit-learn xgboost matplotlib seaborn requests scipy jupyter
```

### 2. Quick Start (Test Mode)

To verify the entire pipeline with synthetic data:

```bash
python test_pipeline.py
```

This will:
- Generate synthetic climate data (~44 years)
- Preprocess and merge datasets
- Train 3 regression models
- Generate visualizations
- Create an analysis report

**Output**: `reports/TEST_REPORT.md` and plots in `reports/figures/`

### 3. Full Analysis (Real Data)

To collect real data from NOAA, NASA, and OWID:

```bash
python main_analysis.py
```

**Note**: Real data collection requires internet access and may take 5-15 minutes.

## Project Structure

```
├── data_collection/              # Data fetching modules
│   ├── noaa_data.py             # NOAA greenhouse gases
│   ├── nasa_data.py             # NASA temperature & solar
│   └── owid_data.py             # OWID emissions & proxies
│
├── data_preprocessing/           # Data processing
│   └── preprocessor.py          # Cleaning, merging, feature engineering
│
├── models/                       # Regression models
│   └── regressor.py             # Training & evaluation
│
├── visualizations/               # Analysis visualizations
│   └── plotter.py               # Plots and charts
│
├── data/
│   ├── raw/                     # Downloaded datasets
│   └── processed/               # Merged, cleaned dataset
│
├── reports/                     # Analysis output
│   ├── figures/                # Generated plots
│   ├── ANALYSIS_REPORT.md       # Main report
│   └── model_results.json       # Model metrics
│
├── main_analysis.py            # Main pipeline orchestrator
├── test_pipeline.py            # Test with synthetic data
├── requirements.txt             # Python dependencies
└── README.md                    # User documentation
```

## Key Components

### 1. Data Collection (`data_collection/`)

#### NOAACollector
- Fetches CO₂, CH₄, N₂O from NOAA Global Monitoring Laboratory
- Parses text file format
- Saves individual and combined CSVs

#### NASACollector
- Fetches temperature anomaly from NASA GISS
- Fetches solar irradiance from NOAA
- Matches datasets on date

#### OWIDCollector
- Fetches CO₂ emissions from Our World in Data GitHub
- Includes breakdown by source (coal, oil, gas, cement)
- Creates synthetic aerosol optical depth data

### 2. Data Preprocessing (`data_preprocessing/preprocessor.py`)

**Key Functions**:
- `load_all_data()` - Reads raw CSV files
- `merge_datasets()` - Joins all sources on date (outer join)
- `fill_missing_values()` - Linear interpolation + forward/backward fill
- `engineer_features()` - Creates 15+ new features
- `standardize_temporal_format()` - Converts to yearly resolution
- `process()` - Complete pipeline

**Engineered Features**:
- Years since baseline
- CO₂/CH₄ growth rates
- 12-month moving averages
- GHG combined index
- Solar irradiance index
- CO₂ anomalies from baseline

### 3. Regression Models (`models/regressor.py`)

**Models Trained**:
1. **Linear Regression** - For interpretability via coefficients
2. **Random Forest** - 100 trees, max_depth=15
3. **XGBoost** - 100 estimators, learning_rate=0.1

**Output**:
- R² score, RMSE, MAE for each model
- Feature importance rankings
- Model comparison metrics

### 4. Visualizations (`visualizations/plotter.py`)

**Generated Plots**:
- `greenhouse_gas_trends.png` - CO₂, CH₄, N₂O time series
- `temperature_vs_co2.png` - Scatter with polynomial trend
- `time_series_comparison.png` - Dual-axis temperature & CO₂
- `feature_importance_*.png` - Top 15 features per model
- `model_comparison.png` - R², RMSE, MAE bars
- `residuals_*.png` - Diagnostic plots per model

## Usage Examples

### Example 1: Collect Only NOAA Data

```python
from data_collection.noaa_data import NOAACollector

collector = NOAACollector(output_dir="data/raw")
co2_df = collector.collect_co2()
ch4_df = collector.collect_ch4()
noaa_combined = collector.collect_all()
```

### Example 2: Preprocess Existing Data

```python
from data_preprocessing.preprocessor import DataPreprocessor

preprocessor = DataPreprocessor("data/raw", "data/processed")
df_processed, samples = preprocessor.process()

# Access processed data
print(f"Size: {df_processed.shape}")
print(f"Samples:\n{samples}")
```

### Example 3: Train Models Only

```python
from models.regressor import TemperatureRegressor

regressor = TemperatureRegressor("data/processed/climate_data_processed.csv")
results = regressor.train_all_models()

print(results['feature_importances']['random_forest'])
```

### Example 4: Create Specific Visualization

```python
from visualizations.plotter import ClimatePlotter
import pandas as pd

df = pd.read_csv("data/processed/climate_data_processed.csv")
plotter = ClimatePlotter()

plotter.plot_temperature_vs_co2(df)
# Check reports/figures/temperature_vs_co2.png
```

## Understanding the Results

### Feature Importance Interpretation

**High Importance** → Strong predictor of temperature anomaly
- CO₂ concentration (directly linked to greenhouse effect)
- CO₂ growth rate (acceleration of warming)
- CH₄ concentration (GHG forcing)

**Low Importance** → Weak predictor
- Solar irradiance (natural variability less significant)
- Aerosol optical depth (variable effects)

### Model Selection

- **Linear Regression**: Most interpretable, shows direct relationships
- **Random Forest**: Captures nonlinear interactions, generalizes well
- **XGBoost**: Highest accuracy, complex patterns

For this project, **Random Forest** provides good balance of accuracy and interpretability.

## Common Issues & Solutions

### Issue: Data Collection Fails
**Solution**: Check internet connection, verify URLs are accessible
```bash
curl -I https://gml.noaa.gov/  # Test NOAA access
```

### Issue: Missing Values in Processed Data
**Solution**: The preprocessor handles this with interpolation. Check `date` column alignment.
```python
df = pd.read_csv("data/processed/climate_data_processed.csv")
print(df.isnull().sum())  # See remaining NAs
```

### Issue: Model Training Is Slow
**Solution**: Reduce sample size by filtering years:
```python
# In preprocessor, after loading: df = df[df['year'] >= 2000]
```

### Issue: Plots Not Saving
**Solution**: Ensure `reports/figures/` directory exists:
```bash
mkdir -p reports/figures
python visualizations/plotter.py
```

## How to Generate the Final Report

The `main_analysis.py` script automatically generates:

1. **models/model_results.json** - Quantitative metrics
2. **reports/ANALYSIS_REPORT.md** - Comprehensive narrative report
3. **reports/figures/\*.png** - All visualizations

To customize the report, edit the `generate_analysis_report()` function in `main_analysis.py`.

## Submitting Your Project

### Required Deliverables

1. **GitHub Repository** (make public)
   ```bash
   git add .
   git commit -m "Climate analysis project submission"
   git push origin main
   ```

2. **Processed Data** (include CSV or script)
   - `data/processed/climate_data_processed.csv` - Final merged dataset
   - OR: Data collection scripts that generate it

3. **Code Quality**
   - All scripts documented
   - Modular structure (separate files for each step)
   - Error handling in data collection
   - Type hints recommended

4. **Final Report** ("60% of grade")
   - Location: `reports/ANALYSIS_REPORT.md`
   - Includes: All mandatory items from assignment
   - Sample rows from preprocessed data
   - AI usage disclosure

### Checklist

- [ ] All source code in GitHub (public repo)
- [ ] Data collection scripts are reproducible
- [ ] Preprocessing creates >1000 samples
- [ ] 3+ regression models trained
- [ ] Feature importance extracted and visualized
- [ ] Report discusses human vs natural factors
- [ ] Example plots generated and saved
- [ ] README.md documents project
- [ ] requirements.txt lists dependencies
- [ ] Sample data rows shown in report
- [ ] AI usage transparently disclosed

## References

**Data Sources**:
- NOAA: https://gml.noaa.gov/ccgg/trends/
- NASA GISS: https://data.giss.nasa.gov/gistemp/
- OWID: https://ourworldindata.org/co2-emissions

**Methods**:
- Regression for causal inference (limitations noted)
- Feature importance (SHAP, tree-based, coefficients)
- Climate science consensus on anthropogenic forcing

**Climate Science**:
- IPCC Assessment Reports: https://www.ipcc.ch/
- Masson-Delmotte et al. (2021): Climate Change 2021 report
- Schmidt et al. (2010): Attribution of Greenhouse Gas effects

## Additional Tips

1. **Understand the Domain**: Read a climate science article before analyzing results
2. **Check Your Data**: Plot raw data first to ensure it makes sense
3. **Validate Results**: Compare feature importance with scientific literature
4. **Document Everything**: Clear code comments help graders understand decisions
5. **Be Honest About Limitations**: Regression ≠ causation (mention in report)

Good luck! This is an excellent project for learning data science + climate science integration.
