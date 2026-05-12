from pydantic import BaseModel, EmailStr
from typing import Optional
class User(BaseModel):

    username: str
    email: EmailStr

class UserDB(User):
    password: str
    role: Optional[str] = None



