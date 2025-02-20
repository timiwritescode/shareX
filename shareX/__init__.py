from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO

from shareX.config import ProductionConfig, DevelopmentConfig
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = None

socketio = SocketIO(app)


from shareX.database.models import User, Message, ChatRoom, ChatRoomMessage, RoomMembers
from shareX import routes



with app.app_context():
    from .database.config import db
    db.create_all()

