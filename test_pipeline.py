"""
Quick test script to verify the analysis pipeline without external data fetches
Generates synthetic data to validate model training and visualization
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing.preprocessor import DataPreprocessor
from models.regressor import TemperatureRegressor
from visualizations.plotter import ClimatePlotter


def generate_synthetic_data():
    """Generate synthetic climate data for testing."""
    print("\n" + "=" * 70)
    print("GENERATING SYNTHETIC TEST DATA")
    print("=" * 70)
    
    os.makedirs("data/raw", exist_ok=True)
    
    # Generate yearly data from 1980 to 2023
    years = np.arange(1980, 2024)
    n_years = len(years)
    
    # CO2 - increasing trend
    co2_base = 338
    co2_trend = np.linspace(0, 50, n_years)
    CO2 = co2_base + co2_trend + np.random.normal(0, 0.5, n_years)
    
    # CH4 - increasing trend
    ch4_base = 1540
    ch4_trend = np.linspace(0, 350, n_years)
    CH4 = ch4_base + ch4_trend + np.random.normal(0, 5, n_years)
    
    # N2O - increasing trend
    n2o_base = 312
    n2o_trend = np.linspace(0, 30, n_years)
    N2O = n2o_base + n2o_trend + np.random.normal(0, 0.3, n_years)
    
    # Temperature anomaly - correlated with CO2
    temp_base = -0.2
    temp_trend = (CO2 - co2_base) * 0.02 + np.random.normal(0, 0.1, n_years)
    temp_anomaly = temp_base + temp_trend
    
    # Solar irradiance - small variations
    solar_base = 1361
    solar_variation = np.sin(np.linspace(0, 4*np.pi, n_years)) * 0.5
    solar_irradiance = solar_base + solar_variation + np.random.normal(0, 0.1, n_years)
    
    # Create dataframes
    noaa_df = pd.DataFrame({
        'year': years,
        'month': 6,
        'date': pd.to_datetime([f'{y}-06-01' for y in years]),
        'CO2_concentration': CO2,
        'CH4_concentration': CH4,
        'N2O_concentration': N2O
    })
    
    nasa_df = pd.DataFrame({
        'year': years,
        'month': 6,
        'date': pd.to_datetime([f'{y}-06-01' for y in years]),
        'temperature_anomaly': temp_anomaly,
        'solar_irradiance': solar_irradiance
    })
    
    # OWID emissions (synthetic)
    co2_emissions = (CO2 - co2_base) * 10 + np.random.normal(0, 2, n_years)
    aerosol_optical_depth = 0.15 - (years - 1980) * 0.002 + np.random.normal(0, 0.01, n_years)
    aerosol_optical_depth = np.clip(aerosol_optical_depth, 0.08, 0.4)
    
    owid_df = pd.DataFrame({
        'year': years,
        'month': 6,
        'date': pd.to_datetime([f'{y}-06-01' for y in years]),
        'co2': co2_emissions,
        'coal_co2': co2_emissions * 0.4,
        'oil_co2': co2_emissions * 0.35,
        'gas_co2': co2_emissions * 0.25,
        'aerosol_optical_depth': aerosol_optical_depth
    })
    
    # Save datasets
    noaa_df.to_csv('data/raw/noaa_combined.csv', index=False)
    nasa_df.to_csv('data/raw/nasa_combined.csv', index=False)
    owid_df.to_csv('data/raw/owid_combined.csv', index=False)
    
    print("✓ Generated NOAA data (CO2, CH4, N2O)")
    print("✓ Generated NASA data (Temperature, Solar)")
    print("✓ Generated OWID data (Emissions, Aerosols)")
    print(f"✓ Data covers {n_years} years (1980-2023)")
    
    return noaa_df, nasa_df, owid_df


def run_test_pipeline():
    """Run the analysis pipeline with synthetic data."""
    
    print("\n" + "=" * 70)
    print("CLIMATE ANALYSIS PIPELINE - TEST RUN")
    print("=" * 70)
    
    # Step 1: Generate test data
    print("\n[STEP 1/5] GENERATING SYNTHETIC DATA\n")
    generate_synthetic_data()
    
    # Step 2: Preprocessing
    print("\n[STEP 2/5] PREPROCESSING AND FEATURE ENGINEERING\n")
    preprocessor = DataPreprocessor(raw_data_dir="data/raw", 
                                   processed_data_dir="data/processed")
    df_processed, sample_rows = preprocessor.process()
    
    # Step 3: Model Training
    print("\n[STEP 3/5] TRAINING REGRESSION MODELS\n")
    regressor = TemperatureRegressor(
        processed_data_path="data/processed/climate_data_processed.csv",
        output_dir="models"
    )
    model_data = regressor.train_all_models()
    
    # Step 4: Visualization
    print("\n[STEP 4/5] CREATING VISUALIZATIONS\n")
    plotter = ClimatePlotter(output_dir="reports/figures")
    
    try:
        print("\nGenerating data trend plots...")
        plotter.plot_greenhouse_gas_trends(df_processed)
        plotter.plot_temperature_vs_co2(df_processed)
        plotter.plot_time_series_comparison(df_processed)
        
        print("Generating model evaluation plots...")
        plotter.plot_feature_importance(model_data['feature_importances'])
        plotter.plot_model_comparison(model_data['results'])
        
        print("Generating residual diagnostics...")
        for model_name, model in model_data['models'].items():
            y_pred = model.predict(model_data['X_test'])
            plotter.plot_residuals(model_data['y_test'], y_pred, model_name)
    except Exception as e:
        print(f"  Warning: Visualization error: {e}")
    
    # Step 5: Report
    print("\n[STEP 5/5] GENERATING REPORT\n")
    generate_test_report(df_processed, model_data, sample_rows)
    
    print("\n" + "=" * 70)
    print("TEST RUN COMPLETE!")
    print("=" * 70)
    print("\nGenerated artifacts:")
    print("  ✓ data/raw/ - Raw datasets")
    print("  ✓ data/processed/ - Processed dataset")
    print("  ✓ models/ - Model results")
    print("  ✓ reports/figures/ - Visualizations")
    print("  ✓ reports/TEST_REPORT.md - Analysis report")
    print("\n" + "=" * 70 + "\n")


def generate_test_report(df, model_data, samples):
    """Generate test analysis report."""
    os.makedirs("reports", exist_ok=True)
    
    with open("reports/TEST_REPORT.md", 'w') as f:
        f.write("# Climate Analysis - Test Report (Synthetic Data)\n\n")
        f.write("## Overview\n")
        f.write("This report demonstrates the complete climate analysis pipeline using synthetic data.\n\n")
        
        f.write("## Dataset\n")
        f.write(f"- **Records**: {len(df)}\n")
        f.write(f"- **Features**: {df.shape[1]}\n")
        f.write(f"- **Time Range**: {df['year'].min():.0f} - {df['year'].max():.0f}\n\n")
        
        f.write("## Sample Data\n```\n")
        f.write(samples.to_string())
        f.write("\n```\n\n")
        
        f.write("## Model Performance\n")
        for name, results in model_data['results'].items():
            f.write(f"### {name.title()}\n")
            f.write(f"- R²: {results['r2_score']:.4f}\n")
            f.write(f"- RMSE: {results['rmse']:.6f}\n")
            f.write(f"- MAE: {results['mae']:.6f}\n\n")
        
        f.write("## Feature Importance (Top 10 - Linear Model)\n")
        if model_data['feature_importances']['linear']:
            for i, (feat, imp) in enumerate(list(model_data['feature_importances']['linear'].items())[:10], 1):
                f.write(f"{i}. {feat} - {imp:.6f}\n")
        f.write("\n")
        
        f.write("## Interpretation\n")
        f.write("This test successfully demonstrates:\n")
        f.write("- Data merging from multiple sources\n")
        f.write("- Feature engineering for climate drivers\n")
        f.write("- Multiple regression model training\n")
        f.write("- Feature importance ranking\n")
        f.write("- Visualization of results\n\n")
        
        f.write("## Next Steps\n")
        f.write("1. Replace synthetic data with real NOAA/NASA/OWID data\n")
        f.write("2. Adjust for actual data quality and coverage\n")
        f.write("3. Validate against published climate analyses\n")
    
    print("✓ Test report generated")


if __name__ == "__main__":
    run_test_pipeline()
