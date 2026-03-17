"""
NASA GISS Surface Temperature Analysis Data Collection
Collects global temperature anomaly data and solar irradiance
Sources: 
- https://data.giss.nasa.gov/gistemp/
- https://www.ncei.noaa.gov/data/total-solar-irradiance/access/
"""

import pandas as pd
import requests
import os

class NASACollector:
    """Collect temperature anomaly and solar irradiance data from NASA."""
    
    # NASA GISS temperature anomaly URL
    TEMP_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.txt"
    
    # NOAA Solar Irradiance URL
    SOLAR_URL = "https://www.ncei.noaa.gov/data/total-solar-irradiance/access/1701/tim_c22_annual.txt"
    
    def __init__(self, output_dir="data/raw"):
        """Initialize collector with output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def collect_temperature_anomaly(self):
        """
        Collect global surface temperature anomaly data from NASA GISS.
        
        Returns:
            DataFrame with year, month, and temperature anomaly
        """
        print("Collecting temperature anomaly data from NASA GISS...")
        try:
            response = requests.get(self.TEMP_URL, timeout=10)
            response.raise_for_status()
            
            lines = response.text.split('\n')
            # Skip header lines until we find the data
            data_start = None
            for i, line in enumerate(lines):
                if line.strip().startswith('Year'):
                    data_start = i + 1
                    break
            
            if data_start is None:
                print("Could not find data header")
                return None
            
            data = []
            for line in lines[data_start:]:
                if not line.strip():
                    continue
                parts = line.split()
                try:
                    year = int(parts[0])
                    # NASA provides monthly anomalies, we'll average them
                    # Format: Year Jan Feb Mar ... Dec D-J-F M-A-M J-J-A S-O-N
                    monthly_values = []
                    for month_idx in range(1, 13):
                        try:
                            val = float(parts[month_idx])
                            if val != 999.99:  # Missing value flag
                                monthly_values.append(val)
                        except (ValueError, IndexError):
                            continue
                    
                    if monthly_values:
                        annual_anomaly = sum(monthly_values) / len(monthly_values)
                        data.append({
                            'year': year,
                            'month': 6,  # Use mid-year
                            'date': pd.Timestamp(year=year, month=6, day=1),
                            'temperature_anomaly': annual_anomaly
                        })
                except (ValueError, IndexError):
                    continue
            
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values('date').reset_index(drop=True)
                df.to_csv(os.path.join(self.output_dir, 'nasa_temp_anomaly.csv'), index=False)
                print(f"Temperature anomaly data: {len(df)} records")
                return df
            
        except Exception as e:
            print(f"Error fetching temperature data: {e}")
        
        return None
    
    def collect_solar_irradiance(self):
        """
        Collect total solar irradiance data.
        
        Returns:
            DataFrame with year and solar irradiance
        """
        print("Collecting solar irradiance data...")
        try:
            # Using NOAA solar irradiance data
            response = requests.get(self.SOLAR_URL, timeout=10)
            response.raise_for_status()
            
            lines = response.text.split('\n')
            data = []
            
            for line in lines:
                if line.strip() and not line.startswith(';') and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            year = int(parts[0])
                            irradiance = float(parts[1])
                            data.append({
                                'year': year,
                                'month': 6,
                                'date': pd.Timestamp(year=year, month=6, day=1),
                                'solar_irradiance': irradiance
                            })
                        except (ValueError, IndexError):
                            continue
            
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values('date').reset_index(drop=True)
                df.to_csv(os.path.join(self.output_dir, 'solar_irradiance.csv'), index=False)
                print(f"Solar irradiance data: {len(df)} records")
                return df
            
        except Exception as e:
            print(f"Error fetching solar irradiance data: {e}")
        
        return None
    
    def collect_all(self):
        """Collect all NASA data."""
        print("\n=== Collecting NASA Data ===")
        temp = self.collect_temperature_anomaly()
        solar = self.collect_solar_irradiance()
        
        if temp is not None and solar is not None:
            merged = temp.merge(solar[['date', 'solar_irradiance']], on='date', how='outer')
            merged = merged.sort_values('date').reset_index(drop=True)
            merged.to_csv(os.path.join(self.output_dir, 'nasa_combined.csv'), index=False)
            print(f"Combined NASA data: {len(merged)} records")
            return merged
        
        return temp if temp is not None else None


if __name__ == "__main__":
    collector = NASACollector()
    collector.collect_all()
