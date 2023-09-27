# this is where all the models will live in
from shareX import db, login_manager
from sqlalchemy.sql import func
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def getCurrentTime():
    """
    Function to get the current time
    :return: str 
    """
    now = datetime.now()
    formatted_time = now.strftime('%-I:%M %p')

    return formatted_time

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30))
    message = db.relationship('Message', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def check_password_correction(self, attempted_password):
        """Function to check if the password attempted is matches that of user"""         
        if self.password == attempted_password:
            return True 
        return False


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.String, default=getCurrentTime())
    updated_at = db.Column(db.String, default=getCurrentTime()) # for when the user edits a message
    message_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    