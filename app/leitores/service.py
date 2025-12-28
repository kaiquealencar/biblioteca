from app.extensions import db
from app.models import Reader

STATUS_VALIDOS = {"ativo", "bloqueado", "suspenso", "inativo"}

class ReaderService:
    
    @staticmethod
    def create(**kwargs):
        status = kwargs.get("status", "ativo")
        if status not in STATUS_VALIDOS:
            raise ValueError("Status Inválido")
        
        reader = Reader(**kwargs)
        db.session.add(reader)
        db.session.commit()
        
        return reader
    
    @staticmethod
    def update(id, **kwargs):
        reader = Reader.query.get(id)


        if not reader:
            return None
        
        for field, value in kwargs.items():
            if hasattr(reader, field):
                setattr(reader, field, value)

        db.session.commit()

        return reader
    

    @staticmethod
    def get_by_id(id):  
        return Reader.query.get(id) 
    
    @staticmethod
    def get_all():
        return Reader.query.all()   

    @staticmethod
    def delete(id):
        reader = Reader.query.get(id)

        if not reader:
            return None
        
        db.session.delete(reader)
        db.session.commit()