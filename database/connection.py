from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from core.settings import settings
engine = create_engine(settings.database_url)

LocalSesion = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def db():
    db = LocalSesion()
    try:
        yield db
    finally:
        db.close()

