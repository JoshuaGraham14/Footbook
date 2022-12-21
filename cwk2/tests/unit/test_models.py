from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and fields are defined correctly
    """
    user = User(email='john@smith.com', username='JohnSmithy1', password=generate_password_hash('12345678', method='sha256'), team='Arsenal')
    assert user.email == 'john@smith.com'
    assert user.username == 'JohnSmithy1'
    assert check_password_hash(user.password, '12345678')
    assert user.team == 'Arsenal'

def test_new_post():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and fields are defined correctly
    """
    post = Post(title='Messi is the GOAT', description='Messi is the greatest player of all time. FULL STOP.', user_id=1)
    assert post.title == 'Messi is the GOAT'
    assert post.description == 'Messi is the greatest player of all time. FULL STOP.'
    assert post.user_id == 1