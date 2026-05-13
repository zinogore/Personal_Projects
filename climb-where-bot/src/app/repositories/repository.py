from sqlalchemy import select
from src.app.core.database import get_db_session
from src.app.models.models import ClimbingGyms, Chats, Visits, Polls

def get_list_of_gym_names():
    with get_db_session() as session:
        result = session.execute(select(ClimbingGyms.gym_name)).scalars().all()
    return result

def store_ids_to_polls(poll_id, chat_id, message_id):
    with get_db_session() as session:
        new_poll = Polls(poll_id=poll_id, chat_id=chat_id, message_id=message_id)
        session.add(new_poll)
    return

def fetch_message_ids_from_polls(chat_id):
    with get_db_session() as session:
        result = session.execute(select(Polls.message_id).where(Polls.chat_id == chat_id)).scalars().all()
    return result

def delete_poll(poll_id):
    with get_db_session() as session:
        result = session.execute(select(Polls).where(Polls.poll_id == poll_id)).scalars().first()
        session.delete(result)
    return

def fetch_chat_ids_from_polls(poll_id):
    with get_db_session() as session:
        result = session.execute(select(Polls.chat_id).where(Polls.poll_id == poll_id)).scalars().first()
    return result

def store_repoll_options(chat_id, repoll_options):
    with get_db_session() as session:
        new_chat = Chats(chat_id=chat_id, repoll_options=repoll_options)
        session.add(new_chat)
    return

def update_repoll_options(chat_id, repoll_options):
    with get_db_session() as session:
        result = session.execute(select(Chats).where(Chats.chat_id == chat_id)).scalars().first()
        result.repoll_options = repoll_options
    return

def fetch_repoll_options(chat_id):
    with get_db_session() as session:
        result = session.execute(select(Chats.repoll_options).where(Chats.chat_id == chat_id)).scalars().first()
    return result