# this is where all the models will live in
from shareX import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30))
    message = db.relationship('Message', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_username_present(self):
        
        user = db.get_or_404(User, self.username)
        if user:
            return True
         

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now()) # for when the user edits a message
    message_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))