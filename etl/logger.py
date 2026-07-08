import logging
import os
from datetime import datetime
from etl.config import config

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger that outputs to both console and a log file.
    Returns the configured logger.
    """
    logger = logging.getLogger(name)
    
    # If logger already has handlers, don't add more to avoid duplication
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File Handler
    current_date = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(config.LOG_DIR, f"etl_pipeline_{current_date}.log")
    
    try:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        logger.warning(f"Failed to set up file logging to {log_file}. Error: {e}")
        
    return logger
