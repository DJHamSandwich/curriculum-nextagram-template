import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for
from models.base_model import BaseModel
from models.user import User
from models import user
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')
app = Blueprint('home', __name__)


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new_form', methods=['POST'])
def create_new_form():
    nu = User(username=request.form.get('username'), email=request.form. get(
        'email'), password=generate_password_hash(request.form.get('password')))

    if nu.save():
        flash("succesfully created a new user")
        return redirect(url_for('users.new'))
    else:
        flash("Not Succesfull in creating new user")
        return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@app.route("/")
def home():
    return render_template("home.html")


@users_blueprint.route("/user")
def user():
    return render_template()
