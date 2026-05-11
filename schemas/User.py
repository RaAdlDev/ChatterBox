from pydantic import BaseModel, EmailStr
from typing import Optional
class User(BaseModel):

    username: str
    email: EmailStr

class UserDB(User):
    password: str
    role: Optional[str] = None

class UserUpdate():
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

