from fastapi import FastAPI
from routers import auth, chats
from database.models import Base
from database.connection import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan,
        title="ChatterBox API",
        description="API for chatting",
        version="1.0.0")
app.include_router(auth.router)
app.include_router(chats.router)

@app.get("/")
async def root():
    return {"status": "welcome to ChatterBox"}