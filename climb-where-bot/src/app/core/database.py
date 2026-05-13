from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.models import Base, ClimbingGyms
import json
from contextlib import contextmanager

# engine = create_engine(r'sqlite:///./instance/database.db', echo=True) # higher verbose
engine = create_engine(r'sqlite:///./instance/database.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # create tables
    Base.metadata.create_all(engine)

@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def populate_gym_names():
    with open("./scripts/database.json") as file:
        data = json.load(file)

    all_gyms_names = [ele.get("name") for ele in data["data"]["climbing_gyms"]]
    print(all_gyms_names)

    for gym_name in all_gyms_names:
        session = next(get_db_session())
        new_gym = ClimbingGyms(gym_name=gym_name)
        session.add(new_gym)
        session.commit()