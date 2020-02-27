import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for, Flask, session, escape
from models.base_model import BaseModel
from models.session import Session
from models import session
from models.user import User
from models import user
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


# @app.route('/')
# def index():
#     if 'username' in session:
#         return 'Logged in as %s' % escape(session['username'])
#     return 'You are not logged in'


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/new_form', methods=['POST'])
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

    if user and check_password_hash:
        flash("Login successfull")
        # session["user.id"] = user.id
        return redirect(url_for('sessions.new'))
    # User is valid and the password given is valid
