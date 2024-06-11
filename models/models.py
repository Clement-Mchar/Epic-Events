from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_utils.types.choice import ChoiceType
from models.base import Base
from sqlalchemy_utils import PasswordType
from typing import List
from sqlalchemy.sql import func
import datetime
import re

class User(Base):
    """Sets the model for the user object's creation"""

    __tablename__ = "user"

    ROLE = [("Manager", "man"), ("Commercial", "com"), ("Support", "sup")]

    _id: Mapped[int] = mapped_column(
        "_id", primary_key=True, unique=True, autoincrement=True
    )
    _password: Mapped[str] = mapped_column(
        "_password",
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
        ),
    )
    _full_name: Mapped[str] = mapped_column("_full_name", String(30))
    _email: Mapped[str] = mapped_column("_email", String(50), unique=True)
    _department: Mapped[str] = mapped_column(
        "_department", String(3), ChoiceType(ROLE)
    )

    clients: Mapped[List["Client"]] = relationship(
        back_populates="commercial_contact"
    )

    def __init__(self, id, full_name, email, department):
        self._id = id
        self._full_name = full_name
        self._email = email
        self._department = department

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        self._full_name = full_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, department):
        self._validate_role(department)
        self._department = department

    def _validate_role(self, department):
        valid_roles = [role[1] for role in self.ROLE]
        if department not in valid_roles:
            raise ValueError(
                f"Invalid department: {department}. Must be one of"
                f" {valid_roles}"
            )

    def __repr__(self):
        return (
            f"User(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', department='{self.department}')"
        )


class Client(Base):
    """Sets the model for the client object's creation"""

    __tablename__ = "client"

    _id: Mapped[int] = mapped_column(
        "_id", primary_key=True, unique=True, autoincrement=True
    )
    _full_name: Mapped[str] = mapped_column("_full_name", String(30))
    _email: Mapped[str] = mapped_column("_email", String(50), unique=True)
    _telephone: Mapped[int] = mapped_column("_telephone", Integer, unique=True)
    _business_name: Mapped[str] = mapped_column("_business_name", String)
    _creation_date: Mapped[datetime.datetime] = mapped_column(
        "_creation_date", DateTime(timezone=True), server_default=func.now()
    )
    _last_update: Mapped[datetime.datetime] = mapped_column(
        "_last_update",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    _commercial_contact: Mapped[int] = mapped_column(
        "_commercial_contact", ForeignKey("user._id")
    )

    commercial: Mapped["User"] = relationship(back_populates="clients")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="client")

    def __init__(self, id, full_name, email, telephone, business_name):
        self._id = id
        self._full_name = full_name
        self._email = email
        self._telephone = telephone
        self._business_name = business_name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        self._full_name = full_name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._validate_email(email)
        self._email = email

    def _validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email
    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, telephone):
        self._telephone = telephone

    @property
    def business_name(self):
        return self._business_name

    @business_name.setter
    def business_name(self, business_name):
        self._business_name = business_name

    def __repr__(self):
        return (
            f"Client(id={self.id}, full_name='{self.full_name}',"
            f" email='{self.email}', telephone='{self.telephone}',"
            f" business_name='{self.business_name}')"
        )


class Contract(Base):
    """Sets the model for the contract object's creation"""

    __tablename__ = "contract"

    _id: Mapped[int] = mapped_column(
        "_id", primary_key=True, unique=True, autoincrement=True
    )
    _client_infos: Mapped[int] = mapped_column(
        "_client_infos", ForeignKey("client._id")
    )
    _commercial: Mapped[int] = mapped_column(
        "_commercial", ForeignKey("user._id")
    )
    _total_amount: Mapped[int] = mapped_column("_total_amount", Integer)
    _left_amount: Mapped[int] = mapped_column("_left_amount", Integer)
    _creation_date: Mapped[datetime.datetime] = mapped_column(
        "_creation_date", DateTime(timezone=True), server_default=func.now()
    )
    _status: Mapped[bool] = mapped_column("_status", Boolean, default=False)

    client: Mapped["Client"] = relationship(back_populates="contracts")
    event: Mapped["Event"] = relationship(back_populates="contract")

    def __init__(
        self, id, client_infos, commercial, total_amount, left_amount, status
    ):
        self._id = id
        self._client_infos = client_infos
        self._commercial = commercial
        self._total_amount = total_amount
        self._left_amount = left_amount
        self._status = status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def client_infos(self):
        return self._client_infos

    @client_infos.setter
    def client_infos(self, client_infos):
        self._client_infos = client_infos

    @property
    def commercial(self):
        return self._commercial

    @commercial.setter
    def commercial(self, commercial):
        self._commercial = commercial

    @property
    def total_amount(self):
        return self._total_amount

    @total_amount.setter
    def total_amount(self, total_amount):
        self._total_amount = total_amount

    @property
    def left_amount(self):
        return self._left_amount

    @left_amount.setter
    def left_amount(self, left_amount):
        self._left_amount = left_amount

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def __repr__(self):
        return (
            f"Contract(id={self.id}, client_infos={self.client_infos},"
            f" commercial={self.commercial}, total_amount={self.total_amount},"
            f" left_amount={self.left_amount}, status={self.status})"
        )


class Event(Base):
    """Sets the model for the event object's creation"""

    __tablename__ = "event"

    _id: Mapped[int] = mapped_column(
        "_id", primary_key=True, unique=True, autoincrement=True
    )
    _contract_id: Mapped[int] = mapped_column(
        "_contract_id", ForeignKey("contract._id")
    )
    _client: Mapped[int] = mapped_column("_client", ForeignKey("client._id"))
    _event_start: Mapped[str] = mapped_column("_event_start", String)
    _event_end: Mapped[str] = mapped_column("_event_end", String)
    _support_contact: Mapped[int] = mapped_column(
        "_support_contact", ForeignKey("user._id")
    )
    _location: Mapped[str] = mapped_column("_location", String)
    _attendees: Mapped[int] = mapped_column("_attendees", Integer)
    _notes: Mapped[str] = mapped_column("_notes", String)

    contract: Mapped["Contract"] = relationship(back_populates="event")

    def __init__(
        self,
        id,
        contract_id,
        client,
        event_start,
        event_end,
        support_contact,
        location,
        attendees,
        notes,
    ):
        self._id = id
        self._contract_id = contract_id
        self._client = client
        self._event_start = event_start
        self._event_end = event_end
        self._support_contact = support_contact
        self._location = location
        self._attendees = attendees
        self._notes = notes

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def contract_id(self):
        return self._contract_id

    @contract_id.setter
    def contract_id(self, contract_id):
        self._contract_id = contract_id

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client):
        self._client = client

    @property
    def event_start(self):
        return self._event_start

    @event_start.setter
    def event_start(self, event_start):
        self._event_start = event_start

    @property
    def event_end(self):
        return self._event_end

    @event_end.setter
    def event_end(self, event_end):
        self._event_end = event_end

    @property
    def support_contact(self):
        return self._support_contact

    @support_contact.setter
    def support_contact(self, support_contact):
        self._support_contact = support_contact

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def attendees(self):
        return self._attendees

    @attendees.setter
    def attendees(self, attendees):
        self._attendees = attendees

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes

    def __repr__(self):
        return (
            f"Event(id={self.id}, contract_id={self.contract_id},"
            f" client={self.client}, event_start='{self.event_start}',"
            f" event_end='{self.event_end}',"
            f" support_contact={self.support_contact},"
            f" location='{self.location}', attendees={self.attendees},"
            f" notes='{self.notes}')"
        )
