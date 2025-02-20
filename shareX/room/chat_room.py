from shareX import app
from shareX.database.config import db
from shareX.database.models import (User, ChatRoom,
                                    ChatRoomMessage, RoomMembers)
from .util import create_unique_room_id
from shareX.util import get_user_by_id

from flask import (render_template, request,
                   redirect, url_for, flash)
from flask_login import current_user, login_required
from sqlalchemy.exc import NoResultFound


# to add new members to a room, it can be done by having a
# add new members button and getting a list of all users in the database
# and then each of the user name is an href pointing to the add_users view

@app.route('/chat_room/<string:username>', methods=["GET", "POST"])
@login_required
def chat_room(username):
    # get the name of the friend user wants to chat with
    friend = request.args.get('friend')

    try:
        room_creator = db.session.execute(db.select(User).filter(User.username == username)).scalar_one()

        friend_in_db = db.session.execute(db.select(User).filter(User.username == friend)).scalar_one()

        room_id = create_unique_room_id(room_creator.username,
                                        friend_in_db.username,
                                        room_creator.id,
                                        friend_in_db.id)
        # verify if room already exists or not
        try:
            chat_room = db.session.execute(db.select(ChatRoom).filter_by(custom_id=room_id)).scalar_one()
            # get the messages in the room
            room_messages_query = db.session.execute(db.select(ChatRoomMessage).filter_by(room_id=chat_room.id))
            room_messages = room_messages_query.scalars()
            # find the creator of room
            creator = db.session.execute(
                db.select(RoomMembers).filter_by(room_id=chat_room.id, creator=True)).scalar_one()
            room_name = chat_room.room_name
            if creator.user_id == current_user.id:
                creator_tag = 'Creator'
            else:
                creator_tag = None
            # get the other member(s) in the chat room
            other_member = db.session.execute(
                db.select(RoomMembers).filter_by(room_id=chat_room.id, creator=False)).scalar_one()
            guest = get_user_by_id(other_member.user_id)
            guest_username = guest.username
            print(guest_username, 'guest username')
            room_messages_list = [room_message for room_message in room_messages]
            messages = [room_message.message for room_message in room_messages_list]

            if request.method == "POST":
                # handle the message
                form_message = request.form['message']
                new_message = ChatRoomMessage(message=form_message,
                                              sender_id=current_user.id,
                                              room_id=chat_room.id)

                db.session.add(new_message)
                db.session.commit()
                return redirect(f'/chat_room/{username}?friend={guest_username}')

            return render_template('chat_room.html',
                                   room_messages=room_messages_list,
                                   room_name=room_name,
                                   messages=messages,
                                   creator_tag=creator_tag,
                                   username=username,
                                   get_user_by_id=get_user_by_id,
                                   guest=guest_username)
        except NoResultFound:
            # create the room
            flash("Room don't exist create a one?", category='error')
            return redirect(url_for('create_room'))
    except Exception as e:
        print(e)
        flash('An unexpected error occured from our end')
        return (redirect(url_for('chat_room')))
