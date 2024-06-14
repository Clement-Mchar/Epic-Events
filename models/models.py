from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils.types.choice import ChoiceType
from models.base import Base

from sqlalchemy_utils import PasswordType, force_auto_coercion, EmailType
from typing import List, Set
from sqlalchemy.sql import func
import datetime
import re

force_auto_coercion()


class Role(Base):
    """Sets the model for the role object's creation"""

    __tablename__ = "role"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", String(30), unique=True)
    code: Mapped[str] = mapped_column("code", String(3), unique=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="role")


class User(Base):
    """Sets the model for the user object's creation"""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    password: Mapped[str] = mapped_column(
        "password",
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
        ),
    )

    full_name: Mapped[str] = mapped_column("full_name", String(30))
    email: Mapped[str] = mapped_column("email", EmailType, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    clients: Mapped[List["Client"]] = relationship(back_populates="commercial")

    def __init__(self, full_name, email, role_id, **kwargs):
        self.set_full_name(full_name)
        self.set_email(email)
        self.role_id = role_id
        super().__init__(**kwargs)

    def validate_full_name(self, value):
        if not value:
            raise ValueError("Name field can't be empty.")

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Email is not valid.")

    def validate_role_id(self, value):
        from database import SessionLocal

        session = SessionLocal()
        role = session.query(Role).filter_by(id=value).first()
        session.close()
        if role is None:
            raise ValueError("Invalid role ID.")

    def __repr__(self):
        return (
            f"User(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', role='{self.role}')"
        )

    def set_full_name(self, value):
        self.validate_full_name(value)
        self.full_name = value

    def set_email(self, value):
        self.validate_email(value)
        self.email = value

    def set_role(self, value):
        self.validate_role_id(value)
        self.role = value

    def __repr__(self):
        return (
            f"User(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', role='{self.role}')"
        )


class Client(Base):
    """Sets the model for the client object's creation"""

    __tablename__ = "client"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    full_name: Mapped[str] = mapped_column("full_name", String(30))
    email: Mapped[str] = mapped_column("email", String(50), unique=True)
    telephone: Mapped[int] = mapped_column("telephone", Integer, unique=True)
    business_name: Mapped[str] = mapped_column("business_name", String)
    creation_date: Mapped[datetime.datetime] = mapped_column(
        "creation_date", DateTime(timezone=True), server_default=func.now()
    )
    last_update: Mapped[datetime.datetime] = mapped_column(
        "last_update",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    commercial_contact: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    commercial: Mapped["User"] = relationship(back_populates="clients")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")

    def validate_full_name(self, value):
        if not value:
            raise ValueError("Full name field can't be empty.")

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Email is not valid.")

    def validate_telephone(self, value):
        if not re.match(r"^\d{10}$", str(value)):
            raise ValueError("Telephone number is not valid.")

    def validate_commercial_contact(self, value):
        from database import SessionLocal

        session = SessionLocal()
        commercial = session.query(User).filter_by(id=value).first()
        session.close()
        if commercial is None:
            raise ValueError("Invalid commercial contact ID.")

    def set_full_name(self, value):
        self.validate_full_name(value)
        self.full_name = value

    def set_email(self, value):
        self.validate_email(value)
        self.email = value

    def set_telephone(self, value):
        self.validate_telephone(value)
        self.telephone = value

    def set_commercial_contact(self, value):
        self.validate_commercial_contact(value)
        self.commercial_contact = value

    def __repr__(self):
        return (
            f"Client(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', telephone='{self.telephone}',"
            f" business_name='{self.business_name}')"
        )


class Contract(Base):
    """Sets the model for the contract object's creation"""

    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    client_infos: Mapped[int] = mapped_column(
        "client_infos", ForeignKey("client.id")
    )

    total_amount: Mapped[int] = mapped_column("total_amount", Integer)
    left_amount: Mapped[int] = mapped_column("left_amount", Integer)
    creation_date: Mapped[datetime.datetime] = mapped_column(
        "creation_date", DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[bool] = mapped_column("status", Boolean, default=False)

    client: Mapped["Client"] = relationship(back_populates="contracts")
    event: Mapped["Event"] = relationship(back_populates="contract")

    def validate_client_infos(self, value):
        from database import SessionLocal

        session = SessionLocal()
        client = session.query(Client).filter_by(id=value).first()
        session.close()
        if client is None:
            raise ValueError("Invalid client ID.")

    def validate_commercial(self, value):
        from database import SessionLocal

        session = SessionLocal()
        commercial = session.query(User).filter_by(id=value).first()
        session.close()
        if commercial is None:
            raise ValueError("Invalid commercial contact ID.")

    def validate_amount(self, value):
        if value < 0:
            raise ValueError("Amount cannot be negative.")

    def set_client_infos(self, value):
        self.validate_client_infos(value)
        self.client_infos = value

    def set_commercial(self, value):
        self.validate_commercial(value)
        self.commercial = value

    def set_total_amount(self, value):
        self.validate_amount(value)
        self.total_amount = value

    def set_left_amount(self, value):
        self.validate_amount(value)
        self.left_amount = value

    def __repr__(self):
        return (
            f"Contract(id={self.id}, client_infos={self.client_infos},"
            f" commercial={self.commercial}, total_amount={self.total_amount},"
            f" left_amount={self.left_amount}, status={self.status})"
        )


class Event(Base):
    """Sets the model for the event object's creation"""

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(
        primary_key=True, unique=True, autoincrement=True
    )
    contract_id: Mapped[int] = mapped_column(
        "contract_id", ForeignKey("contract.id")
    )
    client: Mapped[int] = mapped_column("client", ForeignKey("client.id"))
    event_name: Mapped[str] = mapped_column("full_name", String(60))
    event_start: Mapped[str] = mapped_column("event_start", String)
    event_end: Mapped[str] = mapped_column("event_end", String)
    support_contact: Mapped[int] = mapped_column(
        "support_contact", ForeignKey("user.id")
    )
    location: Mapped[str] = mapped_column("location", String)
    attendees: Mapped[int] = mapped_column("attendees", Integer)
    notes: Mapped[str] = mapped_column("notes", String)

    contract: Mapped["Contract"] = relationship(back_populates="event")

    def validate_contract_id(self, value):
        from database import SessionLocal

        session = SessionLocal()
        contract = session.query(Contract).filter_by(id=value).first()
        session.close()
        if contract is None:
            raise ValueError("Invalid contract ID.")

    def validate_client_id(self, value):
        from database import SessionLocal

        session = SessionLocal()
        client = session.query(Client).filter_by(id=value).first()
        session.close()
        if client is None:
            raise ValueError("Invalid client ID.")

    def set_contract_id(self, value):
        self.validate_contract_id(value)
        self.contract_id = value

    def set_client(self, value):
        self.validate_client_id(value)
        self.client = value

    def __repr__(self):
        return (
            f"Event(id={self.id}, contract_id={self.contract_id},"
            f" client={self.client}, event_start='{self.event_start}',"
            f" event_end='{self.event_end}',"
            f" support_contact={self.support_contact},"
            f" location='{self.location}', attendees={self.attendees},"
            f" notes='{self.notes}')"
        )
