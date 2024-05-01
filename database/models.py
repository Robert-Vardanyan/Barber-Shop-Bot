from sqlalchemy import DateTime, String, Text,  Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import datetime

class Base(DeclarativeBase):

    last_order: Mapped[DateTime] = mapped_column(DateTime, default= datetime.datetime(2022, 2, 22))
    reg: Mapped[DateTime] = mapped_column(DateTime, default= func.now())


class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    n_order = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    mail: Mapped[str] = mapped_column(String(150), nullable=False)
    verify: Mapped[str] = mapped_column(String(150), nullable=True)
