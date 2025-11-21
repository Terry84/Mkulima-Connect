from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import ProduceListing, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def admin_required():
    if not current_user.is_admin:
        flash('Access restricted to admins only.', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
def dashboard():
    unapproved_listings = ProduceListing.query.filter_by(is_approved=False).order_by(ProduceListing.timestamp.desc()).all()
    farmers = {u.id: u for u in User.query.filter(User.id.in_([p.farmer_id for p in unapproved_listings])).all()}
    return render_template('admin/dashboard.html', listings=unapproved_listings, farmers=farmers)

@admin_bp.route('/approve/<int:produce_id>', methods=['POST'])
def approve(produce_id):
    listing = ProduceListing.query.filter_by(id=produce_id, is_approved=False).first()
    if not listing:
        flash('Produce listing not found or already approved.', 'danger')
        return redirect(url_for('admin.dashboard'))
    listing.is_approved = True
    db.session.commit()
    flash(f'Produce listing "{listing.crop_name}" approved successfully.', 'success')
    return redirect(url_for('admin.dashboard'))
