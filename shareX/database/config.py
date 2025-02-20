from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from shareX import app
from shareX.config import ProductionConfig, DevelopmentConfig
import os
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')


if os.environ.get("APP_ENV") == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


path = os.path.join(os.path.dirname(__file__), 'instance')
database_path = os.path.join(path, 'database.database')
