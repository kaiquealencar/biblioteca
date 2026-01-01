import pdb
from datetime import datetime
from app.extensions import db
from app.models import Loan, Book, Reader
from sqlalchemy import or_

class LoanService:
    
    @staticmethod
    def create(**kwargs):    
        
        leitor_id = kwargs.get('leitor_id')
        livro_id = kwargs.get('livro_id')
        data_s = kwargs.get('data_emprestimo') or kwargs.get('data_saida')
        data_p = kwargs.get('data_devolucao') or kwargs.get('data_prevista')
        
        if isinstance(data_s, str) and data_s:
            data_s = datetime.strptime(data_s, "%Y-%m-%d")
        
        if isinstance(data_p, str) and data_p:
            data_p = datetime.strptime(data_p, "%Y-%m-%d")
            
        loan = Loan(
           leitor_id=leitor_id,
            livro_id=livro_id,
            data_saida=data_s,
            data_prevista=data_p,
            status="pendente",
            multa_aplicada=0.0
        )

        livro = Book.query.get(livro_id)
        if livro:
            livro.status = "emprestado"

        db.session.add(loan)
        db.session.commit()
        
        return loan
    
    @staticmethod
    def update(id, **kwargs):
        loan = Loan.query.get(id)

        if not loan:
            return None
        
        for date_field in ['data_emprestimo', 'data_devolucao', 'data_retorno']:
            if isinstance(kwargs.get(date_field), str) and kwargs[date_field]:
                kwargs[date_field] = datetime.strptime(kwargs[date_field], '%Y-%m-%d').date()
                
        for field, value in kwargs.items():
            if hasattr(loan, field):
                setattr(loan, field, value)

        db.session.commit()

        return loan
    

    @staticmethod
    def delete(id):
        loan = Loan.query.get(id)

        if not loan:
            return None
        
        db.session.delete(loan)
        db.session.commit()

    
    @staticmethod
    def get_by_id(id):  
        return Loan.query.get(id) 
    
    @staticmethod
    def get_all():
        return Loan.query.all()
    
    
    
    @staticmethod
    def search(leitor_nome="", livro_titulo="", status=""):
        query = db.session.query(Loan).outerjoin(Reader, Loan.leitor_id == Reader.id)\
                                      .outerjoin(Book, Loan.livro_id == Book.id)
        if leitor_nome and leitor_nome.strip():
            query = query.filter(
                or_(
                    Reader.nome.ilike(f"%{leitor_nome}%"), 
                    Reader.cpf.contains(leitor_nome)
                )
            )

        if livro_titulo and livro_titulo.strip():
            query = query.filter(
                or_(
                    Book.titulo.ilike(f"%{livro_titulo}%"), 
                    Book.isbn.contains(livro_titulo)
                )
            )
        if status and status.strip():
            query = query.filter(Loan.status == status)

        return query.order_by(Loan.id.desc()).all()
    
    @staticmethod
    def devolver_emprestimo(emprestimo_id):      
        emprestimo = Loan.query.get(emprestimo_id)
        if not emprestimo:
            return None
        
        if emprestimo.status == "devolvido":
            return emprestimo  
        
        emprestimo.status = "devolvido"
        emprestimo.data_retorno = datetime.now()
        
        livro = Book.query.get(emprestimo.livro_id)
        if livro:
            livro.status = "disponivel"
        
        db.session.commit()
        return emprestimo   
    
    @staticmethod
    def calcular_multa(emprestimo_id, valor_multa_por_dia):
        emprestimo = Loan.query.get(emprestimo_id)
        if not emprestimo:
            return None
        
        if emprestimo.status != "devolvido" or not emprestimo.data_retorno:
            return emprestimo  
        
        dias_atraso = (emprestimo.data_retorno.date() - emprestimo.data_prevista.date()).days
        if dias_atraso > 0:
            multa_total = dias_atraso * valor_multa_por_dia
            emprestimo.multa_aplicada = multa_total
        else:
            emprestimo.multa_aplicada = 0.0
        
        db.session.commit()
        return emprestimo
    
    @staticmethod
    def consultar_disponibilidade_livro(livro_id):
        emprestimo_ativo = Loan.query.filter_by(livro_id=int(livro_id), status="pendente").first()

        if emprestimo_ativo:
            return False

        return True
