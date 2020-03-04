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


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('image not found', 'warning')
        return redirect(url_for('home'))

    return render_template('donations/new.html', image=image)
