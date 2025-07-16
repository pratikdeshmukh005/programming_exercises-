import os
from dotenv import load_dotenv

load_dotenv()

class Config:   
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        ' postgresql://postgres:postgres@localhost/book'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    BOOKS_PER_PAGE = 25
    
    # API settings
    JSON_SORT_KEYS = False
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'