import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for
from models.base_model import BaseModel
from models.user import User
from models import user
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new_form', methods=['POST'])
def create():
    nu = User(username=request.form.get('username'), email=request.form. get(
        'email'), password=generate_password_hash(request.form.get('password')))

    if nu.save():
        flash("succesfully created a new user")
        return redirect(url_for('users.new'))
    else:
        flash("Not Succesfull in creating new user")
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):

    user = User.get_or_none(User.id == id)

    if not user:
        flash('user does not exist')
        return redirect(url_for('home'))

    if not current_user.id == user.id:  # current_user method is
        flash('you are not allowed to vieew this page')
        return redirect(url_for('home'))

    return render_template('users/edit.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)

    username = request.form.get('username')
    email = request.form.get('email')

    user.email = email
    user.username = username

    if user.save():
        flash("Succesfully updated info!")
        return redirect(url_for('users.edit', id=user.id))
    else:
        flash("Not Succesfull in updating info")
        return render_template('users/edit.html')


@users_blueprint.route("/user")
def user():
    return render_template()
