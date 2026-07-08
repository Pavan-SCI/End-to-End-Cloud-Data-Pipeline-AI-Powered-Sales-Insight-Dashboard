# Power BI DAX Measures

Below are the core DAX measures required for the Executive Dashboard. 
Create these inside Power BI Desktop under a dedicated `_Measures` table.

### 1. High-Level KPIs
```dax
Total Sales = SUM(Fact_Sales[Sales])
```
```dax
Total Profit = SUM(Fact_Sales[Profit])
```
```dax
Total Orders = DISTINCTCOUNT(Fact_Sales[OrderID])
```
```dax
Total Customers = DISTINCTCOUNT(Fact_Sales[CustomerID])
```
```dax
Average Order Value (AOV) = DIVIDE([Total Sales], [Total Orders], 0)
```
```dax
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)
```

### 2. Time Intelligence (YoY & MoM)
*Note: Requires a marked Date Table connected to Fact_Sales[OrderDate].*
```dax
Sales Last Year = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Dim_Date'[Date]))
```
```dax
Sales YoY Growth % = 
VAR SalesDiff = [Total Sales] - [Sales Last Year]
RETURN DIVIDE(SalesDiff, [Sales Last Year], 0)
```

### 3. Customer Insights
```dax
Customer Lifetime Value (Avg) = DIVIDE([Total Sales], [Total Customers], 0)
```
```dax
Repeat Customer Rate = 
VAR CustomersWithMultipleOrders = 
    CALCULATE(
        DISTINCTCOUNT(Fact_Sales[CustomerID]),
        FILTER(
            SUMMARIZE(Fact_Sales, Fact_Sales[CustomerID], "OrderCount", DISTINCTCOUNT(Fact_Sales[OrderID])),
            [OrderCount] > 1
        )
    )
RETURN DIVIDE(CustomersWithMultipleOrders, [Total Customers], 0)
```

### 4. AI Sentiment Insights
```dax
Positive Sentiment % = 
DIVIDE(
    CALCULATE(COUNT(Fact_Reviews[ReviewID]), Fact_Reviews[SentimentLabel] = "Positive"),
    COUNT(Fact_Reviews[ReviewID]),
    0
)
```
```dax
Average Review Score = AVERAGE(Fact_Reviews[ReviewScore])
```
