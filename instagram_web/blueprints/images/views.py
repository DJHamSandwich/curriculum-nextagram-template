import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for, Flask, session, escape
from models.base_model import BaseModel
from models.user import User
from models import user
from models.image import Image
from models import image
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from helpers import *

images_blueprint = Blueprint('images', __name__, template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
    if not 'image' in request.files:
        flash('No image provided', 'warning')
        return redirect(request.referrer)

    file = request.files.get('image')
    caption = request.form.get('caption')

    file.filename = secure_filename(file.filename)

    if not upload_file_to_s3(file):
        flash('Error uploading image', 'warning')
        return redirect(request.referrer)

    image = Image(filename=file.filename, caption=caption,
                  user_id=current_user.id)

    if not image.save():
        flash('Image unable to save', 'warning')
        return redirect(request.referrer)

    flash('Successfully added new image', 'success')
    return redirect(request.referrer)
