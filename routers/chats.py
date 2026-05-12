from fastapi import APIRouter, WebSocketDisconnect, Depends, WebSocket, HTTPException
from database.connection import engine, db
from core.security import get_current, decode_token
from services.chat_services import WebConection, get_conversation, save_message, verify_conversation, conversation_info, verify_users, chats
from sqlalchemy.orm import sessionmaker

manager = WebConection()
router = APIRouter()

LocalSesion = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    

@router.websocket("/ws/{user_id}")
async def message( user_id: str, websocket: WebSocket, current: dict = Depends(get_current)  ):
    
    db = LocalSesion() 

    c_id = get_conversation(db, current, user_id)
    verify = verify_conversation(db, c_id, current)
    if not verify:
        await websocket.close()
        return
    await manager.connect( websocket, c_id)
    try:
        while True:
            
            
            data = await websocket.receive_text()
            
            await manager.message(c_id, data)
            save_message(db, data, c_id, current)
         
            
    except WebSocketDisconnect:
        manager.disconect(c_id, websocket)
    finally:
        db.close()



@router.get("/conversation/{user_id}")
async def conversation(user_id: str, db = Depends(db), current: str = Depends(decode_token)):
    c_id = verify_users(db, current, user_id)
    if not c_id:
        raise HTTPException(status_code=404, detail= "Not Allowed")
    return conversation_info(c_id, db)
    
        
@router.get("/conversations")
async def conversations(current: str = Depends(decode_token), db = Depends(db)):
    chat = chats(current, db)
    return chat
    

        