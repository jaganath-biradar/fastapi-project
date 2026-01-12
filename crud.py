from sqlalchemy.orm import Session
import models

def get_items(db: Session):
    return db.query(models.Book).all()
def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_item(db: Session, name: str):
    book = models.Book(
        title=name,
        description="N/A",
        author="Unknown",
        year=2024
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def delete_item(db: Session, item_id: int):
    book = db.query(models.Book).filter(models.Book.id == item_id).first()
    if book:
        db.delete(book)
        db.commit()
