from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base import Base
import datetime
from models import client
from models.event import Event

class Contract(Base):
    __tablename__ = 'contract'

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    client_infos : Mapped[str] = mapped_column(ForeignKey('client.id'))
    commercial : Mapped[int] = mapped_column(ForeignKey('user.id'))
    total_amount : Mapped[int] = mapped_column()
    left_amount : Mapped[int] = mapped_column()
    creation_date : Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status : Mapped[bool] = mapped_column(default=False)

    client : Mapped['client.Client'] = relationship(back_populates='contracts', lazy='deferred')

    event : Mapped['Event'] = relationship(back_populates='contract', lazy='deferred')