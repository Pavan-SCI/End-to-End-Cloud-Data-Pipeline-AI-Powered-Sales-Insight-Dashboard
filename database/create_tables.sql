-- Use this script to define the schema if not relying on pandas' to_sql for DDL
-- Useful for production deployments to ensure strict data types and constraints

-- 1. Create Schema (Optional based on environment)
-- CREATE SCHEMA sales;
-- GO

-- 2. Drop existing tables if they exist
IF OBJECT_ID('Fact_Reviews', 'U') IS NOT NULL DROP TABLE Fact_Reviews;
IF OBJECT_ID('Fact_Sales', 'U') IS NOT NULL DROP TABLE Fact_Sales;
IF OBJECT_ID('Dim_Product', 'U') IS NOT NULL DROP TABLE Dim_Product;
IF OBJECT_ID('Dim_Customer', 'U') IS NOT NULL DROP TABLE Dim_Customer;

-- 3. Create Dimension Tables
CREATE TABLE Dim_Customer (
    CustomerID VARCHAR(50) PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    Region VARCHAR(100),
    Segment VARCHAR(100)
);

CREATE TABLE Dim_Product (
    ProductID VARCHAR(50) PRIMARY KEY,
    Category VARCHAR(100),
    SubCategory VARCHAR(100),
    ProductName VARCHAR(255) NOT NULL,
    UnitCost DECIMAL(18, 2),
    UnitPrice DECIMAL(18, 2)
);

-- 4. Create Fact Tables
CREATE TABLE Fact_Sales (
    OrderID VARCHAR(50) PRIMARY KEY,
    OrderDate DATETIME NOT NULL,
    ShippingDate DATETIME,
    CustomerID VARCHAR(50) NOT NULL,
    ProductID VARCHAR(50) NOT NULL,
    Quantity INT,
    Discount DECIMAL(5, 2),
    Sales DECIMAL(18, 2),
    Profit DECIMAL(18, 2),
    ShippingDurationDays INT,
    OrderYear INT,
    OrderMonth INT,
    OrderQuarter INT,
    ProfitMargin DECIMAL(10, 2),
    CONSTRAINT FK_Fact_Sales_Customer FOREIGN KEY (CustomerID) REFERENCES Dim_Customer(CustomerID),
    CONSTRAINT FK_Fact_Sales_Product FOREIGN KEY (ProductID) REFERENCES Dim_Product(ProductID)
);

CREATE TABLE Fact_Reviews (
    ReviewID VARCHAR(50) PRIMARY KEY,
    OrderID VARCHAR(50) NOT NULL,
    ProductID VARCHAR(50) NOT NULL,
    ReviewScore INT CHECK (ReviewScore BETWEEN 1 AND 5),
    ReviewText NVARCHAR(MAX),
    SentimentLabel VARCHAR(50),
    SentimentPolarity DECIMAL(5, 2),
    CONSTRAINT FK_Fact_Reviews_Sales FOREIGN KEY (OrderID) REFERENCES Fact_Sales(OrderID),
    CONSTRAINT FK_Fact_Reviews_Product FOREIGN KEY (ProductID) REFERENCES Dim_Product(ProductID)
);

-- 5. Create Indexes for Performance
CREATE INDEX IX_Fact_Sales_OrderDate ON Fact_Sales(OrderDate);
CREATE INDEX IX_Fact_Sales_CustomerID ON Fact_Sales(CustomerID);
CREATE INDEX IX_Fact_Sales_ProductID ON Fact_Sales(ProductID);
CREATE INDEX IX_Dim_Customer_Region ON Dim_Customer(Region);
CREATE INDEX IX_Dim_Product_Category ON Dim_Product(Category);
