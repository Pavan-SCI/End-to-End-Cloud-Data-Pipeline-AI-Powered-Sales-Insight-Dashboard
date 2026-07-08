import pandas as pd
from etl.logger import setup_logger
import os
from etl.config import config

logger = setup_logger(__name__)

def run_validations(processed_data: dict) -> bool:
    """
    Validates data quality before loading to the database.
    Checks for orphan records, negative sales, missing keys, etc.
    Returns True if valid, False otherwise.
    """
    logger.info("Starting validation phase...")
    is_valid = True
    report = []
    
    customers = processed_data['Dim_Customer']
    products = processed_data['Dim_Product']
    sales = processed_data['Fact_Sales']
    
    # 1. Null Keys Check
    if sales['CustomerID'].isnull().any():
        msg = "Validation Error: Null CustomerIDs found in Fact_Sales."
        logger.error(msg)
        report.append(msg)
        is_valid = False
        
    if sales['ProductID'].isnull().any():
        msg = "Validation Error: Null ProductIDs found in Fact_Sales."
        logger.error(msg)
        report.append(msg)
        is_valid = False
        
    # 2. Orphan Records Check (Referential Integrity)
    orphan_customers = sales[~sales['CustomerID'].isin(customers['CustomerID'])]
    if not orphan_customers.empty:
        msg = f"Validation Error: {len(orphan_customers)} orphan Sales records found with unknown CustomerID."
        logger.error(msg)
        report.append(msg)
        is_valid = False
        
    orphan_products = sales[~sales['ProductID'].isin(products['ProductID'])]
    if not orphan_products.empty:
        msg = f"Validation Error: {len(orphan_products)} orphan Sales records found with unknown ProductID."
        logger.error(msg)
        report.append(msg)
        is_valid = False
        
    # 3. Negative Sales Logic Check
    negative_sales = sales[sales['Sales'] < 0]
    if not negative_sales.empty:
        msg = f"Validation Warning: {len(negative_sales)} records found with negative Sales."
        logger.warning(msg)
        report.append(msg) # Warnings don't fail the pipeline natively but logged
        
    # Save Validation Report
    report_path = os.path.join(config.LOG_DIR, "validation_report.txt")
    with open(report_path, "w") as f:
        f.write("Data Quality Validation Report\n")
        f.write("="*30 + "\n")
        if not report:
            f.write("All checks passed successfully.\n")
        else:
            for item in report:
                f.write(item + "\n")
                
    if is_valid:
        logger.info("Data Validation Passed.")
    else:
        logger.error("Data Validation Failed. Check validation_report.txt")
        
    return is_valid
