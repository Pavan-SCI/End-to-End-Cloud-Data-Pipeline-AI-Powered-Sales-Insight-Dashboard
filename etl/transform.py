import pandas as pd
import numpy as np
from etl.logger import setup_logger

logger = setup_logger(__name__)

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform customer dimension."""
    logger.info("Transforming customers...")
    df = df.drop_duplicates(subset=['CustomerID'])
    df['CustomerName'] = df['CustomerName'].str.strip().str.title()
    df.fillna({'Region': 'Unknown', 'Segment': 'Unknown'}, inplace=True)
    return df

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform product dimension."""
    logger.info("Transforming products...")
    df = df.drop_duplicates(subset=['ProductID'])
    df['ProductName'] = df['ProductName'].str.strip()
    df['UnitCost'] = pd.to_numeric(df['UnitCost'], errors='coerce').fillna(0)
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce').fillna(0)
    return df

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform order facts, adding calculated columns."""
    logger.info("Transforming orders...")
    df = df.drop_duplicates(subset=['OrderID'])
    
    # Convert dates
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    df['ShippingDate'] = pd.to_datetime(df['ShippingDate'], errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['OrderDate'])
    
    # Calculated Columns
    df['ShippingDurationDays'] = (df['ShippingDate'] - df['OrderDate']).dt.days
    df['ShippingDurationDays'] = df['ShippingDurationDays'].apply(lambda x: max(0, x)) # Ensure no negative shipping days
    
    # Date Parts for Time Dimension
    df['OrderYear'] = df['OrderDate'].dt.year
    df['OrderMonth'] = df['OrderDate'].dt.month
    df['OrderQuarter'] = df['OrderDate'].dt.quarter
    
    # Handle numeric columns
    numeric_cols = ['Quantity', 'Discount', 'Sales', 'Profit']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    df['ProfitMargin'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    
    return df

def transform_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform reviews."""
    logger.info("Transforming reviews...")
    df = df.drop_duplicates(subset=['ReviewID'])
    df['ReviewText'] = df['ReviewText'].str.strip().fillna('')
    df['ReviewScore'] = pd.to_numeric(df['ReviewScore'], errors='coerce').fillna(3) # Default to neutral 3
    return df

def transform_data(raw_data: dict) -> dict:
    """
    Main transform orchestrator.
    Expects dictionary of raw dataframes and returns transformed dataframes.
    """
    logger.info("Starting data transformation phase...")
    
    processed_data = {}
    
    processed_data['Dim_Customer'] = transform_customers(raw_data['customers'])
    processed_data['Dim_Product'] = transform_products(raw_data['products'])
    processed_data['Fact_Sales'] = transform_orders(raw_data['orders'])
    processed_data['Fact_Reviews'] = transform_reviews(raw_data['reviews'])
    
    logger.info("Data transformation phase completed successfully.")
    return processed_data
