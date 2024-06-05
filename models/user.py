from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy_utils.types.choice import ChoiceType
from models.base import Base
from typing import Set
from sqlalchemy_utils import PasswordType
from models.client import Client



class User(Base):
    __tablename__ = 'user'

    ROLE = [
        ("Gestion", "ges"),
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

    clients : Mapped[Set['Client']] = relationship(back_populates='commercial_obj', lazy='deferred')
