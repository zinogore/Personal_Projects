from sqlalchemy import create_engine, Integer, String, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine(r'sqlite:///./instance/database.db', echo=True)

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

class Visits(Base):
    __tablename__ = "visits"
    visit_id: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    gym_id: Mapped[int] = mapped_column(ForeignKey("climbing_gyms.gym_id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))

Base.metadata.create_all(engine)

def get_list_of_gym_names():
    with Session(engine) as session:
        result = session.execute(select(ClimbingGyms.gym_name)).scalars()
        return list(result)
