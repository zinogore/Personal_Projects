import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.models.models import Base, Chats, Polls, Visits

# 1. Setup
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session # 2. Execution - This is where the test happens

    # 3. Teardown
    session.close()
    Base.metadata.drop_all(engine)

def test_create_chat_entry(db_session):
    # add chat entry
    new_chat = Chats(chat_id=123, chat_name="chat 123", repoll_options='{"B+ @ Chevy": 0, "BM @ Downtown": 0, "BM @ Bugis": 0, "CC @ Funan": 0, "House of Light": 0, "BFF @ Bendy": 0, "BM @ Rochor": 0}')
    db_session.add(new_chat)
    db_session.commit()

    # query chat entry
    retrieved = db_session.query(Chats).filter_by(chat_id=123).first()
    assert retrieved.chat_name == "chat 123"