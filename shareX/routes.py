from shareX import app
from flask import (render_template, 
                   request, redirect, url_for, 
                   flash) 
from .util.helper_functions import *
from .models import User, Message
from shareX import db

@app.route('/')
@app.route('/start')
def start():
    return render_template('start_page.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    # if button clicked is for new chat, give new chat
    # if button clicked  is for old chat, give old chat + previous messages
    
    return render_template('chat.html')


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
            except Exception as e:
                print(e)
                flash("An error occured, don't worry it's us not you", 'error')
            return redirect(url_for("register"))

                
        else: 
            flash("Password does not match", 'error')
            return redirect(url_for("register"))

    return render_template('register.html')             
     

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        if user.is_username_present():
            print(user.username)
            return {1: True}
    return render_template('login.html')
