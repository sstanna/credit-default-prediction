import pandas as pd
import numpy as np
import requests
import os
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_data(url: str, output_path: str) -> None:
    """Download data from URL to local path."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Data downloaded successfully to {output_path}")
    except Exception as e:
        logger.error(f"Error downloading data: {e}")
        raise

def load_raw_data(data_path: str) -> pd.DataFrame:
    """Load raw data from file."""
    try:
        # UCI Credit Card Default dataset
        df = pd.read_excel(data_path, header=1)
        
        # Remove the first column (ID) as it's not needed
        df = df.drop(df.columns[0], axis=1)
        
        logger.info(f"Raw data loaded: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading raw data: {e}")
        raise

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the raw data."""
    df_clean = df.copy()
    
    # Rename target column for clarity
    df_clean = df_clean.rename(columns={'default.payment.next.month': 'default_payment'})
    
    # Handle missing values
    df_clean = df_clean.fillna(0)
    
    # Convert categorical variables
    df_clean['SEX'] = df_clean['SEX'].astype('category')
    df_clean['EDUCATION'] = df_clean['EDUCATION'].astype('category')
    df_clean['MARRIAGE'] = df_clean['MARRIAGE'].astype('category')
    
    logger.info(f"Data cleaned: {df_clean.shape}")
    return df_clean

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create additional features through feature engineering."""
    df_features = df.copy()
    
    # Payment behavior features
    payment_cols = [f'PAY_{i}' for i in range(0, 6)]
    bill_cols = [f'BILL_AMT{i}' for i in range(1, 7)]
    
    # Average payment delay
    df_features['avg_payment_delay'] = df_features[payment_cols].mean(axis=1)
    
    # Average bill amount
    df_features['avg_bill_amount'] = df_features[bill_cols].mean(axis=1)
    
    # Credit utilization ratio (simplified)
    df_features['credit_utilization'] = df_features['avg_bill_amount'] / (df_features['LIMIT_BAL'] + 1)
    
    # Age bins
    df_features['age_group'] = pd.cut(df_features['AGE'], 
                                    bins=[0, 25, 35, 45, 55, 100], 
                                    labels=['young', 'adult', 'middle', 'senior', 'elderly'])
    
    # Payment consistency (how often payments are on time)
    df_features['payment_consistency'] = (df_features[payment_cols] <= 0).sum(axis=1) / len(payment_cols)
    
    logger.info(f"Features created: {df_features.shape}")
    return df_features

def prepare_data(data_path: str, output_path: Optional[str] = None) -> pd.DataFrame:
    """Complete data preparation pipeline."""
    logger.info("Starting data preparation...")
    
    # Load raw data
    df_raw = load_raw_data(data_path)
    
    # Clean data
    df_clean = clean_data(df_raw)
    
    # Create features
    df_features = create_features(df_clean)
    
    # Save processed data if output path provided
    if output_path:
        df_features.to_parquet(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")
    
    return df_features

if __name__ == "__main__":
    # Example usage
    data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
    raw_data_path = "data/raw/credit_card_default.xls"
    processed_data_path = "data/processed/credit_card_default.parquet"
    
    # Download data
    download_data(data_url, raw_data_path)
    
    # Prepare data
    df = prepare_data(raw_data_path, processed_data_path)
    
    print(f"Final dataset shape: {df.shape}")
    print(f"Target distribution: {df['default_payment'].value_counts()}")
