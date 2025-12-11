from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:

    @staticmethod
    def create(usuario, email, senha):
        hashed_password = generate_password_hash(senha)

        user = User(usuario=usuario, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        return user
    
