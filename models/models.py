from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils.types.choice import ChoiceType
from models.base import Base
from typing import Set
from sqlalchemy_utils import PasswordType
from typing import List
from sqlalchemy.sql import func
import datetime


class User(Base):
    __tablename__ = 'user'

    ROLE = [
        ("Manager", "man"),
        ("Commercial", "com"),
        ("Support", "sup")
    ]

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    password : Mapped[str] = mapped_column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    full_name : Mapped[str] = mapped_column(String(30))
    email : Mapped[str] = mapped_column(String(50), unique=True)
    department : Mapped[str] = mapped_column(String(3), ChoiceType(ROLE))

    clients : Mapped[List['Client']] = relationship(back_populates='commercial_obj')

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

    commercial_obj : Mapped['User'] = relationship(back_populates='clients')
    contracts : Mapped[List["Contract"]] = relationship(back_populates='client')

class Contract(Base):
    __tablename__ = 'contract'

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    client_infos : Mapped[int] = mapped_column(ForeignKey('client.id'))
    commercial : Mapped[int] = mapped_column(ForeignKey('user.id'))
    total_amount : Mapped[int] = mapped_column()
    left_amount : Mapped[int] = mapped_column()
    creation_date : Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status : Mapped[bool] = mapped_column(default=False)

    client : Mapped['Client'] = relationship(back_populates='contracts')
    event : Mapped['Event'] = relationship(back_populates='contract')


class Event(Base):
    __tablename__ = "event"

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    contract_id : Mapped[int] = mapped_column(ForeignKey('contract.id'))
    client : Mapped[int] = mapped_column(ForeignKey('client.id'))
    event_start : Mapped[str] = mapped_column()
    event_end : Mapped[str] = mapped_column()
    support_contact : Mapped[int] = mapped_column(ForeignKey('user.id'))
    location : Mapped[str] = mapped_column()
    attendees : Mapped[int] = mapped_column()
    notes : Mapped[str] = mapped_column()

    contract : Mapped['Contract'] = relationship(back_populates='event')