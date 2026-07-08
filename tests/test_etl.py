import pytest
import pandas as pd
from etl.transform import transform_customers, transform_orders
from etl.validation import run_validations

@pytest.fixture
def sample_customer_data():
    return pd.DataFrame({
        'CustomerID': ['CUST-001', 'CUST-002', 'CUST-001'],
        'CustomerName': [' John Doe ', 'Jane Smith', 'John Doe'],
        'Region': ['North', None, 'North'],
        'Segment': ['Consumer', 'Corporate', 'Consumer']
    })

@pytest.fixture
def sample_sales_data():
    return pd.DataFrame({
        'OrderID': ['ORD-001', 'ORD-002'],
        'OrderDate': ['2023-01-01', '2023-01-02'],
        'ShippingDate': ['2023-01-05', '2023-01-03'],
        'CustomerID': ['CUST-001', 'CUST-002'],
        'ProductID': ['PROD-001', 'PROD-002'],
        'Quantity': [2, 1],
        'Discount': [0, 0.1],
        'Sales': [100.0, 50.0],
        'Profit': [20.0, -5.0]
    })

def test_transform_customers(sample_customer_data):
    df = transform_customers(sample_customer_data)
    
    assert len(df) == 2, "Duplicate CustomerID should be dropped."
    assert df.iloc[0]['CustomerName'] == 'John Doe', "Names should be stripped and title cased."
    assert df.iloc[1]['Region'] == 'Unknown', "Null regions should be filled with 'Unknown'."

def test_transform_orders(sample_sales_data):
    df = transform_orders(sample_sales_data)
    
    assert 'ShippingDurationDays' in df.columns
    assert df.iloc[0]['ShippingDurationDays'] == 4
    assert df.iloc[1]['ShippingDurationDays'] == 1
    
    assert 'ProfitMargin' in df.columns
    assert df.iloc[0]['ProfitMargin'] == 20.0
    assert df.iloc[1]['ProfitMargin'] == -10.0

def test_run_validations_missing_customer():
    customers = pd.DataFrame({'CustomerID': ['CUST-001']})
    products = pd.DataFrame({'ProductID': ['PROD-001']})
    sales = pd.DataFrame({'CustomerID': ['CUST-009'], 'ProductID': ['PROD-001'], 'Sales': [100]})
    
    processed_data = {
        'Dim_Customer': customers,
        'Dim_Product': products,
        'Fact_Sales': sales
    }
    
    is_valid = run_validations(processed_data)
    assert is_valid == False, "Validation should fail for orphan sales records."
