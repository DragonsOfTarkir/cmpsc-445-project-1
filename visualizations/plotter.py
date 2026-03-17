"""
Visualization of climate analysis results
Plots trends, feature importance, and regression relationships
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ClimatePlotter:
    """Create visualizations for climate analysis."""
    
    def __init__(self, output_dir="reports/figures"):
        """Initialize plotter."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
    
    def plot_greenhouse_gas_trends(self, df):
        """Plot CO2, CH4, N2O trends over time."""
        print("Creating greenhouse gas trends plot...")
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        
        # CO2
        if 'CO2_concentration' in df.columns:
            axes[0].plot(df['year'], df['CO2_concentration'], 'b-', linewidth=2)
            axes[0].set_ylabel('CO₂ (ppm)', fontsize=11, fontweight='bold')
            axes[0].set_title('Atmospheric CO₂ Concentration Trend', fontsize=12, fontweight='bold')
            axes[0].grid(True, alpha=0.3)
        
        # CH4
        if 'CH4_concentration' in df.columns:
            axes[1].plot(df['year'], df['CH4_concentration'], 'g-', linewidth=2)
            axes[1].set_ylabel('CH₄ (ppb)', fontsize=11, fontweight='bold')
            axes[1].set_title('Atmospheric CH₄ Concentration Trend', fontsize=12, fontweight='bold')
            axes[1].grid(True, alpha=0.3)
        
        # N2O
        if 'N2O_concentration' in df.columns:
            axes[2].plot(df['year'], df['N2O_concentration'], 'r-', linewidth=2)
            axes[2].set_ylabel('N₂O (ppb)', fontsize=11, fontweight='bold')
            axes[2].set_title('Atmospheric N₂O Concentration Trend', fontsize=12, fontweight='bold')
            axes[2].set_xlabel('Year', fontsize=11, fontweight='bold')
            axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'greenhouse_gas_trends.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  Saved to {output_path}")
        plt.close()
    
    def plot_temperature_vs_co2(self, df):
        """Plot temperature anomaly vs CO2 concentration."""
        print("Creating temperature vs CO2 scatter plot...")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        if 'temperature_anomaly' in df.columns and 'CO2_concentration' in df.columns:
            # Remove NaN values
            mask = df['temperature_anomaly'].notna() & df['CO2_concentration'].notna()
            temp = df.loc[mask, 'temperature_anomaly']
            co2 = df.loc[mask, 'CO2_concentration']
            years = df.loc[mask, 'year']
            
            # Scatter plot colored by year
            scatter = ax.scatter(co2, temp, c=years, cmap='viridis', 
                               s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
            
            # Add trend line
            z = np.polyfit(co2, temp, 2)
            p = np.poly1d(z)
            co2_sorted = np.sort(co2)
            ax.plot(co2_sorted, p(co2_sorted), 'r--', linewidth=3, label='Polynomial trend')
            
            ax.set_xlabel('CO₂ Concentration (ppm)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Temperature Anomaly (°C)', fontsize=12, fontweight='bold')
            ax.set_title('Global Temperature Anomaly vs CO₂ Concentration', 
                        fontsize=13, fontweight='bold')
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Year', fontweight='bold')
            
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'temperature_vs_co2.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  Saved to {output_path}")
        plt.close()
    
    def plot_time_series_comparison(self, df):
        """Plot time series of temperature vs GHGs."""
        print("Creating time series comparison plot...")
        
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        if 'temperature_anomaly' in df.columns and 'CO2_concentration' in df.columns:
            # Temperature on primary y-axis
            color = 'tab:red'
            ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Temperature Anomaly (°C)', color=color, fontsize=11, fontweight='bold')
            line1 = ax1.plot(df['year'], df['temperature_anomaly'], color=color, 
                           linewidth=2.5, label='Temperature Anomaly')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.grid(True, alpha=0.3)
            
            # CO2 on secondary y-axis
            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel('CO₂ Concentration (ppm)', color=color, fontsize=11, fontweight='bold')
            line2 = ax2.plot(df['year'], df['CO2_concentration'], color=color, 
                           linewidth=2.5, label='CO₂', linestyle='--')
            ax2.tick_params(axis='y', labelcolor=color)
            
            # Combined legend
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax1.legend(lines, labels, loc='upper left', fontsize=10)
            
            plt.title('Temperature Anomaly & CO₂ Concentration Trends', 
                     fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'time_series_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  Saved to {output_path}")
        plt.close()
    
    def plot_feature_importance(self, feature_importances):
        """Plot feature importance from models."""
        print("Creating feature importance plots...")
        
        for model_name, importance_dict in feature_importances.items():
            if importance_dict is None:
                continue
            
            # Get top 15 features
            features = list(importance_dict.keys())[:15]
            values = list(importance_dict.values())[:15]
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create color palette
            colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features)))
            
            # Horizontal bar plot
            bars = ax.barh(range(len(features)), values, color=colors, edgecolor='black', linewidth=1)
            ax.set_yticks(range(len(features)))
            ax.set_yticklabels(features, fontsize=10)
            ax.set_xlabel('Importance Score', fontsize=11, fontweight='bold')
            ax.set_title(f'Top Features - {model_name.replace("_", " ").title()}', 
                        fontsize=13, fontweight='bold')
            ax.invert_yaxis()
            
            # Add value labels
            for i, (feature, value) in enumerate(zip(features, values)):
                ax.text(value, i, f' {value:.4f}', va='center', fontsize=9)
            
            plt.tight_layout()
            output_path = os.path.join(self.output_dir, f'feature_importance_{model_name}.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"  Saved to {output_path}")
            plt.close()
    
    def plot_model_comparison(self, results):
        """Plot model performance comparison."""
        print("Creating model comparison plot...")
        
        if not results:
            return
        
        models = list(results.keys())
        metrics = ['r2_score', 'rmse', 'mae']
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for idx, metric in enumerate(metrics):
            values = [results[model].get(metric, 0) for model in models]
            colors = ['#2ecc71', '#3498db', '#e74c3c']
            
            axes[idx].bar(models, values, color=colors, edgecolor='black', linewidth=1.5)
            axes[idx].set_ylabel(metric.replace('_', ' ').title(), fontsize=11, fontweight='bold')
            axes[idx].set_title(f'{metric.upper()} Comparison', fontsize=12, fontweight='bold')
            axes[idx].grid(True, alpha=0.3, axis='y')
            
            # Rotate x labels
            axes[idx].set_xticklabels(models, rotation=15)
            
            # Add value labels on bars
            for i, v in enumerate(values):
                axes[idx].text(i, v, f'{v:.4f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, 'model_comparison.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  Saved to {output_path}")
        plt.close()
    
    def plot_residuals(self, y_test, y_pred, model_name):
        """Plot residuals for a model."""
        residuals = y_test - y_pred
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Residuals vs predicted
        axes[0].scatter(y_pred, residuals, alpha=0.6, edgecolors='black', linewidth=0.5)
        axes[0].axhline(y=0, color='r', linestyle='--', linewidth=2)
        axes[0].set_xlabel('Predicted Values', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Residuals', fontsize=11, fontweight='bold')
        axes[0].set_title(f'{model_name.title()} - Residuals vs Predicted', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Residuals distribution
        axes[1].hist(residuals, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        axes[1].axvline(x=0, color='r', linestyle='--', linewidth=2)
        axes[1].set_xlabel('Residuals', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[1].set_title(f'{model_name.title()} - Residuals Distribution', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f'residuals_{model_name}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  Saved to {output_path}")
        plt.close()


if __name__ == "__main__":
    plotter = ClimatePlotter()
    # This would be called from main analysis
