import json
import os
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()

DATA_DIR = "app/data"
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")


class TaskState(StatesGroup):
    waiting_for_task = State()


def ensure_tasks_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)


def load_tasks():
    ensure_tasks_file()
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    ensure_tasks_file()
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


@router.message(F.text.lower() == "➕ добавить задачу")
async def add_task(message: Message, state: FSMContext):
    await message.answer("Напиши задачу/записку одним сообщением:")
    await state.set_state(TaskState.waiting_for_task)


@router.message(StateFilter(TaskState.waiting_for_task))
async def save_task_handler(message: Message, state: FSMContext):
    tasks = load_tasks()
    tasks.append({
        "text": message.text,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_tasks(tasks)

    await message.answer("✅ Задача добавлена")
    await state.clear()


@router.message(F.text.lower() == "мои задачи")
async def my_tasks(message: Message):
    tasks = load_tasks()

    if not tasks:
        await message.answer("📋 Задач нет")
        return

    text = "📋 Мои задачи:\n\n"
    for index, task in enumerate(tasks, start=1):
        task_text = task.get("text") or task.get("task") or "Без текста"
        created_at = task.get("created_at", "")
        text += f"{index}. {task_text}"
        if created_at:
            text += f"\n   создано: {created_at}"
        text += "\n\n"

    await message.answer(text)
