from werkzeug.security import generate_password_hash

from app import create_app
from models.models import User

def seed():
    User.create(
        name = 'admin',
        email = 'admin@admin.com',
        password = generate_password_hash(
            '123', method='pbkdf2', salt_length=16
        ),
        is_admin = True
    )
    User.create(
        name = 'testUser',
        email = 'test@test.com',
        password = generate_password_hash(
            '123', method='pbkdf2', salt_length=16
        ),
        is_admin = False
    )


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed()