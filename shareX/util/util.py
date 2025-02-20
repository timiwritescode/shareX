from shareX.database.config import db
from shareX.database.models import User



def get_user_by_id(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()

    return user

 