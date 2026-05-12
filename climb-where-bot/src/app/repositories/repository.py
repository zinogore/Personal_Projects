from sqlalchemy import select
from src.app.core.database import get_db_session
from src.app.models.models import ClimbingGyms, Chats, Visits, Polls

def get_list_of_gym_names():
    session = next(get_db_session())
    result = session.execute(select(ClimbingGyms.gym_name)).scalars()
    print(list(result))
    return list(result)

def store_ids(poll_id, chat_id, message_id):
    session = get_db_session()
    new_poll = Polls(poll_id=poll_id, chat_id=chat_id, message_id=message_id)
    session.add(new_poll)
    session.commit()
