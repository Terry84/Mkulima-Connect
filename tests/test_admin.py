import pytest
from app import create_app, db
from models import User, ProduceListing

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('password123')
        db.session.add(admin)

        farmer = User(username='farmer1', email='farmer1@example.com', is_farmer=True)
        farmer.set_password('password123')
        db.session.add(farmer)
        db.session.commit()

        produce = ProduceListing(
            farmer_id=farmer.id,
            crop_name='Carrots',
            quantity=150,
            price=35.0,
            location='Farm Area',
            category='vegetables',
            county='Nairobi',
            is_approved=False
        )
        db.session.add(produce)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def login_admin(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_admin_dashboard_and_approval(client):
    login_admin(client, 'admin@example.com', 'password123')

    # Access dashboard shows unapproved produce
    response = client.get('/admin/dashboard')
    assert b'Carrots' in response.data
    assert b'Approve' in response.data

    # Approve produce
    response = client.post('/admin/approve/1', follow_redirects=True)
    assert b'approved successfully' in response.data

    # After approval, produce should not appear in unapproved list
    response = client.get('/admin/dashboard')
    assert b'No unapproved produce listings' in response.data

def test_admin_access_restriction(client):
    # Try to access admin without login
    response = client.get('/admin/dashboard', follow_redirects=True)
    assert b'Login' in response.data
