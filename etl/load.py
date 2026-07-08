import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from etl.logger import setup_logger
from etl.config import config

logger = setup_logger(__name__)

def get_engine():
    """Creates and returns a SQLAlchemy engine."""
    if not config.SQLALCHEMY_DATABASE_URI:
        logger.warning("No database URI found. Please check .env settings.")
        return None
    try:
        engine = create_engine(
            config.SQLALCHEMY_DATABASE_URI, 
            fast_executemany=True, # Critical for performance with pyodbc
            pool_size=5,
            max_overflow=10
        )
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        return None

def load_table(df: pd.DataFrame, table_name: str, engine, if_exists: str = 'replace') -> bool:
    """Loads a single dataframe to the database."""
    try:
        logger.info(f"Loading {len(df)} rows into table '{table_name}'...")
        # Using transactional load
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                if_exists=if_exists,
                index=False,
                chunksize=5000
            )
        logger.info(f"Successfully loaded '{table_name}'.")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Database error while loading '{table_name}': {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error loading '{table_name}': {e}")
        return False

def load_data(processed_data: dict) -> bool:
    """Orchestrates the loading of all dataframes to the database."""
    logger.info("Starting data load phase...")
    engine = get_engine()
    
    if not engine:
        logger.error("Aborting load phase due to missing database engine.")
        # Fallback to saving as CSV in processed folder if DB is unavailable (useful for purely local testing)
        logger.info("Fallback: Saving processed data locally to CSV...")
        for name, df in processed_data.items():
            df.to_csv(f"{config.PROCESSED_DIR}/{name}.csv", index=False)
        return True # Return true since fallback succeeded

    success = True
    # Order of operations matters for foreign keys if using 'append' instead of 'replace'
    # but since we are doing full replace in this demo, order is slightly less critical
    
    table_mappings = {
        'Dim_Customer': 'Dim_Customer',
        'Dim_Product': 'Dim_Product',
        'Fact_Sales': 'Fact_Sales',
        'Fact_Reviews': 'Fact_Reviews'
    }
    
    for key, table_name in table_mappings.items():
        if key in processed_data:
            result = load_table(processed_data[key], table_name, engine)
            if not result:
                success = False
                
    if success:
        logger.info("Data load phase completed successfully.")
    else:
        logger.error("Data load phase completed with errors.")
        
    return success
