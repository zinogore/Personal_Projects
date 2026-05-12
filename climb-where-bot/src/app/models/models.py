from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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

class Polls(Base):
    __tablename__ = "polls"
    poll_id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)