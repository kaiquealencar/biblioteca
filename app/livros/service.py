from app.extensions import db
from app.models import Book

class BookService:

    @staticmethod
    def create(**kwargs):
        book = Book(**kwargs)
        db.session.add(book)
        db.session.commit()

        return book

    @staticmethod
    def update(id, **kwargs):
        book = Book.query.get(id)

        if not book:
            return None
        
        for field, value in kwargs.items():
            if hasattr(book, field):
                setattr(book, field, value)
        
        db.session.commit()

        return book


    @staticmethod
    def delete(id):
        book = Book.query.get(id)

        if not book:
                return None
            
        db.session.delete(book)
        db.session.commit()