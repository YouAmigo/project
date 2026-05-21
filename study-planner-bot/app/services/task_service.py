from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(
        self,
        user_id: int,
        title: str,
        category: str,
        deadline,
    ):
        task = Task(
            user_id=user_id,
            title=title,
            category=category,
            deadline=deadline,
        )

        self.session.add(task)
        await self.session.commit()

        return task

    async def get_tasks(self, user_id: int):
        query = select(Task).where(Task.user_id == user_id)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def delete_task(self, task_id: int):
        task = await self.session.get(Task, task_id)

        if task:
            await self.session.delete(task)
            await self.session.commit()