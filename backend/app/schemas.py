from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class BookCreate(BaseModel):
    name: str
    isbn: str
    author: str
    category: str

class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True


