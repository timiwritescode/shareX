from shareX import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    # if button clicked is for new chat, give new chat
    # if button cliacked  is for old chat, give old chat + previous messages
    return render_template('chat.html')