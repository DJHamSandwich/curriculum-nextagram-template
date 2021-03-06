from app import app
from flask import render_template, Flask, session, redirect, url_for, escape, request
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint, create
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.base_model import BaseModel
from models.user import User
from models import user
from flask_login import LoginManager
import os
from instagram_web.util.google_oauth import oauth
import config
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect(app)

assets = Environment(app)
assets.register(bundles)


app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")


login_manager = LoginManager()
login_manager.init_app(app)

oauth.init_app(app)
csrf.init_app(app)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(user_id == User.id)
