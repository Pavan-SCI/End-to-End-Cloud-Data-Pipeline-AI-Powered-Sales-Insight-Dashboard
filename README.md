# End-to-End Cloud Data Pipeline & AI-Powered Sales Insight Dashboard

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Azure SQL](https://img.shields.io/badge/Database-Azure_SQL-0078D4) ![Power BI](https://img.shields.io/badge/Dashboard-Power_BI-F2C811) ![AI](https://img.shields.io/badge/AI-OpenAI_%2F_NLP-green) ![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-black)

## 📌 Project Overview
This project is a comprehensive, production-ready Cloud Data Engineering portfolio piece. It demonstrates the complete lifecycle of data: from extraction and transformation (ETL) of raw CSV files, validation and AI-enrichment, loading into a relational cloud database (Azure SQL), and finally, visualizing the insights through an interactive Power BI Executive Dashboard.

**Ideal for showcasing skills in:** Cloud Data Engineering, Data Analytics, SQL Development, and Python Automation.

## 🏗️ Architecture & Data Flow
![Architecture](docs/architecture.md) *See `docs/architecture.md` for Mermaid diagrams.*

1. **Extract**: Reads raw synthetic sales data (Orders, Customers, Products, Reviews).
2. **Transform**: Cleanses data, handles nulls, calculates new metrics (Profit Margin, Shipping Duration), and structures it into a **Star Schema** (Fact and Dimension tables).
3. **AI Enrichment**: Applies Natural Language Processing (NLP via TextBlob / OpenAI) to customer reviews to determine Sentiment Polarity (Positive, Neutral, Negative).
4. **Validate**: Runs data quality checks (referential integrity, negative logic checks).
5. **Load**: Pushes the cleansed, enriched data to an Azure SQL Database (or local SQL Server) using fast bulk inserts.
6. **Visualize**: Power BI connects to SQL Views to deliver interactive Executive, Customer, Product, and AI insights.

## 🗂️ Folder Structure
```text
project-root/
│
├── ai/                     # AI & NLP integration scripts
├── data/                   # Data generation and raw/processed CSVs
├── database/               # SQL DDL, Views, and Sample Analytical Queries
├── docs/                   # Architecture diagrams and documentation
├── etl/                    # Core Python ETL logic (extract, transform, load, pipeline)
├── powerbi/                # Power BI Theme JSON and DAX measures
├── tests/                  # Pytest unit tests for ETL logic
├── logs/                   # Pipeline execution logs and validation reports
├── .github/workflows/      # CI/CD GitHub Actions pipeline
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # Project documentation
```

## 🚀 Features & Skills Demonstrated
- **Robust ETL Pipeline**: Modular Python scripts with standard error handling, logging, and configuration management.
- **Data Quality & Validation**: Automated checks for orphan records and anomalous values before DB insertion.
- **Relational Data Modeling**: Implementation of a Star Schema design optimized for OLAP analytical queries.
- **Advanced SQL**: Utilization of Stored Procedures, Views, CTEs, Window Functions, and Joins.
- **AI Integration**: Applied NLP sentiment analysis on unstructured text data.
- **CI/CD**: Automated testing and linting via GitHub Actions.
- **Data Visualization**: Clean, executive-level Power BI dashboard design with custom DAX and a cohesive theme.

## 🛠️ Tech Stack
- **Languages**: Python 3.12, SQL, DAX
- **Libraries**: `pandas`, `numpy`, `sqlalchemy`, `pyodbc`, `textblob`, `pytest`, `openai`
- **Database**: Azure SQL Database / Microsoft SQL Server
- **BI Tool**: Power BI Desktop
- **Version Control**: Git & GitHub Actions

## 💻 Installation & Usage

### 1. Clone the repository and setup environment
```bash
git clone https://github.com/yourusername/cloud-data-pipeline.git
cd cloud-data-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file and fill in your database credentials:
```bash
cp .env.example .env
```
*(Edit `.env` with your Azure SQL or local SQL Server details)*

### 3. Generate Synthetic Data
Since real company data is proprietary, this project includes a robust script to generate thousands of realistic, relational records.
```bash
python data/generate_data.py
```
*This creates the necessary CSV files in `data/raw/`.*

### 4. Run the ETL Pipeline
Execute the full orchestrator to Extract, Transform, Validate, run AI Analysis, and Load to your database.
```bash
python etl/pipeline.py
```
*Check the `logs/` directory for execution details and validation reports.*

### 5. Setup Power BI
1. Open Power BI Desktop.
2. Go to **View** -> **Themes** -> **Browse for themes** and select `powerbi/theme.json`.
3. Click **Get Data** -> **SQL Server**. Enter your server details and connect.
4. Load the `VW_...` views from your database.
5. Create a new Measures table and copy the formulas from `powerbi/DAX_Measures.md`.

## 🔮 Future Enhancements
- [ ] Migrate the ETL runtime to **Azure Data Factory** or **Apache Airflow**.
- [ ] Store raw CSVs in **Azure Blob Storage** or **AWS S3** rather than locally.
- [ ] Implement Incremental Loading (UPSERTs) instead of Full Load replacements.
- [ ] Add PySpark for distributed processing on massive datasets.

## 📄 License
This project is licensed under the MIT License. Feel free to use it for your own portfolio!
