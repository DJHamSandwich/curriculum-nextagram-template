import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for, Flask, session, escape
from models.base_model import BaseModel
from models.user import User
from models import user
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/new_form', methods=['GET', 'POST'])
def create():

    # password keyed in by the user in the sign in form
    password_to_check = request.form['password']

    email_input = request.form['email']

    user = User.get_or_none(User.email == email_input)

    if not user:
        flash("User does not exist")
        return redirect(url_for('sessions.new'))

    if not check_password_hash(user.password, password_to_check):
        flash("Password does not match")
        return redirect(url_for('sessions.new'))

    if user and request.method == 'POST':
        # flash("Login successfull")
        # session['user_id'] = user.id
        # return redirect(url_for('sessions.new'))

        login_user(user)
        flash(f"Welcome back {user.username}! You are now logged in")
        return redirect(url_for("home"))


@sessions_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully logged out. Goodbye!")
    return redirect(url_for("home"))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('sessions.new'))
