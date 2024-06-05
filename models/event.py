from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm import relationship
from models.base import Base
from models import contract, client, user
from sqlalchemy.sql import func
import datetime

class Event(Base):
    __tablename__ = "event"

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    contract : Mapped[int] = mapped_column(ForeignKey('contract.id'))
    client : Mapped[str] = mapped_column(ForeignKey('client.id'))
    event_start : Mapped[str] = mapped_column()
    event_end : Mapped[str] = mapped_column()
    support_contact : Mapped[str] = mapped_column(ForeignKey('user.id'))
    location : Mapped[str] = mapped_column()
    attendees : Mapped[int] = mapped_column()
    notes : Mapped[str] = mapped_column()

    contract : Mapped["contract.Contract"] = relationship(back_populates='event', lazy='deferred')

