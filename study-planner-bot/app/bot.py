import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os

from app.handlers.start import router as start_router
from app.handlers.tasks import router as tasks_router
from app.handlers.upload import router as upload_router
from app.handlers.schedule import router as schedule_router


load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(tasks_router)
dp.include_router(upload_router)
dp.include_router(schedule_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())