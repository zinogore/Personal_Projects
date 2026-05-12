from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.models import Base

engine = create_engine(r'sqlite:///./instance/database.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # create tables
    Base.metadata.create_all(engine)

def get_db_session():
    with SessionLocal() as session:
        yield session