# Climate Change Root-Cause Analysis: Regression-Based Driver Identification

A comprehensive data science pipeline to identify the most influential drivers of global temperature change using regression models and feature importance analysis.

## Project Overview

This project implements a complete analytical pipeline to understand which environmental factors contribute most to global temperature variation. Using data from NOAA, NASA GISS, and Our World in Data, we:

1. **Collect** atmospheric greenhouse gas data, temperature measurements, and anthropogenic factors
2. **Preprocess** multi-source data with standardization and feature engineering  
3. **Train** multiple regression models (Linear Regression, Random Forest, XGBoost)
4. **Analyze** feature importance to identify key temperature drivers
5. **Visualize** relationships between factors and temperature anomaly
6. **Report** findings on human vs natural factors influencing climate

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run Full Pipeline

```bash
# Execute complete analysis (data collection → preprocessing → modeling → visualization)
python main_analysis.py
```

This will:
- Collect data from three scientific sources
- Preprocess and align datasets
- Train three regression models
- Generate feature importance ranks
- Create diagnostic plots
- Generate comprehensive report

### Run Individual Components

```bash
# Data Collection Only
python data_collection/noaa_data.py
python data_collection/nasa_data.py
python data_collection/owid_data.py

# Data Preprocessing
python data_preprocessing/preprocessor.py

# Model Training
python models/regressor.py

# Visualization
# (Called automatically from main analysis)
```

## Project Structure

```
cmpsc-445-project-1/
├── data/
│   ├── raw/                          # Original downloaded datasets
│   │   ├── noaa_combined.csv         # Greenhouse gas data
│   │   ├── nasa_combined.csv         # Temperature and solar data
│   │   └── owid_combined.csv         # Emissions data
│   └── processed/
│       └── climate_data_processed.csv # Merged, engineered dataset
│
├── data_collection/                  # Data fetching modules
│   ├── noaa_data.py                 # NOAA GHG collection
│   ├── nasa_data.py                 # NASA temperature/irradiance
│   └── owid_data.py                 # OWID emissions/anthropogenic
│
├── data_preprocessing/               # Data processing pipeline
│   └── preprocessor.py              # Cleaning, merging, feature engineering
│
├── models/                          # Regression models
│   └── regressor.py                # Model training and evaluation
│
├── visualizations/                  # Result visualizations
│   └── plotter.py                  # Plots and charts
│
├── reports/
│   ├── figures/                    # Generated plots
│   ├── ANALYSIS_REPORT.md          # Comprehensive findings
│   └── model_results.json          # Model metrics
│
├── main_analysis.py                # Main orchestration script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Data Sources

### 1. NOAA Global Monitoring Laboratory
- **URL**: https://gml.noaa.gov/ccgg/trends/
- **Data**: CO₂, CH₄, N₂O monthly concentrations
- **Content**: Mauna Loa & global averages
- **Use**: Primary greenhouse gas drivers

### 2. NASA GISS Surface Temperature Analysis
- **URL**: https://data.giss.nasa.gov/gistemp/
- **Data**: Global surface temperature anomaly (monthly, 1880-present)
- **Target Variable**: Temperature anomaly (°C)
- **Solar Data**: https://www.ncei.noaa.gov/data/total-solar-irradiance/
- **Use**: Temperature monitoring, solar forcing

### 3. Our World in Data (OWID)
- **URL**: https://ourworldindata.org/
- **Data**: CO₂ emissions by sector, energy use, anthropogenic factors
- **Content**: Global emissions, industrial activity metrics
- **Use**: Human-driven activity factors

## Key Features Engineered

- **Time-based**: Years since baseline (1980)
- **Growth Rates**: Annual percent change in CO₂, CH₄
- **Smoothing**: 12-month moving averages
- **Composite**: Combined GHG metric (CO₂ + 25×CH₄)
- **Anomalies**: Deviation from historical baseline
- **Indices**: Normalized solar irradiance
- **Volcanic Activity**: Aerosol optical depth proxy

## Regression Models

| Model | Type | Use Case | Strength |
|-------|------|----------|----------|
| **Linear Regression** | Parametric | Interpretability, coefficients | Direct relationships |
| **Random Forest** | Tree-based ensemble | Non-linear patterns, feature rank | Captures interactions |
| **XGBoost** | Gradient boosting | Highest accuracy | Reduces bias/variance |

All models trained on 70% of data, evaluated on 30% test set.

## Key Findings Example

Feature importance typically shows:

1. **CO₂ Concentration** - Dominant driver (highest importance)
2. **CO₂ Growth Rate** - Acceleration of warming
3. **CH₄ Concentration** - Secondary GHG driver
4. **Solar Irradiance** - Lower importance (natural variability less influential)
5. **N₂O Concentration** - Minor but measurable effect

**Interpretation**: Anthropogenic (human-driven) factors, particularly CO₂ emissions, are the strongest predictive factors for temperature anomaly, while natural factors like solar variations play secondary roles. This aligns with established climate science consensus.

## Visualizations Generated

- `greenhouse_gas_trends.png` - Time series of CO₂, CH₄, N₂O
- `temperature_vs_co2.png` - Scatter plot with trend line
- `time_series_comparison.png` - Dual-axis temperature & CO₂
- `feature_importance_linear.png` - Linear regression coefficients
- `feature_importance_random_forest.png` - Random forest rankings
- `feature_importance_xgboost.png` - XGBoost rankings
- `model_comparison.png` - R², RMSE, MAE across models
- `residuals_*.png` - Diagnostics for each model

## Analysis Report

The comprehensive report (`reports/ANALYSIS_REPORT.md`) includes:

- **Data Description**: Sources, preprocessing steps, engineer features
- **Sample Data**: Example rows post-processing
- **Model Performance**: R², RMSE, MAE for each model
- **Root-Cause Analysis**: Ranked feature importance by model
- **Interpretation**: Human vs natural factor discussion
- **Limitations**: Causal inference challenges, data quality notes
- **Conclusion**: Alignment with climate science
- **AI Disclosure**: Transparency on tool usage

## Methodology

### Data Pipeline

```
Raw Data (3 sources)
    ↓
Standardize (convert to yearly)
    ↓
Merge (join on date)
    ↓
Fill Missing Values (interpolation)
    ↓
Feature Engineering
    ↓
Processed Dataset
```

### Model Pipeline

```
Processed Data (70/30 split)
    ↓
Scale Features (standardize)
    ↓
Train Models (Linear, RF, XGBoost)
    ↓
Evaluate (R², RMSE, MAE)
    ↓
Extract Feature Importance
    ↓
Rank & Visualize
```

## Requirements

- Python 3.8+
- pandas 2.1.3
- numpy 1.24.3
- scikit-learn 1.3.2
- xgboost 2.0.2
- matplotlib 3.8.2
- seaborn 0.13.0
- requests 2.31.0

See `requirements.txt` for full list.

## Limitations & Caveats

1. **Causation vs Correlation**: Regression identifies associations, not causation
2. **Aggregation**: Global metrics hide regional variations
3. **Feedback Mechanisms**: Complex climate feedbacks not explicitly modeled
4. **Data Quality**: Limited by source data quality and completeness
5. **Temporal**: Annual resolution may miss seasonal/sub-annual dynamics
6. **Scope**: Regression relies on observable correlations, not physical processes

## Discussion

### Alignment with Climate Science

The analysis results—showing CO₂ and anthropogenic factors as dominant temperature drivers—align with scientific consensus:
- IPCC reports: 100%+ of warming from human activities
- Multiple lines of evidence support GHG dominance
- Solar/natural forcing explains only ~10% of observed warming

### Ethical Considerations

- **Data Reliability**: All sources from reputable institutions (NOAA, NASA, OWID)
- **Scientific Accuracy**: Methods standard in climate analytics
- **Transparency**: Full disclosure of methods, limitations, AI usage
- **Reproducibility**: Open code, documented pipeline

## Future Improvements

- Integrate additional data sources (ocean heat content, ice sheet dynamics)
- Spatial analysis (regional drivers, latitude bands)
- Causal inference (instrumental variables, causal forests)
- Deep learning (neural networks for nonlinear patterns)
- Real-time updating pipeline
- Interactive dashboard

## References

- NOAA GML: https://gml.noaa.gov/
- NASA GISS: https://data.giss.nasa.gov/
- Our World in Data: https://ourworldindata.org/
- IPCC Climate Report: https://www.ipcc.ch/

## Author Notes

This project demonstrates the application of regression-based causal inference (or at least predictive analytics with interpretability) to one of society's most important questions: What is driving climate change?

While machine learning cannot prove causation, feature importance provides compelling quantitative evidence about which factors matter most in predicting global temperature change. The consistency across multiple model types strengthens confidence in the findings.

## License

Educational - CMPSC 445 Project