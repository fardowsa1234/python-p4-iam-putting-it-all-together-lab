from models import db, User, Recipe
from app import app

with app.app_context():
    db.create_all()
    
    user = User(username='testuser', password='testpass', image_url='http://example.com/image.jpg', bio='This is a test user.')
    db.session.add(user)
    db.session.commit()

    recipe = Recipe(title='Test Recipe', instructions='These are the instructions for the test recipe. Make sure to include at least 50 characters.', minutes_to_complete=30, user_id=user.id)
    db.session.add(recipe)
    db.session.commit()
