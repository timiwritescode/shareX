from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import ProductionConfig, DevelopmentConfig
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

if os.environ.get("APP_ENV") == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)




db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = None

path = os.path.join(os.path.dirname(__file__), 'instance')
database_path = os.path.join(path, 'database.db')

if not os.path.exists(database_path):
    with app.app_context():
        db.create_all()

from .models import User, Message, ChatRoom, ChatRoomMessage, RoomMembers
from shareX import routes
