from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import books, members, borrow, reports

app = FastAPI()

from app.models import Book, Borrow, Member
Base.metadata.create_all(bind=engine)


app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System"}
