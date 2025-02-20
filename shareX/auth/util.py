from shareX.database.config import db

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