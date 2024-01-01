class Config:
    # Database Configuration
    HOSTNAME = "13.212.232.71"
    PORT = 3306
    USERNAME = "serpApi"
    PASSWORD = "CGpch5JKsSD4w6rP"
    DATABASE = "serpapi"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

    # Other configuration variables
    SERP_API_KEY = "39ffcd6e2c5819a50c7ceb95d2dcecec4f38960d1f065a0f33c848e1abf51da2"
