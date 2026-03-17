# Global Temperature Regression Analysis

## Project Overview
This project builds a regression-based analytical pipeline to identify the most influential drivers (“root causes”) of global temperature change. The goal is to collect environmental data from multiple scientific sources, merge them into a single dataset, and use regression models to determine which factors contribute most to global temperature variation.

The analysis focuses on understanding the relationship between greenhouse gases, natural variables, and global temperature anomalies using feature importance techniques.

---

## Data Sources

The project integrates data from the following sources:

- NOAA Global Monitoring Laboratory  
  - Atmospheric CO₂ and CH₄ concentrations  
  - https://gml.noaa.gov/ccgg/trends/

- NASA GISS Surface Temperature Analysis  
  - Global temperature anomaly data  
  - https://data.giss.nasa.gov/gistemp/

- Our World in Data (OWID)  
  - Anthropogenic factors such as emissions and energy use  
  - https://ourworldindata.org/co2-emissions

These datasets are collected using scripts in the `data_collection/` module and merged into a unified dataset. Monthly data is used to ensure sufficient sample size (≥1000 observations).

---

## Data Preprocessing

Data preprocessing is handled in: # Global Temperature Regression Analysis

## Project Overview
This project builds a regression-based analytical pipeline to identify the most influential drivers (“root causes”) of global temperature change. The goal is to collect environmental data from multiple scientific sources, merge them into a single dataset, and use regression models to determine which factors contribute most to global temperature variation.

The analysis focuses on understanding the relationship between greenhouse gases, natural variables, and global temperature anomalies using feature importance techniques.

---

## Data Sources

The project integrates data from the following sources:

- NOAA Global Monitoring Laboratory  
  - Atmospheric CO₂ and CH₄ concentrations  
  - https://gml.noaa.gov/ccgg/trends/

- NASA GISS Surface Temperature Analysis  
  - Global temperature anomaly data  
  - https://data.giss.nasa.gov/gistemp/

- Our World in Data (OWID)  
  - Anthropogenic factors such as emissions and energy use  
  - https://ourworldindata.org/co2-emissions

These datasets are collected using scripts in the `data_collection/` module and merged into a unified dataset. Monthly data is used to ensure sufficient sample size (≥1000 observations).

---

## Data Preprocessing

Data preprocessing is handled in: data_preprocessing/preprocessor.py

Key steps include:
- Cleaning and removing invalid or missing values
- Standardizing time format (Year and Month)
- Merging datasets from different sources
- Aligning all variables to a consistent temporal resolution

Feature engineering includes:
- Time index (months since baseline)
- CO₂ growth rate
- CH₄ growth rate
- Moving averages (e.g., 12-month averages)

The final dataset is used for model training and analysis.

---

## Model Development

Model training is implemented in: 
Key steps include:
- Cleaning and removing invalid or missing values
- Standardizing time format (Year and Month)
- Merging datasets from different sources
- Aligning all variables to a consistent temporal resolution

Feature engineering includes:
- Time index (months since baseline)
- CO₂ growth rate
- CH₄ growth rate
- Moving averages (e.g., 12-month averages)

The final dataset is used for model training and analysis.

---

## Model Development

Model training is implemented in: models/regressor.py


The following regression models are used:
- Linear Regression (required for interpretability)
- Random Forest Regressor

The dataset is split into training and testing sets (approximately 70/30 split).

- Input features: environmental variables and engineered features  
- Target variable: global temperature anomaly  

---

## Root Cause Analysis

Feature importance is used to identify the most influential variables driving temperature change.

Methods used:
- Linear regression coefficients
- Random forest feature importance scores

### Key Findings:
- CO₂ is the strongest predictor of temperature change
- CH₄ also contributes to temperature variation
- Natural factors (e.g., solar influences) have a smaller impact compared to human-driven variables

These results suggest that anthropogenic factors play a dominant role in global temperature increases.

---

## Visualization

Visualization functions are implemented in: visualizations/plotter.py


The following plots are generated:
- Time-series plots of greenhouse gases vs temperature
- Feature importance bar charts
- Scatter plots for key variables

These visualizations help interpret relationships between environmental factors and temperature changes.

---

## Project Structure
cmpsc-445-project-1-main/
│── main_analysis.py # Main pipeline execution
│── run_analysis.sh # Script to run full pipeline
│── test_pipeline.py # Testing script
│── requirements.txt # Dependencies
│
├── data_collection/ # Data collection scripts
│ ├── noaa_data.py
│ ├── nasa_data.py
│ ├── owid_data.py
│
├── data_preprocessing/ # Data cleaning & merging
│ ├── preprocessor.py
│
├── models/ # Regression models
│ ├── regressor.py
│
├── visualizations/ # Plot generation
│ ├── plotter.py
│
└── documentation files


---

## How to Run the Project

1. Install dependencies: pip install -r requirements.txt

2. Run the full pipeline: python main_analysis.py

Or use: bash run_analysis.sh

---

## Example Data (After Preprocessing)

| Year | Month | CO2 | CH4 | Temperature |
|------|-------|-----|-----|-------------|
| 1958 | 3     | 315.7 | 1650 | -0.12 |
| 1958 | 4     | 316.1 | 1652 | -0.08 |

---

## Discussion & Conclusion

The results indicate that greenhouse gases, particularly CO₂, are the most significant contributors to global temperature change. This aligns with established climate science, which identifies human emissions as the primary driver of recent warming trends.

### Challenges
- Integrating datasets with different formats and resolutions  
- Handling missing or inconsistent data  
- Ensuring accurate time alignment across sources  

### Limitations
- Regression models show correlation, not causation  
- Some climate variables (e.g., ocean currents, cloud cover) are not included  
- Data quality depends on external sources  

### Ethical Considerations
- Importance of using reliable scientific data  
- Avoiding misinterpretation of results  
- Transparency in modeling assumptions and limitations  

---

## Submission

This repository includes:
- Complete source code
- Data collection and preprocessing pipeline
- Regression models and analysis
- Visualizations
- Documentation
