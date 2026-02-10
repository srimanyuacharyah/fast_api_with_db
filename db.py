from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
sessionlocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    if not sessionlocal:
        raise ValueError("DATABASE_URL environment variable is not set")
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()