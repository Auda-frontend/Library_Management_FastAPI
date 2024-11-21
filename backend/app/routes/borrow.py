from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Borrow, Book
from datetime import datetime

router = APIRouter()

@router.post("/issue")
def issue_book(book_id: int, member_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.copies_available <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    borrow = Borrow(book_id=book_id, member_id=member_id, borrow_date=datetime.now())
    book.copies_available -= 1
    db.add(borrow)
    db.commit()
    return {"message": "Book issued successfully"}

@router.put("/return/{borrow_id}")
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    book.copies_available += 1
    borrow.return_date = datetime.now()
    db.commit()
    return {"message": "Book returned successfully"}
