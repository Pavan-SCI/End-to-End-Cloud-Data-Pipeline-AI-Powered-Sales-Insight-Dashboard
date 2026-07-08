import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def create_synthetic_data(num_orders=5000):
    np.random.seed(42)
    random.seed(42)
    
    # 1. Customers
    regions = ['North', 'South', 'East', 'West', 'Central']
    segments = ['Consumer', 'Corporate', 'Home Office']
    
    customers = pd.DataFrame({
        'CustomerID': [f'CUST-{i:04d}' for i in range(1, 1001)],
        'CustomerName': [f'Customer {i}' for i in range(1, 1001)],
        'Region': np.random.choice(regions, 1000),
        'Segment': np.random.choice(segments, 1000, p=[0.6, 0.3, 0.1])
    })
    
    # 2. Products
    categories = ['Technology', 'Furniture', 'Office Supplies']
    sub_categories = {
        'Technology': ['Phones', 'Accessories', 'Machines', 'Copiers'],
        'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
        'Office Supplies': ['Binders', 'Paper', 'Art', 'Envelopes', 'Fasteners']
    }
    
    products_list = []
    for i in range(1, 201):
        cat = random.choice(categories)
        sub_cat = random.choice(sub_categories[cat])
        base_price = round(random.uniform(10, 1000), 2)
        products_list.append({
            'ProductID': f'PROD-{i:04d}',
            'Category': cat,
            'SubCategory': sub_cat,
            'ProductName': f'{sub_cat} Model {i}',
            'UnitCost': round(base_price * random.uniform(0.3, 0.6), 2),
            'UnitPrice': base_price
        })
    products = pd.DataFrame(products_list)
    
    # 3. Orders (Sales)
    start_date = datetime(2023, 1, 1)
    orders_list = []
    
    for i in range(1, num_orders + 1):
        order_date = start_date + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        cust = customers.sample(1).iloc[0]
        prod = products.sample(1).iloc[0]
        qty = random.randint(1, 10)
        
        # Calculate revenue and profit
        sales = round(qty * prod['UnitPrice'], 2)
        discount = round(random.choice([0, 0.05, 0.1, 0.2]), 2)
        net_sales = round(sales * (1 - discount), 2)
        cost = round(qty * prod['UnitCost'], 2)
        profit = round(net_sales - cost, 2)
        
        orders_list.append({
            'OrderID': f'ORD-{i:06d}',
            'OrderDate': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'ShippingDate': ship_date.strftime('%Y-%m-%d %H:%M:%S'),
            'CustomerID': cust['CustomerID'],
            'ProductID': prod['ProductID'],
            'Quantity': qty,
            'Discount': discount,
            'Sales': net_sales,
            'Profit': profit
        })
    orders = pd.DataFrame(orders_list)
    
    # 4. Customer Reviews
    review_templates = {
        'Positive': ["Great product!", "Highly recommend.", "Excellent quality.", "Fast shipping and good value."],
        'Neutral': ["It's okay.", "Met expectations.", "Average quality.", "Nothing special."],
        'Negative': ["Poor quality.", "Arrived broken.", "Do not buy.", "Terrible customer service."]
    }
    
    reviews_list = []
    # Generate reviews for about 30% of orders
    review_orders = orders.sample(frac=0.3)
    for _, row in review_orders.iterrows():
        # Tie review sentiment somewhat to profit/discount or completely random
        sentiment_prob = random.random()
        if sentiment_prob > 0.6:
            sentiment = 'Positive'
            score = random.randint(4, 5)
        elif sentiment_prob > 0.2:
            sentiment = 'Neutral'
            score = 3
        else:
            sentiment = 'Negative'
            score = random.randint(1, 2)
            
        reviews_list.append({
            'ReviewID': f'REV-{row["OrderID"]}',
            'OrderID': row['OrderID'],
            'ProductID': row['ProductID'],
            'ReviewScore': score,
            'ReviewText': random.choice(review_templates[sentiment])
        })
    reviews = pd.DataFrame(reviews_list)
    
    # Save to CSV
    os.makedirs('data/raw', exist_ok=True)
    customers.to_csv('data/raw/customers.csv', index=False)
    products.to_csv('data/raw/products.csv', index=False)
    orders.to_csv('data/raw/orders.csv', index=False)
    reviews.to_csv('data/raw/reviews.csv', index=False)
    
    print("Synthetic data generated successfully in 'data/raw' directory.")

if __name__ == "__main__":
    create_synthetic_data()
