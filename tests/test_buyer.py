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
        # Create buyer user
        buyer = User(username='buyer1', email='buyer1@example.com', is_farmer=False)
        buyer.set_password('password123')
        db.session.add(buyer)
        # Create farmer user and produce
        farmer = User(username='farmer1', email='farmer1@example.com', is_farmer=True)
        farmer.set_password('password123')
        db.session.add(farmer)
        db.session.commit()

        produce = ProduceListing(
            farmer_id=farmer.id,
            crop_name='Maize',
            quantity=200,
            price=40.0,
            location='Farmville',
            category='grains',
            county='Nairobi',
            is_approved=True
        )
        db.session.add(produce)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def login_buyer(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_search_produce(client):
    login_buyer(client, 'buyer1@example.com', 'password123')

    # Search with no filters (submit empty or defaults)
    response = client.post('/buyer/search', data={'category': 'all', 'county': 'all'}, follow_redirects=True)
    assert b'Maize' in response.data

    # Search with category filter no results
    response = client.post('/buyer/search', data={'category': 'fruits', 'county': 'all'}, follow_redirects=True)
    assert b'No produce found' in response.data or b'No produce found matching your criteria' in response.data

def test_message_farmer(client):
    login_buyer(client, 'buyer1@example.com', 'password123')

    # Get produce id
    produce_id = 1

    # GET message page
    response = client.get(f'/buyer/message/{produce_id}')
    assert response.status_code == 200
    assert b'Send Message' in response.data

    # POST empty message (validation error)
    response = client.post(f'/buyer/message/{produce_id}', data={'content': ''}, follow_redirects=True)
    assert b'This field is required' in response.data or b'Message content cannot be empty' in response.data

    # POST valid message
    response = client.post(f'/buyer/message/{produce_id}', data={'content': 'Is this available for delivery?'}, follow_redirects=True)
    assert b'Message sent' in response.data
