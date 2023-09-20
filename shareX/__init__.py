from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig, DevelopmentConfig
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

if os.environ.get("APP_ENVIRON") == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)