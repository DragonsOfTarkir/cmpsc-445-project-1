# Code Quality & Documentation

## Module Overview

This document explains the architecture, design decisions, and code organization.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│          main_analysis.py (Orchestrator)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  │ NOAA     │    │ NASA     │    │ OWID     │         │
│  │ Collector│    │ Collector│    │ Collector│         │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘         │
│       │                │                │                │
│       └────────────────┴────────────────┘                │
│                  Data Sources                            │
│                      ↓                                    │
│          Raw CSV files (data/raw/)                       │
│                      ↓                                    │
│  ┌──────────────────────────────────┐                  │
│  │     DataPreprocessor             │                  │
│  │ - Load & merge datasets          │                  │
│  │ - Handle missing values          │                  │
│  │ - Feature engineering            │                  │
│  └──────────────────┬───────────────┘                  │
│                     ↓                                    │
│      Processed CSV (data/processed/)                     │
│                     ↓                                    │
│  ┌──────────────────────────────────┐                  │
│  │   TemperatureRegressor           │                  │
│  │ - Train Linear/RF/XGBoost        │                  │
│  │ - Evaluate models                │                  │
│  │ - Extract feature importance     │                  │
│  └──────────────────┬───────────────┘                  │
│                     ↓                                    │
│       Model results (models/*)                           │
│                     ↓                                    │
│  ┌──────────────────────────────────┐                  │
│  │      ClimatePlotter              │                  │
│  │ - Generate visualizations        │                  │
│  │ - Time series plots              │                  │
│  │ - Feature importance bars        │                  │
│  └──────────────────┬───────────────┘                  │
│                     ↓                                    │
│     PNG files (reports/figures/)                         │
│     Markdown report (reports/)                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Design Patterns

### 1. Data Pipeline Pattern
Each data source (NOAA, NASA, OWID) implements same interface:
```python
collector.collect_all()  # Returns merged DataFrame
```

### 2. Configuration-Driven
Paths and parameters are configurable:
```python
preprocessor = DataPreprocessor(
    raw_data_dir="data/raw",
    processed_data_dir="data/processed"
)
```

### 3. Separation of Concerns
- **Collection**: Fetch and save raw data
- **Preprocessing**: Clean and engineer data
- **Modeling**: Train and evaluate models
- **Visualization**: Generate plots
- **Orchestration**: Coordinate pipeline

## Data Flow

### Step 1: Collection
```
Online Source → Network Request → Parse Response → Save CSV
```
- NOAA: Plain text format with headers
- NASA: Space-formatted columns
- OWID: Standard CSV from GitHub

### Step 2: Preprocessing
```
Raw CSVs → Load → Merge on Date → Fill NAs → Engineer Features → Save Processed CSV
```
Features created:
- Time-based: `years_since_baseline`
- Growth: `CO2_growth_rate`, `CH4_growth_rate`
- Smoothing: 12-month moving averages
- Composite: `GHG_combined` = CO₂ + 25×CH₄

### Step 3: Modeling
```
Processed CSV → Train/Test Split (70/30) → Scale Features → Train Models → Evaluate → Rank Features
```

Models:
- Linear Regression (interpretable coefficients)
- Random Forest (robust feature importance)
- XGBoost (non-linear patterns)

### Step 4: Visualization
```
Processed Data + Model Results → Generate Plots → Save PNGs
```

## Code Quality Standards

### Structure
Each module is self-contained with clear purpose:
```
module/
├── __init__.py          # Package marker
└── processor.py         # Implementation
```

### Documentation
Every class and function has docstrings:
```python
def collect_co2(self):
    """
    Collect CO2 data.
    
    Returns:
        DataFrame with date and CO2_concentration columns
    """
```

### Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except Exception as e:
    print(f"Error: {e}")
    return None
```

### Type Hints (optional but recommended)
```python
def load_data(self) -> pd.DataFrame:
    ...

def prepare_features(self, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    ...
```

### Logging
Throughout the code, informative print statements show progress:
```python
print(f"Loaded {len(df)} records")
print(f"  ✓ Feature created")
```

## Testing Strategy

### Unit Testing (Not Implemented Here)
Would test individual functions:
```python
def test_fill_missing_values():
    df = pd.DataFrame({'value': [1, np.nan, 3]})
    result = preprocessor.fill_missing_values(df)
    assert not result.isnull().any()
```

### Integration Testing
Test full pipeline (use `test_pipeline.py`):
```bash
python test_pipeline.py
```

### Validation
Results validated against:
- Data shape expectations (>1000 samples)
- Feature distributions (reasonable ranges)
- Model metrics (R² visible improvement)
- Visualization output (files created)

## Performance Considerations

### Memory
- **Linear Regression**: ~10 MB for 1000 samples, 50 features
- **Random Forest**: ~100 MB (stores 100 trees)
- **XGBoost**: ~50 MB (efficient storage)

Total: Easily fits in RAM

### Speed
- **Data Collection**: 1-5 minutes (network dependent)
- **Preprocessing**: <1 second
- **Model Training**: 5-10 seconds total
- **Visualization**: 10-20 seconds (saves PNG files)

**Total Pipeline**: ~5-15 minutes

### Optimization Tips
- Use `n_jobs=-1` in RandomForest to parallelize
- XGBoost automatically uses multiple cores
- Visualization is bottleneck (can skip if needed)

## Common Pitfalls & Solutions

### Pitfall 1: Data Alignment Issues
**Problem**: Different data sources have different date ranges
**Solution**: Use `merge(..., how='outer')` then interpolate missing values

### Pitfall 2: Feature Scaling
**Problem**: Linear regression sensitive to feature magnitude
**Solution**: Use StandardScaler before training

### Pitfall 3: Missing Values
**Problem**: NaN values break model training
**Solution**: Interpolate → forward fill → backward fill

### Pitfall 4: Causation vs Correlation
**Problem**: High feature importance ≠ causation
**Solution**: Acknowledge in report, cite climate science consensus

## Extensibility

### Adding New Data Source
1. Create `new_source_data.py` in `data_collection/`
2. Implement `NewCollector` class with `collect_all()` method
3. Return DataFrame with `date` column
4. Import and call in `main_analysis.py`

### Adding New Model
1. Import model from sklearn/xgboost
2. Add training method to `TemperatureRegressor`:
```python
def train_neural_network(self, X_train, y_train):
    from sklearn.neural_network import MLPRegressor
    model = MLPRegressor(...)
    model.fit(X_train, y_train)
    self.models['neural_network'] = model
```
3. Call from `train_all_models()`

### Adding New Visualization
1. Add method to `ClimatePlotter`:
```python
def plot_feature_correlation(self, df):
    # Create plot
    plt.savefig(...)
```
2. Call from `main_analysis.py`

## Dependencies

### Critical
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `scikit-learn`: ML models
- `matplotlib/seaborn`: Plotting
- `requests`: HTTP data fetching

### Optional
- `jupyter`: For interactive analysis
- `xgboost`: Advanced gradient boosting

### Version Compatibility
All packages tested with Python 3.8+
Flexible version constraints (>=X.X) in requirements.txt

## Security Considerations

No sensitive data or authentication needed. All data sources are public.

**Good practices**:
- Validate URLs before fetching
- Set request timeouts (prevents hanging)
- Check response status codes
- Handle network errors gracefully

## Deployment Notes

### For Production Use
1. Add caching to data collection (don't refetch daily)
2. Add scheduler for monthly updates
3. Add database instead of CSV files
4. Add API endpoint for queries
5. Add authentication for restricted access

### For Cloud Deployment
Can run on:
- AWS Lambda (serverless, <15 min runtime)
- Google Colab (free, needs internet)
- Docker container (reproducible)
- GitHub Actions (automated updates)

## Future Enhancements

1. **Statistical Tests**
   - Feature significance tests (p-values)
   - Model comparison (F-tests)
   - Uncertainty quantification

2. **Advanced Methods**
   - Causal inference (instrumental variables)
   - Time series models (ARIMA, Prophet)
   - Neural networks (LSTM, transformer)
   - Ensemble methods (stacking)

3. **Interactivity**
   - Jupyter notebooks for exploration
   - Dash/Streamlit dashboard
   - Interactive SHAP plots

4. **Reproducibility**
   - Seed random states
   - Log all parameters
   - Save model objects
   - Version data snapshots

5. **Validation**
   - Cross-validation (K-fold)
   - Bootstrap confidence intervals
   - Out-of-sample testing
   - Publication bias checks

---

**For questions or improvements**, refer to the main README.md or IMPLEMENTATION_GUIDE.md.
