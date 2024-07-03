import pytest
from app import app, db
from models import User, Recipe

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.drop_all()

def test_signup(client):
    response = client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'

def test_login(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'testuser'

def test_check_session(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.get('/check_session')
    assert response.status_code == 200
    data = response.get_json()
    assert data['username'] == 'testuser'

def test_logout(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.delete('/logout')
    assert response.status_code == 204
    response = client.get('/check_session')
    assert response.status_code == 401

def test_create_recipe(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    response = client.post('/recipes', json={
        'title': 'Test Recipe',
        'instructions': 'These are the instructions for the test recipe. Make sure to include at least 50 characters.',
        'minutes_to_complete': 30
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Recipe'

def test_view_recipes(client):
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpass',
        'image_url': 'http://example.com/image.jpg',
        'bio': 'This is a test user.'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    client.post('/recipes', json={
        'title': 'Test Recipe',
        'instructions': 'These are the instructions for the test recipe. Make sure to include at least 50 characters.',
        'minutes_to_complete': 30
    })
    response = client.get('/recipes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Recipe'
