from fastapi import WebSocket
from database.models import Conversation, Messages, User
from sqlalchemy import select, or_, and_, union
from sqlalchemy.orm import Session
from datetime import datetime
class WebConection:
    def __init__(self):
        self.a_conections: dict[str, WebSocket] = {}

    async def connect(self, websocket : WebSocket, c_id):
        await websocket.accept()

        self.a_conections.setdefault(c_id, []).append(websocket)

    def disconect(self, c_id:str, websocket: WebSocket):
       self.a_conections[c_id].remove(websocket)

    async def message(self, c_id:str, message:str):
        if c_id in self.a_conections:
            for conn in self.a_conections[c_id]:
                await conn.send_text(message)


def get_conversation(db: Session, current: str , user_b: str):
    check = db.execute(select(Conversation.conversation_id).where(
        or_(
            and_(Conversation.user_id_a == current, Conversation.user_id_b == user_b),
            and_(Conversation.user_id_a == user_b, Conversation.user_id_b == current)
        ))).scalar()
    if check:
        return check
    new = Conversation(user_id_a = current, user_id_b = user_b)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new.conversation_id 


def save_message(db: Session,  message: str, c_id: str, sender_id:str):
    new = Messages(sender_id = sender_id, conversation_id = c_id, created_at = datetime.now(), message = message)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new    

def verify_conversation(db: Session, c_id: str, current: str):
    verify = db.execute(select(Conversation).where(Conversation.conversation_id == c_id, or_(
        Conversation.user_id_b == current,
        Conversation.user_id_a == current) )).all()
    if verify:
        return True
    return False

def conversation_info(c_id:str, db: Session):
    data = db.execute(select( User.username, Messages.message_id, Messages.message, Messages.created_at).join(User, Messages.sender_id == User.user_id).where(Messages.conversation_id == c_id )).all()
    return {"messages": [{"from": d.username, "message": d.message, "hour": d.created_at} for d in data]}

def verify_users(db: Session, current: str , user_b: str):
    check = db.execute(select(Conversation.conversation_id).where(
        or_(
            and_(Conversation.user_id_a == current, Conversation.user_id_b == user_b),
            and_(Conversation.user_id_a == user_b, Conversation.user_id_b == current)
        ))).scalar()
    if check:
        return check
    return False
  

def chats(current: str, db: Session):

    b_chats = (select(User.username)
            .select_from(Conversation)
            .join(User, Conversation.user_id_b == User.user_id)
            .where(
                Conversation.user_id_a == current
            ))
    
    a_chats = (select(User.username)
            .select_from(Conversation)
            .join(User, Conversation.user_id_a == User.user_id)
            .where(
                Conversation.user_id_b == current
            ))
    u = union(b_chats, a_chats)
    user_chats = db.execute(u).scalars().all()


    return {"chats": [{"users:": c } for c in user_chats]}