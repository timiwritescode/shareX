from shareX import app, login_manager
from flask import (render_template, 
                   request, redirect, url_for, 
                   flash, jsonify) 
from .util.helper_functions import *
from .models import User, Message, ChatRoom, ChatRoomMessage, RoomMembers
from shareX import db
from sqlalchemy.exc import NoResultFound, IntegrityError
from flask_login import login_required, login_user, current_user


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
        print(created_rooms)
        guests_in_created_rooms = []
        for room in created_rooms:
            room_id = room.room_id
            guest_in_room = db.session.execute(db.select(RoomMembers).filter_by(room_id=room_id, creator=False)).scalars()
            for guest in guest_in_room:
                guest_id = guest.user_id
                guest = get_user_by_id(guest_id)
                guests_in_created_rooms.append(guest.username)
        print(guests_in_created_rooms)        

        # find rooms the user belong in but not created by them
        rooms_guest_in = db.session.execute(db.select(RoomMembers).filter_by(user_id=user_id, creator=False)).scalars()
        rooms_guest_in = [room for room in rooms_guest_in]
        print(len(rooms_guest_in), 'len')
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
        print(room_creators)
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

@app.route('/chat', methods=['GET', 'POST', 'DELETE'])
@login_required
def chat():
    # if button clicked is for new chat, give new chat
    # if button clicked  is for old chat, give old chat + previous messages
    try:
        user_id = current_user.id
        previous_messages = db.session.execute(db.select(Message).filter_by(user_id=user_id)).scalars()
        
        current_username = current_user.username
        if request.method == "POST":
            form_message = request.form['msg-input']     
            message = Message(message=form_message, message_id=user_id, user_id=user_id)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('chat'))
    except Exception as e:
        flash("An error occured", category="error")
        print(e)
        return redirect(url_for('chat'))        
    return render_template('chat.html', 
                           previous_messages=previous_messages,
                           current_username=current_username,) 


@app.route('/create_room', methods=["GET", "POST"])
@login_required
def create_room():
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

"""
@app.route('/join_room/<string:room_id>')
@login_required
def join_room(room_id):
    current_user = current_user
    try:
        room = db.session.execute(db.select(RoomMembers).filter_by(room_id=room_id, user_id=)).scalar_one()
        
        user_id = current_user.id
    except NoResultFound:
        return 'Room does not exist'
"""

# to add new members to a room, it can be done by having a
# add new members button and getting a list of all users in the database
# and then each of the user name is an href pointing to the add_users view

@app.route('/chat_room/<string:username>', methods=["GET", "POST"])
@login_required
def chat_room(username):
    # get the name of the friend user wants to chat with
    friend = request.args.get('friend')
 
    try:
        room_creator = db.session.execute(db.select(User).filter(User.username==username)).scalar_one()
        
        friend_in_db = db.session.execute(db.select(User).filter(User.username==friend)).scalar_one()

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
            creator = db.session.execute(db.select(RoomMembers).filter_by(room_id=chat_room.id, creator=True)).scalar_one()
            room_name = chat_room.room_name
            if creator.user_id == current_user.id:
                creator_tag = 'Creator'
            else:
                creator_tag = None
            # get the other member(s) in the chat room
            other_member = db.session.execute(db.select(RoomMembers).filter_by(room_id=chat_room.id, creator=False)).scalar_one()
            guest = get_user_by_id(other_member.user_id)
            guest_username = guest.username 
            print(guest_username, 'guest username')
            room_messages_list = [room_message for room_message in room_messages]    
            messages = [room_message.message for room_message in room_messages_list]

            
            if request.method=="POST":
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
                                   creator_tag = creator_tag,
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
        return(redirect(url_for('chat_room')))


@app.route('/chat/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    try:
        message = db.session.execute(db.select(Message).filter_by(id=message_id)).scalar_one()
        db.session.delete(message)
        db.session.commit()
        responseObject = {
            'status': 'success'
        }
        return jsonify(responseObject), 200     
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail'
        }
        return jsonify(responseObject), 500
     
   
@app.route('/chat/edit_message/<int:message_id>', methods=['PATCH'])
@login_required
def edit_message(message_id):
    try:
        if request.method == "PATCH":
            data =  request.get_json() 
            print(data)
            
            if "editMessage" in data:
                message = db.session.execute(db.select(Message). filter_by(id=message_id)).scalar_one()
                message.message = data["editMessage"]
                db.session.add(message)
                db.session.commit()

            return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail'}), 500    

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        print(username)
        password_confirm = request.form['password-confirm']
        print(password_confirm)
        if confirm_password(password, password_confirm):
            try:
                user = User(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                flash("User successfully created", "success")
                return redirect(url_for('login'))
            
            except IntegrityError:
                flash("Username already exists, try another one", 
                      category="username-error")
                return redirect(url_for("register"))
            except Exception as e:
                print(e)
                flash("An error occured, don't worry it's us not you", 
                      category='register-error')
            return redirect(url_for("register"))

                
        else: 
            flash("Password does not match", 
                  category='password-error')
            return redirect(url_for("register"))

    return render_template('register.html')             
     

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(password, username)
        try:
            user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
            if user.check_password_correction(password):
                login_user(user)
                # flask login automatically sets a welcome message so no need for one
                flash("Successfully logged in", category="success")
                return redirect(url_for("home"))
            else:
                flash("Username or password incorrect", category="password-error")            
                return redirect(url_for("login"))
        except NoResultFound:
            flash("Username or password incorrect", category="password-error")
            return redirect(url_for("login"))    
        
        except Exception as e:
            flash("An error occured, don't worry it's us not you", category="error")
            return redirect(url_for("login"))    
        
         
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    return redirect(url_for('login'))

    