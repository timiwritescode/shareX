from shareX.database.config import db
from shareX.database.models import User

def validate_password(id, password):
    user = db.session.execute
    return False


def confirm_password(password, confirmation): 
    """
    Confirm if password submitted by user is correct
    """
    if password == confirmation:
        return True
    
    return False


def create_unique_room_id(creator, friend, creator_id, friend_id):
    """
    Function gets the user attempting to create a room and makes a unique
    id from the combination of the username and id of the creator and those of the
    friend they want to create it with
    :params: creator -> sqlalchemy object
            friend ->  sqlachemy object
    :returns string
    """ 
    creator_username = creator
    friend_username = friend
    creator_id = str(creator_id)
    friend_id = str(friend_id)

    fields_combination = creator_username + friend_username + creator_id + friend_id
    room_id = sorted(fields_combination, reverse=True)

    return ''.join(room_id)


def get_user_by_id(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()

    return user

 