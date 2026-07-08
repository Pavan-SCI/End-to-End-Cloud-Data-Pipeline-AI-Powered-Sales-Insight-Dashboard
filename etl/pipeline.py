import sys
import time
from etl.logger import setup_logger
from etl.extract import extract_data
from etl.transform import transform_data
from etl.validation import run_validations
from etl.load import load_data
from ai.sentiment_analysis import apply_sentiment_analysis

logger = setup_logger(__name__)

def run_pipeline():
    """
    Main entry point for the ETL Pipeline.
    Executes Extract, Transform, Validate, AI Enrichment, and Load steps.
    """
    start_time = time.time()
    logger.info("="*50)
    logger.info("Starting Cloud Data Pipeline")
    logger.info("="*50)
    
    try:
        # Step 1: Extract
        raw_data = extract_data()
        
        # Step 2: Transform
        processed_data = transform_data(raw_data)
        
        # Step 3: Validate
        is_valid = run_validations(processed_data)
        if not is_valid:
            logger.error("Pipeline aborted due to validation failures.")
            sys.exit(1)
            
        # Step 4: AI Enrichment (Sentiment Analysis on Reviews)
        if 'Fact_Reviews' in processed_data:
            processed_data['Fact_Reviews'] = apply_sentiment_analysis(processed_data['Fact_Reviews'])
            
        # Step 5: Load
        load_success = load_data(processed_data)
        if not load_success:
            logger.error("Pipeline encountered errors during the Load phase.")
            sys.exit(1)
            
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        logger.info(f"Pipeline completed successfully in {duration} seconds.")
        
    except Exception as e:
        logger.critical(f"Pipeline failed with unhandled exception: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
