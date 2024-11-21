from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    copies_available = Column(Integer)

class Member(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    borrowed_books = relationship("Borrow", back_populates="member")

class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    borrow_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    member = relationship("Member", back_populates="borrowed_books")
    book = relationship("Book")
