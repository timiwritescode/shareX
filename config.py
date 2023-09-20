import os
import dotenv

dotenv.load_dotenv()

class Config:
    """
    Flask app configuration settings
    """
    DEBUG = False
    secret_key = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLACHEMY_DATABASE_URI = os.getenv("DB_URI")


class ProductionConfig:
    """
    Configuration settings for production server
    """
    DEBUG = False

class DevelopmentConfig:
    """
    Configuration settings for development server
    """    
    DEBUG = True