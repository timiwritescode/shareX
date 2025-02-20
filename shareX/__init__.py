from flask import Flask
from flask_login import LoginManager

from shareX.config import ProductionConfig, DevelopmentConfig
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URI')
# app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

# if os.environ.get("APP_ENV") == 'production':
#     app.config.from_object(ProductionConfig)
# else:
#     app.config.from_object(DevelopmentConfig)




# database = SQLAlchemy(app)
# migrate = Migrate(app, database)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = None



from shareX.database.models import User, Message, ChatRoom, ChatRoomMessage, RoomMembers
from shareX import routes



with app.app_context():
    from .database.config import db
    db.create_all()