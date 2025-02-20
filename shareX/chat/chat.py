from shareX import app
from shareX.database.config import db

from shareX.database.models import Message

from flask_login import login_required, current_user
from flask import (request, redirect,
                   url_for, flash,
                   render_template, jsonify)


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
                           current_username=current_username, )


@app.route('/chat/edit_message/<int:message_id>', methods=['PATCH'])
@login_required
def edit_message(message_id):
    try:
        if request.method == "PATCH":
            data = request.get_json()
            print(data)

            if "editMessage" in data:
                message = db.session.execute(db.select(Message).filter_by(id=message_id)).scalar_one()
                message.message = data["editMessage"]
                db.session.add(message)
                db.session.commit()

            return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail'}), 500

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


