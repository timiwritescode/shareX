from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ProductionConfig, DevelopmentConfig
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shareX.db"
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

if os.environ.get("APP_ENV") == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .models import User, Message
from shareX import routes
