from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.User import UserDB
from database.connection import db
from services.auth_services import register_a, login_a, users_a, me, delete_u, promote_user, find_user
from core.security import decode_token, verify_admin
from typing import Optional

router = APIRouter()

@router.post("/register", status_code=201)
async def register(data: UserDB, db = Depends(db)):
    verify =  register_a(data, db)
    if verify:
        return {"status": "successful request"}
    else:
        raise HTTPException(status_code=409, detail="Try Another Data")

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db = Depends(db)):
    verify =  login_a(form, db)
    if verify:
        return verify
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")   

@router.get("/users")
async def users( search: Optional[str] = None, db = Depends(db), current = Depends(decode_token)):
    if search:
        return find_user(db, search)
    return users_a(db, current)


@router.get("/users/me")
async def get_me(db = Depends(db), current = Depends(decode_token)):
    return me(db, current)
  

@router.delete("/users/delete/{user_id}")
async def delete_user(user_id:str, db = Depends(db),  v_admin = Depends(verify_admin)):
     verify = delete_u(db, user_id)
     if verify is None:
         raise HTTPException(status_code=404, detail="User Not Found")
     return {"status": "successful request"}
  

@router.patch("/users/promote/{user_id}")
async def ascend(user_id:str, db = Depends(db), v_admin = Depends(verify_admin)):
     verify = promote_user(db, user_id)
     if verify is None:
         raise HTTPException(status_code=404, detail="User Not Found")
     return {"status": "successful request"}
         
  


