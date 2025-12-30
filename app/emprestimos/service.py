from datetime import datetime
from app.extensions import db
from app.models import Loan, Book, Reader

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