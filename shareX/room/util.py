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