import os

from aiogram import Router, F
from aiogram.types import Message

router = Router()

DATA_DIR = "app/data"
ICS_PATH = os.path.join(DATA_DIR, "schedule.ics")


@router.message(F.text.lower() == "загрузить ics")
async def upload_ics(message: Message):
    await message.answer("Отправь файл с расширением .ics")


@router.message(F.document)
async def handle_ics(message: Message):
    document = message.document

    if not document.file_name or not document.file_name.lower().endswith(".ics"):
        await message.answer("Нужен именно .ics файл")
        return

    os.makedirs(DATA_DIR, exist_ok=True)

    file = await message.bot.get_file(document.file_id)
    await message.bot.download_file(file.file_path, destination=ICS_PATH)

    await message.answer("✅ Расписание загружено и сохранено")
