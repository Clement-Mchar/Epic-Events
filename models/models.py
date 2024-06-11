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
class User(Base):
    """Sets the model for the user object's creation"""

    __tablename__ = "user"

    ROLE = [("Manager", "man"), ("Commercial", "com"), ("Support", "sup")]

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True
    )
    password: Mapped[str] = mapped_column(
        "password", PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
        )
    )
    full_name: Mapped[str] = mapped_column("full_name", String(30))
    email: Mapped[str] = mapped_column("email", EmailType, unique=True)
    department: Mapped[str] = mapped_column(
        "department", String(3), ChoiceType(ROLE)
    )

    clients: Mapped[Set["Client"]] = relationship(
        back_populates="commercial"
    )

    def __init__(self, full_name, email, department, **kwargs):
        self.set_full_name(full_name)
        self.set_email(email)
        self.set_department(department)
        super().__init__(**kwargs)

    def validate_full_name(self, value):
        if not value:
            raise ValueError("Name field can't be empty.")
    
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Email is not valid.")
    
    def validate_department(self, value):
        if value not in [role[1] for role in User.ROLE]:
            raise ValueError("This department doesn't exist.")

    def set_full_name(self, value):
        self.validate_full_name(value)
        self.full_name = value

    def set_email(self, value):
        self.validate_email(value)
        self.email = value
    
    def set_department(self, value):
        self.validate_department(value)
        self.department = value 

    def __repr__(self):
        return (
            f"User(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', department='{self.department}')"
        )


class Client(Base):
    """Sets the model for the client object's creation"""

    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True
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
        "commercial_contact", ForeignKey("user.id")
    )

    commercial: Mapped["User"] = relationship(back_populates="clients")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")

    def __repr__(self):
        return (
            f"Client(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', telephone='{self.telephone}',"
            f" business_name='{self.business_name}')"
        )


class Contract(Base):
    """Sets the model for the contract object's creation"""

    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True
    )
    client_infos: Mapped[int] = mapped_column(
        "client_infos", ForeignKey("client.id")
    )
    commercial: Mapped[int] = mapped_column(
        "commercial", ForeignKey("user.id")
    )
    total_amount: Mapped[int] = mapped_column("total_amount", Integer)
    left_amount: Mapped[int] = mapped_column("left_amount", Integer)
    creation_date: Mapped[datetime.datetime] = mapped_column(
        "creation_date", DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[bool] = mapped_column("status", Boolean, default=False)

    client: Mapped["Client"] = relationship(back_populates="contracts")
    event: Mapped["Event"] = relationship(back_populates="contract")

    def __repr__(self):
        return (
            f"Contract(id={self.id}, client_infos={self.client_infos},"
            f" commercial={self.commercial}, total_amount={self.total_amount},"
            f" left_amount={self.left_amount}, status={self.status})"
        )


class Event(Base):
    """Sets the model for the event object's creation"""

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True
    )
    contract_id: Mapped[int] = mapped_column(
        "contract_id", ForeignKey("contract.id")
    )
    client: Mapped[int] = mapped_column("client", ForeignKey("client.id"))
    event_start: Mapped[str] = mapped_column("event_start", String)
    event_end: Mapped[str] = mapped_column("event_end", String)
    support_contact: Mapped[int] = mapped_column(
        "support_contact", ForeignKey("user.id")
    )
    location: Mapped[str] = mapped_column("location", String)
    attendees: Mapped[int] = mapped_column("attendees", Integer)
    notes: Mapped[str] = mapped_column("notes", String)

    contract: Mapped["Contract"] = relationship(back_populates="event")

    def __repr__(self):
        return (
            f"Event(id={self.id}, contract_id={self.contract_id},"
            f" client={self.client}, event_start='{self.event_start}',"
            f" event_end='{self.event_end}',"
            f" support_contact={self.support_contact},"
            f" location='{self.location}', attendees={self.attendees},"
            f" notes='{self.notes}')"
        )