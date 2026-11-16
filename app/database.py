from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

engine = create_engine("sqlite:///./data.db",
                       connect_args = {"check_same_thread": False})

class Base(DeclarativeBase):
    pass

def get_db():
    with Session(engine) as db_session:
        yield db_session


