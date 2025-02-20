from shareX import app
from shareX.database.config import db
from shareX.database.models import User

from flask import (request, flash,
                   redirect, url_for,
                   render_template)
from flask_login import login_user, login_required
from sqlalchemy.exc import NoResultFound


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
