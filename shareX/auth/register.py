from shareX import app, db
from shareX.models import User
from shareX.util.helper_functions import confirm_password

from flask import (request, flash,
                   redirect, url_for,
                   render_template)
from sqlalchemy.exc import IntegrityError




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
