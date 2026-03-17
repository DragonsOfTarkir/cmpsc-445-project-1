#!/bin/bash
# Setup and run the climate analysis pipeline

set -e

echo "=========================================="
echo "Climate Analysis Pipeline Setup"
echo "=========================================="
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install pandas numpy scikit-learn xgboost matplotlib seaborn requests scipy jupyter

echo ""
echo "Running analysis pipeline..."
python main_analysis.py

echo ""
echo "=========================================="
echo "Complete! Check reports/ for results"
echo "=========================================="
