from jose import jwt, JWTError
from core.settings import settings
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, Query, WebSocketException, status
from database.connection import db
from database.models import User
from sqlalchemy.orm import Session
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

context = CryptContext(schemes=["bcrypt"])


def hash_password(plain_password):
    return context.hash(plain_password)

def verify_password(plain_password, user_pasword):
    return context.verify(plain_password, user_pasword)

def create_token(data: dict):
    to_encode = data.copy()
    time = datetime.utcnow() + timedelta(minutes=settings.token_duration)
    to_encode.update({"exp": time})
    return  jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token:str = Depends(oauth2)): 
    try:
        decode = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = decode.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User Not Found")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="You Are Not Allowed")
    
async def get_current(token: str = Query( None)):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    try:
        decode = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = decode.get("sub")
        if user_id:
            return user_id
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except JWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


def verify_admin(user = Depends(decode_token), db: Session = Depends(db)):

    u = db.get(User, user)
    if not u:
        raise HTTPException(status_code=404, detail="User Not Found")
    if u.role != "admin":
         raise HTTPException(status_code=401, detail="Unauthorized")


