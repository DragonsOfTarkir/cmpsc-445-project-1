"""
Data Preprocessing and Feature Engineering
Merges all datasets and creates analytical features
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

class DataPreprocessor:
    """Preprocess and engineer features for climate analysis."""
    
    def __init__(self, raw_data_dir="data/raw", processed_data_dir="data/processed"):
        """Initialize preprocessor."""
        self.raw_dir = raw_data_dir
        self.processed_dir = processed_data_dir
        os.makedirs(processed_data_dir, exist_ok=True)
    
    def load_all_data(self):
        """Load all collected datasets."""
        print("Loading all datasets...")
        dfs = {}
        
        # Load NOAA data
        noaa_file = os.path.join(self.raw_dir, 'noaa_combined.csv')
        if os.path.exists(noaa_file):
            dfs['noaa'] = pd.read_csv(noaa_file)
            dfs['noaa']['date'] = pd.to_datetime(dfs['noaa']['date'])
            print(f"  NOAA: {len(dfs['noaa'])} records")
        
        # Load NASA data
        nasa_file = os.path.join(self.raw_dir, 'nasa_combined.csv')
        if os.path.exists(nasa_file):
            dfs['nasa'] = pd.read_csv(nasa_file)
            dfs['nasa']['date'] = pd.to_datetime(dfs['nasa']['date'])
            print(f"  NASA: {len(dfs['nasa'])} records")
        
        # Load OWID data
        owid_file = os.path.join(self.raw_dir, 'owid_combined.csv')
        if os.path.exists(owid_file):
            dfs['owid'] = pd.read_csv(owid_file)
            dfs['owid']['date'] = pd.to_datetime(dfs['owid']['date'])
            print(f"  OWID: {len(dfs['owid'])} records")
        
        return dfs
    
    def merge_datasets(self, dfs):
        """
        Merge all datasets into unified dataset.
        
        Args:
            dfs: Dictionary of dataframes from different sources
            
        Returns:
            Merged DataFrame
        """
        print("\nMerging datasets...")
        
        if not dfs:
            raise ValueError("No datasets loaded")
        
        # Start with the first dataset
        merged = None
        for source, df in dfs.items():
            df_sorted = df.sort_values('date').reset_index(drop=True)
            
            if merged is None:
                merged = df_sorted
            else:
                # Merge on date, keeping all dates (outer join)
                merged = merged.merge(df_sorted, on='date', how='outer', 
                                    suffixes=('', f'_{source}'))
        
        merged = merged.sort_values('date').reset_index(drop=True)
        
        # Drop duplicate columns that may have been created
        merged = merged.loc[:, ~merged.columns.duplicated()]
        
        print(f"Merged dataset: {len(merged)} records, {merged.shape[1]} columns")
        return merged
    
    def fill_missing_values(self, df):
        """
        Fill or handle missing values.
        
        Strategy:
        - Forward fill for time-series data with occasional gaps
        - Interpolate for missing values in between
        - Drop rows with multiple missing values
        """
        print("\nHandling missing values...")
        
        # Interpolate missing values (linear interpolation for time series)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            missing_before = df[col].isna().sum()
            # Interpolate
            df[col] = df[col].interpolate(method='linear', limit_direction='both')
            # Forward fill remaining
            df[col] = df[col].fillna(method='ffill')
            # Back fill remaining
            df[col] = df[col].fillna(method='bfill')
            missing_after = df[col].isna().sum()
            if missing_before > 0:
                print(f"  {col}: {missing_before} -> {missing_after} missing values")
        
        # Drop rows with still-missing critical values
        critical_cols = [col for col in df.columns if 'temperature' in col.lower()]
        if critical_cols:
            df = df.dropna(subset=critical_cols)
        
        return df
    
    def engineer_features(self, df):
        """
        Create new features for analysis.
        
        Engineered features:
        - Time-based features (years since baseline)
        - Growth rates (CO2, CH4 growth)
        - Moving averages
        - Anomalies from baseline
        """
        print("\nEngineering features...")
        
        # Baseline year
        baseline_year = df['year'].min() if 'year' in df.columns else 1980
        
        # Time since baseline
        if 'year' in df.columns:
            df['years_since_baseline'] = df['year'] - baseline_year
        
        # CO2 growth rate (% change from previous year)
        if 'CO2_concentration' in df.columns:
            df['CO2_growth_rate'] = df['CO2_concentration'].pct_change() * 100
        
        # CH4 growth rate
        if 'CH4_concentration' in df.columns:
            df['CH4_growth_rate'] = df['CH4_concentration'].pct_change() * 100
        
        # 12-month moving average for CO2 (smoothing)
        if 'CO2_concentration' in df.columns:
            df['CO2_12m_ma'] = df['CO2_concentration'].rolling(window=12, min_periods=1).mean()
        
        # 12-month moving average for temperature anomaly
        if 'temperature_anomaly' in df.columns:
            df['temp_anomaly_12m_ma'] = df['temperature_anomaly'].rolling(window=12, min_periods=1).mean()
        
        # CO2 + CH4 combined greenhouse gas effect (simple sum)
        if 'CO2_concentration' in df.columns and 'CH4_concentration' in df.columns:
            df['GHG_combined'] = (
                df['CO2_concentration'].fillna(0) + 
                df['CH4_concentration'].fillna(0) * 25  # CH4 GWP relative to CO2
            )
        
        # Normalize solar irradiance to index (1961-1990 = 100)
        if 'solar_irradiance' in df.columns:
            irr_mean = df['solar_irradiance'].mean()
            df['solar_index'] = (df['solar_irradiance'] / irr_mean) * 100
        
        # Anomaly from baseline for CO2
        if 'CO2_concentration' in df.columns:
            co2_baseline = df['CO2_concentration'].iloc[0] if len(df) > 0 else 0
            df['CO2_anomaly'] = df['CO2_concentration'] - co2_baseline
        
        print(f"  Created {df.shape[1] - len(df.columns)} new features")
        return df
    
    def standardize_temporal_format(self, df):
        """Ensure all data is at same temporal resolution (yearly)."""
        print("\nStandardizing temporal resolution to yearly...")
        
        if 'year' not in df.columns and 'date' in df.columns:
            df['year'] = df['date'].dt.year
        
        # Group by year and aggregate
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        agg_dict = {col: 'mean' for col in numeric_cols if col != 'year'}
        df_yearly = df.groupby('year', as_index=False).agg(agg_dict)
        
        print(f"  Aggregated to {len(df_yearly)} yearly records")
        return df_yearly
    
    def get_summary_stats(self, df):
        """Print summary statistics."""
        print("\n=== Dataset Summary Statistics ===")
        print(f"Date range: {df['year'].min():.0f} - {df['year'].max():.0f}")
        print(f"Total records: {len(df)}")
        print(f"Total features: {df.shape[1]}")
        print(f"\nMissing values:\n{df.isna().sum()}")
        print(f"\nFeature statistics:\n{df.describe()}")
    
    def save_processed_data(self, df, filename='climate_data_processed.csv'):
        """Save processed dataset."""
        output_path = os.path.join(self.processed_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"\nProcessed data saved to {output_path}")
        return output_path
    
    def get_sample_rows(self, df, n=3):
        """Get sample rows to demonstrate data quality."""
        print(f"\n=== Sample Rows (first {n}) ===")
        return df.head(n)
    
    def process(self):
        """Run complete preprocessing pipeline."""
        print("=" * 60)
        print("DATA PREPROCESSING PIPELINE")
        print("=" * 60)
        
        # Load data
        dfs = self.load_all_data()
        
        if not dfs:
            print("No data files found. Run data collection first.")
            return None
        
        # Merge
        df = self.merge_datasets(dfs)
        
        # Clean and fill missing values
        df = self.fill_missing_values(df)
        
        # Standardize to yearly
        df = self.standardize_temporal_format(df)
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Ensure date column
        if 'date' not in df.columns:
            df['date'] = pd.to_datetime(df['year'].astype(str) + '-06-01')
        
        # Get stats
        self.get_summary_stats(df)
        samples = self.get_sample_rows(df)
        
        # Save
        self.save_processed_data(df)
        
        print("\n" + "=" * 60)
        print("PREPROCESSING COMPLETE")
        print("=" * 60)
        
        return df, samples


if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    preprocessor.process()
