from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Member

router = APIRouter()

@router.get("/")
def get_all_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@router.get("/{member_id}")
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
