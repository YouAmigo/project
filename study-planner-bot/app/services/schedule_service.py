from sqlalchemy import select
from datetime import datetime

from app.models.schedule import ScheduleItem


class ScheduleService:

    def __init__(self, session):
        self.session = session

    async def get_today_schedule(self, user_id: int):
        today = datetime.now().date()

        query = select(ScheduleItem).where(
            ScheduleItem.user_id == user_id
        )

        result = await self.session.execute(query)

        lessons = result.scalars().all()

        return [
            lesson
            for lesson in lessons
            if lesson.start_time.date() == today
        ]

    async def save_schedule(self, user_id: int, lessons: list):
        for lesson in lessons:
            item = ScheduleItem(
                user_id=user_id,
                subject=lesson["subject"],
                room=lesson["room"],
                start_time=lesson["start"],
                end_time=lesson["end"],
            )

            self.session.add(item)

        await self.session.commit()