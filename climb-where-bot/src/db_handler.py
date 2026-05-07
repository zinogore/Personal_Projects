from sqlalchemy import create_engine, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine(r'sqlite:///./instance/database.db', echo=True)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class ClimbingGyms(Base):
    __tablename__ = "climbing_gyms"
    gym_id: Mapped[int] = mapped_column(primary_key=True)
    gym_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    location: Mapped[str] = mapped_column(String(50), nullable=True)

class Chats(Base):
    __tablename__ = "chats"
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    chat_name: Mapped[str] = mapped_column(String(30), nullable=True)
    repoll_options: Mapped[str] = mapped_column(String(250), nullable=True)

class Visits(Base):
    __tablename__ = "visits"
    visit_id: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    gym_id: Mapped[int] = mapped_column(ForeignKey("climbing_gyms.gym_id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))

class Polls():
    __tablename__ = "polls"
    poll_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)

# create tables
Base.metadata.create_all(engine)

def get_list_of_gym_names():
    with Session() as session:
        result = session.execute(select(ClimbingGyms.gym_name)).scalars()
        return list(result)

def store_ids(poll_id, chat_id, message_id):
    with Session() as session:
        new_poll = Polls(poll_id=poll_id, chat_id=chat_id, message_id=message_id)
        session.add(new_poll)
        session.commit()


# create polls table
# store ids in polls table
# remove ids in polls table
# store repoll options in chats table