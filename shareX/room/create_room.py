from shareX import app
from shareX import db
from shareX.models import (User, ChatRoom,
                           ChatRoomMessage, RoomMembers)
from shareX.util.helper_functions import create_unique_room_id, get_user_by_id

from flask import (render_template, request,
                   redirect, url_for, flash, jsonify)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, NoResultFound


@app.route('/create_room', methods=["GET", "POST"])
@login_required
def create_rom():
    username = current_user.username
    friend = request.args.get('friend')
    if request.method=="POST":
        try:
            friend = request.form['friend']

            friend_in_db = db.session.execute(db.select(User).filter_by(username=friend)).scalar_one()
            room_creator = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()

            room_id = create_unique_room_id(room_creator.username,
                                            friend_in_db.username,
                                            room_creator.id,
                                            friend_in_db.id)
            room_name = request.form['room-name']
            new_room = ChatRoom(custom_id=room_id,
                                room_name=room_name,
                                creator_id=room_creator.id)
            db.session.add(new_room)
            db.session.commit()

            first_member = RoomMembers(room_id=new_room.id,
                                          user_id=room_creator.id,
                                          creator=True) # as a rule, first member doubles as the room_creator or guest
            db.session.add(first_member)
            db.session.commit()

            second_member = RoomMembers(room_id=new_room.id,
                                            user_id=friend_in_db.id) # guest in the room
            db.session.add(second_member)
            db.session.commit()

            flash(f"Room {new_room.room_name} successfully created", category="success")
            return redirect(f'/chat_room/{username}?friend={friend}')
        except IntegrityError:
            return "room exists already"

        except Exception as e:
            print(e)
            return "an error occured"

    default_name = username + 'and' + friend
    return render_template('create_room.html',
                           default_name=default_name,
                           username=username,
                           friend=friend)
