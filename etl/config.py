import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database Settings
    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 18 for SQL Server}")
    
    # Construct Connection String
    # Note: For production Azure SQL, Encryption is typically enabled.
    if DB_SERVER and DB_NAME:
        DB_CONNECTION_STRING = (
            f"DRIVER={DB_DRIVER};SERVER={DB_SERVER};DATABASE={DB_NAME};"
            f"UID={DB_USER};PWD={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        )
        # SQLAlchemy URL format for pyodbc (should not have braces in the query param)
        from sqlalchemy.engine import URL
        driver_name = DB_DRIVER.strip("{}")
        SQLALCHEMY_DATABASE_URI = URL.create(
            "mssql+pyodbc",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_SERVER,
            database=DB_NAME,
            query={"driver": driver_name}
        )
    else:
        DB_CONNECTION_STRING = None
        SQLALCHEMY_DATABASE_URI = "sqlite:///local_warehouse.db" # Fallback for local testing
    
    # API Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Path Settings
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    
    # Ensure directories exist
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

config = Config()
