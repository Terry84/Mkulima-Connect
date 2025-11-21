from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import ProduceListing, Message, User
from buyer.forms import SearchForm, MessageForm

buyer_bp = Blueprint('buyer', __name__, url_prefix='/buyer')

@buyer_bp.before_request
@login_required
def buyer_required():
    if current_user.is_farmer or current_user.is_admin:
        flash('Access restricted to buyers only.', 'danger')
        return redirect(url_for('main.index'))

@buyer_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        category = form.category.data
        county = form.county.data
        query = ProduceListing.query.filter_by(is_approved=True)
        if category and category != 'all':
            query = query.filter_by(category=category)
        if county and county != 'all':
            query = query.filter_by(county=county)
        results = query.order_by(ProduceListing.timestamp.desc()).all()
    return render_template('buyer/search.html', form=form, results=results)

@buyer_bp.route('/message/<int:produce_id>', methods=['GET', 'POST'])
def message(produce_id):
    produce = ProduceListing.query.filter_by(id=produce_id, is_approved=True).first()
    if not produce:
        flash('Produce listing not found or not approved.', 'danger')
        return redirect(url_for('buyer.search'))
    farmer = User.query.get(produce.farmer_id)
    form = MessageForm()
    if form.validate_on_submit():
        content = form.content.data.strip()
        if not content:
            flash('Message content cannot be empty.', 'danger')
            return render_template('buyer/message.html', form=form, produce=produce, farmer=farmer)
        msg = Message(
            buyer_id=current_user.id,
            farmer_id=farmer.id,
            produce_id=produce.id,
            content=content
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent to the farmer successfully.', 'success')
        return redirect(url_for('buyer.search'))
    return render_template('buyer/message.html', form=form, produce=produce, farmer=farmer)
