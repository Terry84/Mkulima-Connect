from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import ProduceListing
from farmer.forms import ProduceForm

farmer_bp = Blueprint('farmer', __name__, url_prefix='/farmer')

@farmer_bp.before_request
@login_required
def farmer_required():
    if not current_user.is_farmer:
        flash('Access restricted to farmers only.', 'danger')
        return redirect(url_for('main.index'))

@farmer_bp.route('/dashboard')
def dashboard():
    listings = ProduceListing.query.filter_by(farmer_id=current_user.id).order_by(ProduceListing.timestamp.desc()).all()
    return render_template('farmer/dashboard.html', listings=listings)

@farmer_bp.route('/add_produce', methods=['GET', 'POST'])
def add_produce():
    form = ProduceForm()
    if form.validate_on_submit():
        produce = ProduceListing(
            farmer_id=current_user.id,
            crop_name=form.crop_name.data.strip(),
            quantity=form.quantity.data,
            price=form.price.data,
            location=form.location.data.strip(),
            category=form.category.data,
            county=form.county.data,
            is_approved=False
        )
        db.session.add(produce)
        db.session.commit()
        flash('Produce listing added successfully and awaiting approval.', 'success')
        return redirect(url_for('farmer.dashboard'))
    return render_template('farmer/add_produce.html', form=form)
