from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Borrow
from datetime import datetime, timedelta

router = APIRouter()

LATE_FEE_PER_DAY = 1
BORROW_PERIOD_DAYS = 14

@router.get("/late-fees")
def late_fee_report(db: Session = Depends(get_db)):
    borrows = db.query(Borrow).filter(Borrow.return_date == None).all()
    report = []
    today = datetime.now()
    for borrow in borrows:
        overdue_days = (today - borrow.borrow_date).days - BORROW_PERIOD_DAYS
        if overdue_days > 0:
            report.append({
                "borrow_id": borrow.id,
                "overdue_days": overdue_days,
                "late_fee": overdue_days * LATE_FEE_PER_DAY
            })
    return {"late_fee_report": report}
