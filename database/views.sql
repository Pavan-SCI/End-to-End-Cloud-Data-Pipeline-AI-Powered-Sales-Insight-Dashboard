-- =========================================================================
-- Analytical Views for Power BI & Ad-Hoc Reporting
-- =========================================================================

-- 1. VW_Executive_Summary
-- Provides high-level KPIs aggregated by month and year.
CREATE OR ALTER VIEW VW_Executive_Summary AS
SELECT 
    OrderYear,
    OrderMonth,
    COUNT(DISTINCT OrderID) AS TotalOrders,
    COUNT(DISTINCT CustomerID) AS UniqueCustomers,
    SUM(Sales) AS TotalRevenue,
    SUM(Profit) AS TotalProfit,
    CASE 
        WHEN SUM(Sales) = 0 THEN 0 
        ELSE (SUM(Profit) / SUM(Sales)) * 100 
    END AS OverallProfitMargin
FROM Fact_Sales
GROUP BY OrderYear, OrderMonth;
GO

-- 2. VW_Customer_Lifetime_Value
-- Aggregates total value and profitability per customer.
CREATE OR ALTER VIEW VW_Customer_Lifetime_Value AS
SELECT 
    c.CustomerID,
    c.CustomerName,
    c.Segment,
    c.Region,
    MIN(s.OrderDate) AS FirstPurchaseDate,
    MAX(s.OrderDate) AS LastPurchaseDate,
    COUNT(DISTINCT s.OrderID) AS TotalOrders,
    SUM(s.Sales) AS LifetimeRevenue,
    SUM(s.Profit) AS LifetimeProfit,
    AVG(s.Sales) AS AverageOrderValue
FROM Dim_Customer c
JOIN Fact_Sales s ON c.CustomerID = s.CustomerID
GROUP BY 
    c.CustomerID, c.CustomerName, c.Segment, c.Region;
GO

-- 3. VW_Product_Performance
-- Analyzes sales and profitability at the product level.
CREATE OR ALTER VIEW VW_Product_Performance AS
SELECT 
    p.ProductID,
    p.ProductName,
    p.Category,
    p.SubCategory,
    SUM(s.Quantity) AS TotalUnitsSold,
    SUM(s.Sales) AS TotalRevenue,
    SUM(s.Profit) AS TotalProfit,
    AVG(s.ProfitMargin) AS AvgProfitMargin
FROM Dim_Product p
JOIN Fact_Sales s ON p.ProductID = s.ProductID
GROUP BY 
    p.ProductID, p.ProductName, p.Category, p.SubCategory;
GO

-- 4. VW_AI_Sentiment_Insights
-- Joins product and review data for AI sentiment analysis reporting.
CREATE OR ALTER VIEW VW_AI_Sentiment_Insights AS
SELECT 
    r.ReviewID,
    p.Category,
    p.SubCategory,
    p.ProductName,
    r.ReviewScore,
    r.SentimentLabel,
    r.SentimentPolarity,
    r.ReviewText
FROM Fact_Reviews r
JOIN Dim_Product p ON r.ProductID = p.ProductID;
GO
