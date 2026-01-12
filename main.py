from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import models
import crud
import services
import schemas

from db import engine, SessionLocal, get_db

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI()

# -----------------------------
# Create DB tables
# -----------------------------
models.Base.metadata.create_all(bind=engine)

# -----------------------------
# Templates & static files
# -----------------------------
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health_check():
    return {"message": "FastAPI is running"}

# =====================================================
# UI ROUTES (BOOK UI)
# =====================================================

# READ (List books)
@app.get("/")
def read_books_ui(request: Request):
    db = SessionLocal()
    books = crud.get_items(db)
    db.close()
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "items": books}
    )

# SHOW CREATE PAGE
@app.get("/create-page")
def create_page(request: Request):
    return templates.TemplateResponse(
        "create.html",
        {"request": request}
    )

# CREATE BOOK (POST)
@app.post("/create")
def create_book_ui(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...)
):
    db = SessionLocal()
    book = models.Book(
        title=title,
        description="N/A",
        author=author,
        year=year
    )
    db.add(book)
    db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)

# EDIT PAGE (GET)
@app.get("/edit/{book_id}")
def edit_book_page(request: Request, book_id: int):
    db = SessionLocal()
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.close()

    if not book:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "book": book}
    )

# UPDATE BOOK (POST)
@app.post("/update/{book_id}")
def update_book_ui(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...)
):
    db = SessionLocal()
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book:
        book.title = title
        book.author = author
        book.year = year
        db.commit()

    db.close()
    return RedirectResponse("/", status_code=303)

# DELETE BOOK
@app.get("/delete/{book_id}")
def delete_book_ui(book_id: int):
    db = SessionLocal()
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    db.close()
    return RedirectResponse("/", status_code=303)

# =====================================================
# API ROUTES (BOOKS)
# =====================================================

@app.get("/books/", response_model=list[schemas.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    return services.get_book_by_id(db, book_id)

@app.post("/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return services.create_book(db, book)

@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    return services.update_book_service(db, book_id, book)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return services.delete_book_service(db, book_id)
