"""
Regression Models for Temperature Anomaly Prediction
Trains and evaluates multiple models to identify important climate drivers
"""

import pandas as pd
import numpy as np
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb

class TemperatureRegressor:
    """Train regression models to predict temperature anomaly."""
    
    def __init__(self, processed_data_path="data/processed/climate_data_processed.csv",
                 output_dir="models"):
        """Initialize regressor."""
        self.data_path = processed_data_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.models = {}
        self.results = {}
        self.feature_names = None
        self.scaler = StandardScaler()
    
    def load_data(self):
        """Load processed climate data."""
        print("Loading processed data...")
        df = pd.read_csv(self.data_path)
        
        print(f"  Loaded {len(df)} records with {df.shape[1]} columns")
        return df
    
    def prepare_features_and_target(self, df):
        """
        Prepare features and target variable.
        
        Target: temperature_anomaly
        Features: all other numerical columns except identifiers
        """
        print("\nPreparing features and target...")
        
        # Identify target variable
        target_col = None
        for col in df.columns:
            if 'temperature' in col.lower() and 'anomaly' in col.lower():
                target_col = col
                break
        
        if target_col is None:
            raise ValueError("No temperature_anomaly column found")
        
        # Remove rows with missing target
        df = df[df[target_col].notna()].copy()
        
        # Select features (numerical, exclude dates and identifiers)
        exclude_cols = {'date', 'year', 'month', target_col}
        feature_cols = [col for col in df.columns 
                       if col not in exclude_cols 
                       and pd.api.types.is_numeric_dtype(df[col])]
        
        # Remove columns with too many NaNs or zero variance
        feature_cols = [col for col in feature_cols 
                       if df[col].notna().sum() > len(df) * 0.5
                       and df[col].std() > 0.001]
        
        X = df[feature_cols].fillna(df[feature_cols].mean()).values
        y = df[target_col].values
        
        self.feature_names = feature_cols
        
        print(f"  Target: {target_col}")
        print(f"  Features ({len(feature_cols)}): {', '.join(feature_cols[:5])}...")
        print(f"  Dataset: {X.shape[0]} samples, {X.shape[1]} features")
        
        return X, y, feature_cols, df
    
    def split_data(self, X, y, test_size=0.3, random_state=42):
        """Split data into train and test sets."""
        print(f"\nSplitting data (70/30 split)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"  Train: {len(X_train)} samples")
        print(f"  Test: {len(X_test)} samples")
        
        return X_train, X_test, y_train, y_test
    
    def scale_features(self, X_train, X_test):
        """Standardize features."""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
    def train_linear_regression(self, X_train, y_train):
        """Train linear regression model."""
        print("\nTraining Linear Regression...")
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.models['linear'] = model
        print("  ✓ Linear Regression trained")
        return model
    
    def train_random_forest(self, X_train, y_train):
        """Train random forest regressor."""
        print("\nTraining Random Forest Regressor...")
        model = RandomForestRegressor(n_estimators=100, random_state=42, 
                                      n_jobs=-1, max_depth=15)
        model.fit(X_train, y_train)
        self.models['random_forest'] = model
        print("  ✓ Random Forest trained")
        return model
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost model."""
        print("\nTraining XGBoost...")
        model = xgb.XGBRegressor(n_estimators=100, random_state=42, 
                               learning_rate=0.1, max_depth=6)
        model.fit(X_train, y_train, verbose=False)
        self.models['xgboost'] = model
        print("  ✓ XGBoost trained")
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance."""
        y_pred = model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results = {
            'model': model_name,
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2_score': float(r2)
        }
        
        self.results[model_name] = results
        
        print(f"\n{model_name.upper()} Results:")
        print(f"  R² Score: {r2:.4f}")
        print(f"  RMSE: {rmse:.6f}")
        print(f"  MAE: {mae:.6f}")
        
        return results
    
    def get_feature_importance(self, model, model_name):
        """Extract feature importance from model."""
        importance = None
        
        if model_name == 'linear':
            # Coefficients for linear regression
            importance = np.abs(model.coef_)
        elif model_name in ['random_forest', 'xgboost']:
            # Feature importances from tree-based models
            importance = model.feature_importances_
        
        if importance is not None:
            # Sort by importance
            importance_dict = dict(zip(self.feature_names, importance))
            sorted_importance = sorted(importance_dict.items(), 
                                      key=lambda x: x[1], reverse=True)
            return sorted_importance
        
        return None
    
    def print_feature_importance(self, model, model_name):
        """Print feature importance."""
        importance = self.get_feature_importance(model, model_name)
        
        if importance is not None:
            print(f"\n{model_name.upper()} - Top 10 Features:")
            for i, (feature, imp) in enumerate(importance[:10], 1):
                print(f"  {i:2d}. {feature:30s} {imp:10.6f}")
            
            return dict(importance)
        
        return None
    
    def save_results(self):
        """Save model results to JSON."""
        output_path = os.path.join(self.output_dir, 'model_results.json')
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {output_path}")
    
    def train_all_models(self):
        """Train all models and evaluate."""
        print("=" * 60)
        print("MODEL TRAINING & EVALUATION")
        print("=" * 60)
        
        # Load and prepare data
        df = self.load_data()
        X, y, feature_cols, df_clean = self.prepare_features_and_target(df)
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        # Train models
        print("\n" + "=" * 60)
        print("TRAINING MODELS")
        print("=" * 60)
        
        # 1. Linear Regression (unscaled)
        lr_model = self.train_linear_regression(X_train, y_train)
        self.evaluate_model(lr_model, X_test, y_test, 'linear')
        lr_importance = self.print_feature_importance(lr_model, 'linear')
        
        # 2. Random Forest (unscaled)
        rf_model = self.train_random_forest(X_train, y_train)
        self.evaluate_model(rf_model, X_test, y_test, 'random_forest')
        rf_importance = self.print_feature_importance(rf_model, 'random_forest')
        
        # 3. XGBoost (unscaled)
        xgb_model = self.train_xgboost(X_train, y_train)
        self.evaluate_model(xgb_model, X_test, y_test, 'xgboost')
        xgb_importance = self.print_feature_importance(xgb_model, 'xgboost')
        
        # Save results
        self.save_results()
        
        # Store feature importance for visualization
        self.feature_importances = {
            'linear': lr_importance,
            'random_forest': rf_importance,
            'xgboost': xgb_importance
        }
        
        print("\n" + "=" * 60)
        print("MODEL TRAINING COMPLETE")
        print("=" * 60)
        
        return {
            'models': self.models,
            'results': self.results,
            'feature_importances': self.feature_importances,
            'feature_names': self.feature_names,
            'X_test': X_test,
            'y_test': y_test
        }


if __name__ == "__main__":
    regressor = TemperatureRegressor()
    regressor.train_all_models()
