from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    copies_available: int

router = APIRouter()

@router.post("/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.put("/{book_id}")
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    db.commit()
    db.refresh(existing_book)
    return existing_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
