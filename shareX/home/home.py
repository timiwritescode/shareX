from shareX import app
from shareX.database.config import db
from shareX.database.models import User, RoomMembers,ChatRoom
from shareX.util.util import get_user_by_id

from flask_login import login_required, current_user
from flask import render_template, flash, redirect, url_for



@app.route('/')
@app.route('/start')
def start():
    return render_template('start_page.html')


@app.route('/home')
@login_required
def home():
    # all the messages specific to the user

    user_id = current_user.id
    username = current_user.username
    password = current_user.password
    try:
        users = db.session.execute(db.select(User)).scalars()
        # get a list of other users stored in the database
        # and use it to display the other users available
        other_users = [other_user.username for other_user in users if other_user.id != user_id]
        # find the rooms created by this user
        created_rooms = db.session.execute(db.select(RoomMembers).filter_by(user_id=user_id, creator=True)).scalars()
        # print(created_rooms)
        guests_in_created_rooms = []
        for room in created_rooms:
            room_id = room.room_id
            guest_in_room = db.session.execute(
                db.select(RoomMembers).filter_by(room_id=room_id, creator=False)).scalars()
            for guest in guest_in_room:
                guest_id = guest.user_id
                guest = get_user_by_id(guest_id)
                guests_in_created_rooms.append(guest.username)
        # print(guests_in_created_rooms)

        # find rooms the user belong in but not created by them
        rooms_guest_in = db.session.execute(db.select(RoomMembers).filter_by(user_id=user_id, creator=False)).scalars()
        rooms_guest_in = [room for room in rooms_guest_in]
        # print(len(rooms_guest_in), 'len')
        room_creators = []
        # find the creator of the room
        for room in rooms_guest_in:
            room_id = room.room_id
            print('room id', room_id)
            # find the actual chat room with id obtained
            corresponding_chat_room = db.session.execute(db.select(ChatRoom).filter_by(id=room_id)).scalar_one()
            print(corresponding_chat_room.room_name)
            # find creator of that room
            room_creator_id = corresponding_chat_room.creator_id
            room_creator = db.session.execute(db.select(User).filter_by(id=room_creator_id)).scalar_one()

            room_creators.append(room_creator.username)
        # print(room_creators)
        return render_template('home.html',
                               users=other_users,
                               curr_user=username,
                               guests=guests_in_created_rooms,
                               room_creators=room_creators,
                               get_user_by_id=get_user_by_id)
    except Exception as e:
        print(e)
        flash("An error occured, it's us not you")
        return redirect(url_for('home'))
