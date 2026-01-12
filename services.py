from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import crud
import schemas


def create_book(db: Session, data: schemas.BookCreate):
    return crud.create_book(db, data)


def get_books(db: Session):
    return crud.get_books(db)


def get_book_by_id(db: Session, book_id: int):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


def update_book_service(db: Session, book_id: int, data: schemas.BookUpdate):
    book = crud.update_book(db, book_id, data)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book
def delete_book_service(db: Session, book_id: int):
    book = crud.delete_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {"message": "Book deleted successfully"}

