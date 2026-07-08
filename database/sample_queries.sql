-- =========================================================================
-- Sample Analytical Queries for Validation
-- =========================================================================

-- 1. Top 5 Most Profitable Customers
SELECT TOP 5
    CustomerID,
    CustomerName,
    LifetimeRevenue,
    LifetimeProfit
FROM VW_Customer_Lifetime_Value
ORDER BY LifetimeProfit DESC;

-- 2. Year-over-Year Sales Growth (Using Window Functions)
WITH YearlySales AS (
    SELECT 
        OrderYear, 
        SUM(TotalRevenue) AS Revenue
    FROM VW_Executive_Summary
    GROUP BY OrderYear
)
SELECT 
    OrderYear,
    Revenue,
    LAG(Revenue) OVER (ORDER BY OrderYear) AS PrevYearRevenue,
    ((Revenue - LAG(Revenue) OVER (ORDER BY OrderYear)) / LAG(Revenue) OVER (ORDER BY OrderYear)) * 100 AS YoY_Growth_Pct
FROM YearlySales;

-- 3. Worst Performing Products (Negative Profit)
SELECT TOP 10
    ProductName,
    Category,
    TotalRevenue,
    TotalProfit
FROM VW_Product_Performance
WHERE TotalProfit < 0
ORDER BY TotalProfit ASC;

-- 4. Average Shipping Time by Region
SELECT 
    c.Region,
    AVG(CAST(s.ShippingDurationDays AS FLOAT)) AS AvgShippingDays
FROM Fact_Sales s
JOIN Dim_Customer c ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY AvgShippingDays DESC;

-- 5. Customer Sentiment Distribution by Category
SELECT 
    Category,
    SentimentLabel,
    COUNT(ReviewID) AS ReviewCount
FROM VW_AI_Sentiment_Insights
GROUP BY Category, SentimentLabel
ORDER BY Category, ReviewCount DESC;
