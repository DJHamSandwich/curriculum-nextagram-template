from app import app
from flask import render_template, Flask, session, redirect, url_for, escape, request
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

# app = Flask(__name__)
# app.secret_key = b'\xa3\x7f\x88C\xc8\xa8\x089\x19\x11mz\xf3\xe4\x1f\xa7'


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")

app.register_blueprint(sessions_blueprint, url_prefix="/sessions")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')

#     if 'User.id' in session:
#         return 'Logged in as %s' % escape(session['User.id'])
#     return 'You are not logged in'
#     else:
#         return render_template('home.html')


# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('User.id', None)
#     return redirect(url_for('home'))
