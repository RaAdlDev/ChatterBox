from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import uuid
from sqlalchemy import ForeignKey, String, UniqueConstraint
from datetime import datetime
from typing import List
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "User"
    user_id: Mapped[str] = mapped_column(primary_key= True, default=lambda: str( uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")

  


class Conversation(Base):
    __tablename__ = "Conversation"
    conversation_id: Mapped[str] = mapped_column(primary_key=True, default= lambda: str(uuid.uuid4()))
    user_id_a: Mapped[str]= mapped_column(ForeignKey("User.user_id"))
    user_id_b: Mapped[str]= mapped_column(ForeignKey("User.user_id"))

    __table_args__ = (UniqueConstraint("user_id_a", "user_id_b", name="unique_users_conversation"),)


class Messages(Base):
    __tablename__ = "Messages"
    sender_id: Mapped[str] = mapped_column(ForeignKey("User.user_id"))
    message_id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(ForeignKey("Conversation.conversation_id"))
    message: Mapped[str]
    created_at: Mapped[datetime]





    
