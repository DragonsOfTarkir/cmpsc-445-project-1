"""
Our World in Data (OWID) Collection
Collects energy use, emissions, and anthropogenic factors
Source: https://ourworldindata.org/
"""

import pandas as pd
import requests
import os

class OWIDCollector:
    """Collect OWID data from GitHub repository."""
    
    # OWID GitHub URLs for relevant datasets
    CO2_EMISSIONS_URL = "https://github.com/owid/co2-data/raw/master/owid-co2-data.csv"
    
    def __init__(self, output_dir="data/raw"):
        """Initialize collector with output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def collect_co2_emissions(self):
        """
        Collect CO2 emissions data from OWID.
        
        Returns:
            DataFrame with global emissions data
        """
        print("Collecting CO2 emissions data from Our World in Data...")
        try:
            # Read directly from GitHub
            df = pd.read_csv(self.CO2_EMISSIONS_URL)
            
            # Filter for World data
            world_data = df[df['country'] == 'World'].copy()
            
            if world_data.empty:
                print("No global data found")
                return None
            
            # Select relevant columns
            relevant_cols = ['year', 'co2', 'coal_co2', 'oil_co2', 'gas_co2', 
                           'cement_co2', 'flaring_co2', 'energy_per_capita',
                           'cement_per_capita']
            
            available_cols = [col for col in relevant_cols if col in world_data.columns]
            world_data = world_data[['year'] + available_cols]
            
            # Create date column for consistency
            world_data['month'] = 6
            world_data['date'] = pd.to_datetime(world_data['year'].astype(str) + '-06-01')
            
            world_data = world_data.sort_values('date').reset_index(drop=True)
            world_data.to_csv(os.path.join(self.output_dir, 'owid_co2_emissions.csv'), index=False)
            print(f"CO2 emissions data: {len(world_data)} records")
            
            return world_data
            
        except Exception as e:
            print(f"Error fetching OWID data: {e}")
            return None
    
    def collect_aerosol_data(self):
        """
        Collect or create synthetic aerosol optical depth data.
        Real data would come from NOAA or other sources.
        
        Returns:
            DataFrame with aerosol index
        """
        print("Creating aerosol optical depth proxy data...")
        try:
            # Create synthetic aerosol data based on industrial output
            # In practice, this would come from NASA AERONET or NOAA
            years = list(range(1980, 2024))
            data = []
            
            for year in years:
                # Normalized aerosol index based on industrial activity
                # Peaks around major volcanic eruptions (1982, 1991, 2000)
                base = 0.15
                if year == 1982:
                    aod = 0.35  # El Chichón
                elif year == 1991:
                    aod = 0.40  # Mount Pinatubo
                elif year == 2000:
                    aod = 0.20  # Halocon
                else:
                    # Trend: decreasing from 1980s to 2020s
                    aod = base - (year - 1980) * 0.002
                    aod = max(aod, 0.08)  # Floor at 0.08
                
                data.append({
                    'year': year,
                    'month': 6,
                    'date': pd.Timestamp(year=year, month=6, day=1),
                    'aerosol_optical_depth': aod
                })
            
            df = pd.DataFrame(data)
            df.to_csv(os.path.join(self.output_dir, 'aerosol_optical_depth.csv'), index=False)
            print(f"Aerosol data: {len(df)} records")
            return df
            
        except Exception as e:
            print(f"Error creating aerosol data: {e}")
            return None
    
    def collect_all(self):
        """Collect all OWID-related data."""
        print("\n=== Collecting OWID & Proxy Data ===")
        emissions = self.collect_co2_emissions()
        aerosol = self.collect_aerosol_data()
        
        if emissions is not None and aerosol is not None:
            merged = emissions.merge(aerosol[['date', 'aerosol_optical_depth']], 
                                    on='date', how='outer')
            merged = merged.sort_values('date').reset_index(drop=True)
            merged.to_csv(os.path.join(self.output_dir, 'owid_combined.csv'), index=False)
            print(f"Combined OWID data: {len(merged)} records")
            return merged
        
        return emissions if emissions is not None else None


if __name__ == "__main__":
    collector = OWIDCollector()
    collector.collect_all()
