from app.extensions import db
from app.models import Reader

STATUS_VALIDOS = {"ativo", "bloqueado", "suspenso", "inativo"}

class ReaderService:
    
    @staticmethod
    def create(**kwargs):
        status = kwargs.get("status", "ativo")
        if status not in STATUS_VALIDOS:
            raise ValueError("Status Inválido")

        if "numero_matricula" not in kwargs or not kwargs["numero_matricula"]:
            kwargs["numero_matricula"] = ReaderService.gerador_numero_matricula()
        
        
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
    def delete(id):
        reader = Reader.query.get(id)

        if not reader:
            return None
        
        db.session.delete(reader)
        db.session.commit()

    
    @staticmethod
    def get_by_id(id):  
        return Reader.query.get(id) 
    
    @staticmethod
    def get_all():
        return Reader.query.all()   
    
    @staticmethod
    def get_by_cpf(cpf):
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        return Reader.query.filter_by(cpf=cpf_limpo).first()
    
    @staticmethod
    def gerador_numero_matricula():
        ultimo_leitor = Reader.query.order_by(Reader.id.desc()).first()
        if ultimo_leitor:
            try:
                ultimo_numero = int(ultimo_leitor.numero_matricula)
                novo_numero = f"{ultimo_numero + 1:06d}"
            except ValueError:
                novo_numero = "000001"
        else:
            novo_numero = "000001"
        
        return novo_numero