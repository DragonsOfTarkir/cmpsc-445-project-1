"""
NOAA Global Monitoring Laboratory Data Collection
Collects atmospheric greenhouse gas data (CO2, CH4, N2O)
Source: https://gml.noaa.gov/ccgg/trends/
"""

import pandas as pd
import requests
from io import StringIO
import os

class NOAACollector:
    """Collect greenhouse gas data from NOAA."""
    
    # NOAA data URLs
    CO2_URL = "https://gml.noaa.gov/webdata/ccgg/CO2/monthly/co2_mm_mlo.txt"
    CH4_URL = "https://gml.noaa.gov/webdata/ccgg/CH4/monthly/ch4_mm_gl.txt"
    N2O_URL = "https://gml.noaa.gov/webdata/ccgg/N2O/monthly/n2o_mm_gl.txt"
    
    def __init__(self, output_dir="data/raw"):
        """Initialize collector with output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _parse_noaa_txt(self, url, gas_name):
        """
        Parse NOAA text file format.
        
        Args:
            url: URL to NOAA data file
            gas_name: Name of the gas (CO2, CH4, N2O)
            
        Returns:
            DataFrame with year, month, and gas concentration
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            lines = response.text.split('\n')
            data_lines = [line for line in lines if line.strip() and not line.startswith('#')]
            
            data = []
            for line in data_lines:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        year = int(parts[0])
                        month = int(parts[1])
                        value = float(parts[2])
                        data.append({
                            'year': year,
                            'month': month,
                            'date': pd.Timestamp(year=year, month=month, day=1),
                            f'{gas_name}_concentration': value
                        })
                    except (ValueError, IndexError):
                        continue
            
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error fetching {gas_name} data: {e}")
            return None
    
    def collect_co2(self):
        """Collect CO2 data."""
        print("Collecting CO2 data from NOAA...")
        df = self._parse_noaa_txt(self.CO2_URL, 'CO2')
        if df is not None:
            df.to_csv(os.path.join(self.output_dir, 'noaa_co2.csv'), index=False)
            print(f"CO2 data: {len(df)} records")
            return df
        return None
    
    def collect_ch4(self):
        """Collect CH4 data."""
        print("Collecting CH4 data from NOAA...")
        df = self._parse_noaa_txt(self.CH4_URL, 'CH4')
        if df is not None:
            df.to_csv(os.path.join(self.output_dir, 'noaa_ch4.csv'), index=False)
            print(f"CH4 data: {len(df)} records")
            return df
        return None
    
    def collect_n2o(self):
        """Collect N2O data."""
        print("Collecting N2O data from NOAA...")
        df = self._parse_noaa_txt(self.N2O_URL, 'N2O')
        if df is not None:
            df.to_csv(os.path.join(self.output_dir, 'noaa_n2o.csv'), index=False)
            print(f"N2O data: {len(df)} records")
            return df
        return None
    
    def collect_all(self):
        """Collect all NOAA greenhouse gas data."""
        print("\n=== Collecting NOAA Data ===")
        co2 = self.collect_co2()
        ch4 = self.collect_ch4()
        n2o = self.collect_n2o()
        
        # Merge on date
        if co2 is not None and ch4 is not None and n2o is not None:
            merged = co2.merge(ch4[['date', 'CH4_concentration']], on='date', how='outer')
            merged = merged.merge(n2o[['date', 'N2O_concentration']], on='date', how='outer')
            merged = merged.sort_values('date').reset_index(drop=True)
            merged.to_csv(os.path.join(self.output_dir, 'noaa_combined.csv'), index=False)
            print(f"Combined NOAA data: {len(merged)} records")
            return merged
        return None


if __name__ == "__main__":
    collector = NOAACollector()
    collector.collect_all()
