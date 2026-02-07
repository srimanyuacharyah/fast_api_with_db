from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE_URL",DATABASE_URL)
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = create_engine(DATABASE_URL)
    try:
        yield db
    finally:
        db.close()