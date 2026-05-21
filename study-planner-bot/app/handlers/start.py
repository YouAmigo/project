from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="загрузить ics")],
        [KeyboardButton(text="➕ добавить задачу")],
        [KeyboardButton(text="мои задачи")],
        [KeyboardButton(text="сегодня")],
        [KeyboardButton(text="неделя")],
        [KeyboardButton(text="свободное время")]
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я бот-планировщик",
        reply_markup=main_menu
    )