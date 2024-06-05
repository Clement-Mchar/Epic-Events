from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, deferred
from models.base import Base
from typing import Set
from sqlalchemy.sql import func
import datetime
from models import contract, user

class Client(Base):
    __tablename__ = 'client'

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    full_name :  Mapped[str] = mapped_column(String(30))
    email : Mapped[str] = mapped_column(String(50), unique=True)
    telephone : Mapped[int] = mapped_column(unique=True)
    business_name : Mapped[str] = mapped_column()
    creation_date : Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_update : Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    commercial : Mapped[int] = mapped_column(ForeignKey('user.id'))

    commercial_obj : Mapped['user.User'] = relationship(back_populates='clients', lazy='deferred')
    contracts : Mapped[Set["contract.Contract"]] = relationship(back_populates='client', lazy='deferred')