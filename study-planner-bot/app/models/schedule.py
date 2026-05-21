from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime
from sqlalchemy import String

from app.database import Base


class ScheduleItem(Base):
    __tablename__ = "schedule_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]

    subject: Mapped[str] = mapped_column(String(255))
    room: Mapped[str] = mapped_column(String(100))

    start_time: Mapped[DateTime]
    end_time: Mapped[DateTime]