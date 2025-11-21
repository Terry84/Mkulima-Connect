import pytest
from app import create_app, db
from models import User, ProduceListing
from flask_login import login_user

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
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def farmer_user(app):
    user = User(username='farmer1', email='farmer1@example.com', is_farmer=True)
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

def login_farmer(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_farmer_add_produce(client, farmer_user):
    login_farmer(client, farmer_user.email, 'password123')

    # Access add produce page
    response = client.get('/farmer/add_produce')
    assert response.status_code == 200
    assert b'Add Produce Listing' in response.data

    # Submit produce listing with valid data
    response = client.post('/farmer/add_produce', data={
        'crop_name': 'Tomatoes',
        'quantity': 100,
        'price': 50.5,
        'location': 'Farm Area',
        'category': 'vegetables',
        'county': 'Nairobi'
    }, follow_redirects=True)
    assert b'awaiting approval' in response.data

    # Check listing appears on dashboard
    response = client.get('/farmer/dashboard')
    assert b'Tomatoes' in response.data
    assert b'Pending' in response.data

def test_farmer_access_restriction(client):
    # Access without login redirects to login
    response = client.get('/farmer/dashboard', follow_redirects=True)
    assert b'Login' in response.data

def test_add_produce_invalid_data(client, farmer_user):
    login_farmer(client, farmer_user.email, 'password123')

    # Submit empty form
    response = client.post('/farmer/add_produce', data={}, follow_redirects=True)
    assert b'This field is required' in response.data or b'Not a valid integer value' in response.data
