import peeweedbevolve
from flask import Blueprint, render_template, flash, request, redirect, url_for, Flask, session, escape
from models.base_model import BaseModel
from models.image import Image
from models.donation import Donation
from flask_login import login_required, current_user
from instagram_web.util.braintree import gateway


donations_blueprint = Blueprint(
    'donations', __name__, template_folder='templates')


@donations_blueprint.route('/<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('image not found', 'warning')
        return redirect(url_for('home'))

    client_token = gateway.client_token.generate()

    if not client_token:
        flash('Unable to obtain client token', 'warning')
        return redirect(url_for('home'))

    return render_template('donations/new.html', image=image, client_token=client_token,)


@donations_blueprint.route('/<image_id>/', methods=['POST'])
@login_required
def create(image_id):
    nonce = request.form.get('payment_method_nonce')

    if not nonce:
        flash('credit card details are invalid', 'warning')
        return redirect(url_for('home'))

    image = Image.get_or_none(Image.id == image_id)

    if not image:
        flash('image not found', 'warning')
        return redirect(url_for('home'))

    amount = request.form.get('amount')

    if not amount:
        flash('please provide an amount to donate')
        return redirect(url_for('home'))

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if not result.is_success:
        flash('unable to complete donation', 'warning')
        return redirect(request.referrer)

    donation = Donation(amount=amount, image_id=image.id,
                        user_id=current_user.id)

    if not donation.save():
        flash('Donation successfull but could not create record', 'warning')
        return redirect(url_for('home'))

    flash('Successfully donated RM{amount}', 'success')
    return redirect(url_for('home'))
