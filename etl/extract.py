import pandas as pd
import os
from etl.logger import setup_logger
from etl.config import config

logger = setup_logger(__name__)

def read_csv_safe(file_path: str) -> pd.DataFrame:
    """
    Safely reads a CSV file with automatic encoding detection fallback.
    """
    if not os.path.exists(file_path):
        logger.error(f"Missing file: {file_path}")
        raise FileNotFoundError(f"Missing file: {file_path}")
        
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        logger.info(f"Successfully read {file_path} (Shape: {df.shape})")
        return df
    except UnicodeDecodeError:
        logger.warning(f"UTF-8 decode failed for {file_path}. Trying ISO-8859-1...")
        try:
            df = pd.read_csv(file_path, encoding='iso-8859-1')
            logger.info(f"Successfully read {file_path} using ISO-8859-1")
            return df
        except Exception as e:
            logger.error(f"Failed to read {file_path}. Error: {e}")
            raise
    except Exception as e:
        logger.error(f"Unexpected error reading {file_path}. Error: {e}")
        raise

def extract_data() -> dict:
    """
    Extracts all raw CSV files required for the pipeline.
    Returns a dictionary of DataFrames.
    """
    logger.info("Starting data extraction phase...")
    
    raw_data = {}
    files_to_extract = {
        'customers': 'customers.csv',
        'products': 'products.csv',
        'orders': 'orders.csv',
        'reviews': 'reviews.csv'
    }
    
    for key, filename in files_to_extract.items():
        file_path = os.path.join(config.RAW_DIR, filename)
        raw_data[key] = read_csv_safe(file_path)
        
    logger.info("Data extraction phase completed successfully.")
    return raw_data
