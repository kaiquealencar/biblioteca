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
    
    @staticmethod
    def upate(id, usuario=None, email=None, senha=None):
        
        user = User.query.get(id)        
        if not user:
            return None
        
        fields = {"usuario": usuario, "email": email, "senha": senha}

        for key, value in fields.items():
            if value is not None:
                if key == "senha":
                    user.password_hash = generate_password_hash(senha)
                else:
                    setattr(user, key, value)
       

        db.session.commit()

        return user
    
    @staticmethod
    def delete(id):
        user = User.query.get(id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()

        return True
        

    
