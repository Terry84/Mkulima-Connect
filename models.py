from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_farmer = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    produce_listings = db.relationship('ProduceListing', backref='farmer', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.buyer_id', backref='buyer', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.farmer_id', backref='farmer_user', lazy='dynamic')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        role = 'Admin' if self.is_admin else 'Farmer' if self.is_farmer else 'Buyer'
        return f'<User {self.username} ({role})>'

class ProduceListing(db.Model):
    __tablename__ = 'produce_listings'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    county = db.Column(db.String(100), nullable=False, index=True)
    is_approved = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    messages = db.relationship('Message', backref='produce', lazy='dynamic')

    def __repr__(self):
        return f'<ProduceListing {self.crop_name} by Farmer {self.farmer_id} Approved: {self.is_approved}>'

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    produce_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Message from Buyer {self.buyer_id} to Farmer {self.farmer_id} about Produce {self.produce_id}>'

@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    return User.query.get(int(user_id))
