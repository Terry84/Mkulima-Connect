import pytest
from app import create_app, db
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def register(client, username, email, password, confirm, role):
    return client.post('/auth/register', data={
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': confirm,
        'role': role,
    }, follow_redirects=True)

def login(client, email, password):
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)

def logout(client):
    return client.get('/auth/logout', follow_redirects=True)

def test_register_login_logout(client):
    # Register new user
    response = register(client, 'testuser', 'test@example.com', 'password123', 'password123', 'buyer')
    assert b'Registration successful' in response.data

    # Register with existing username/email fails
    response = register(client, 'testuser', 'test@example.com', 'password123', 'password123', 'buyer')
    assert b'Username or email already exists' in response.data

    # Login with wrong password fails
    response = login(client, 'test@example.com', 'wrongpassword')
    assert b'Invalid email or password' in response.data

    # Login correct
    response = login(client, 'test@example.com', 'password123')
    assert b'Logout' in response.data or b'Mkulima Connect' in response.data

    # Logout
    response = logout(client)
    assert b'You have been logged out' in response.data

def test_registration_validation(client):
    # Missing fields
    response = register(client, '', 'invalidemail', '123', '321', 'buyer')
    assert b'Invalid email address' in response.data or b'Field must be equal to password' in response.data
