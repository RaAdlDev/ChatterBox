from core.security import hash_password, verify_password, create_token
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from database.models import User

def register_a(data, db: Session):
    show = db.execute(select(User).where(or_(data.username == User.username, data.email == User.email))).all()
    admin = db.execute(select(User)).all()
    if not admin:
        data.role = "admin"
    if not show:
        data.password = hash_password(data.password)
        db.add(User(username = data.username, email = data.email, password = data.password, role = data.role))
        db.commit()
        return True
    return None

def login_a(form, db: Session):
    verify = db.execute(select(User).where(User.username == form.username)).scalar_one_or_none()
    if verify:
        v_password = verify_password(form.password, verify.password)
        if v_password:
            return {"acces_token": create_token({"sub": verify.user_id}), "token_type": "bearer"}
        return None
    return None


def users_a(db: Session, current:str):
    users = db.execute(select(User.username, User.user_id).where(User.user_id != current)).all()
    return {"users": [{"username": user.username, "id": user.user_id}for user in users]}

def me(db:Session, current:str):
    user = db.execute(select(User.username, User.user_id, User.email).where(User.user_id == current)).all()
    return {"user": [{"username": u.username, "id": u.user_id, "email": u.email}for u in user]}

def find_user(db: Session, search: str):
    users = db.execute(select(User.username, User.user_id).where(User.username.ilike(f"%{search}%"))).all()
    return {"users": [{"username": u.username, "id": u.user_id}for u in users]}

def delete_u(db: Session, user_id:str):
    out = db.get(User, user_id)
    if not out:
        return None
    db.delete(out)
    db.commit()
    return True
    
def promote_user(db: Session, user_id: str):
    user = db.get(User, user_id)
    if not user:
        return None
    user.role = "admin"
    db.commit()
    return True
