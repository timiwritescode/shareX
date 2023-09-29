from shareX import app, login_manager
from flask import (render_template, 
                   request, redirect, url_for, 
                   flash, jsonify) 
from .util.helper_functions import *
from .models import User, Message
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
    flash("Welcome! You are logged in", category="success" )
    return render_template('home.html')

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
                return redirect(url_for("chat"))
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