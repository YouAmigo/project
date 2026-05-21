import os
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message

router = Router()

ICS_FOLDER = "app/data"


def load_all_events():
    events = []

    for file in os.listdir(ICS_FOLDER):
        if not file.endswith(".ics"):
            continue

        path = os.path.join(ICS_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # склеиваем переносы строк в .ics
        fixed_lines = []
        for line in lines:
            line = line.rstrip("\n")

            if line.startswith(" ") and fixed_lines:
                fixed_lines[-1] += line.strip()
            else:
                fixed_lines.append(line)

        event = {}

        for line in fixed_lines:
            line = line.strip()

            if line.startswith("DTSTART"):
                date_str = line.split(":", 1)[1]
                event["start"] = datetime.strptime(date_str[:15], "%Y%m%dT%H%M%S")

            elif line.startswith("DTEND"):
                date_str = line.split(":", 1)[1]
                event["end"] = datetime.strptime(date_str[:15], "%Y%m%dT%H%M%S")

            elif line.startswith("SUMMARY"):
                event["title"] = line.split(":", 1)[1].replace("\\,", ",")

            elif line.startswith("LOCATION"):
                event["location"] = line.split(":", 1)[1].replace("\\,", ",")

            elif line.startswith("DESCRIPTION"):
                desc = line.split(":", 1)[1].replace("\\n", "\n").replace("\\,", ",")

                for desc_line in desc.split("\n"):
                    if desc_line.startswith("Аудитория:"):
                        event["location"] = desc_line.replace("Аудитория:", "").strip()

            if line == "END:VEVENT":
                if "start" in event:
                    event.setdefault("title", "Без названия")
                    event.setdefault("location", "Не указано")
                    events.append(event)

                event = {}

    return events


@router.message(F.text == "сегодня")
async def today_schedule(message: Message):
    today = datetime.now().date()
    events = load_all_events()

    result = "📅 Расписание на сегодня:\n\n"
    found = False

    for event in sorted(events, key=lambda x: x["start"]):
        if event["start"].date() == today:
            found = True

            start = event["start"].strftime("%H:%M")
            end = event["end"].strftime("%H:%M")
            title = event["title"]
            location = event["location"]

            result += (
                f"🕒 {start} - {end}\n"
                f"📚 {title}\n"
                f"📍 {location}\n\n"
            )

    if not found:
        result += "Пар нет 🎉"

    await message.answer(result)


@router.message(F.text == "неделя")
async def week_schedule(message: Message):
    today = datetime.now().date()
    week = today + timedelta(days=7)
    events = load_all_events()

    result = "📆 Расписание на неделю:\n\n"
    found = False

    for event in sorted(events, key=lambda x: x["start"]):
        event_date = event["start"].date()

        if today <= event_date <= week:
            found = True

            day = event["start"].strftime("%d.%m")
            start = event["start"].strftime("%H:%M")
            end = event["end"].strftime("%H:%M")
            title = event["title"]
            location = event["location"]

            result += (
                f"📅 {day}\n"
                f"🕒 {start} - {end}\n"
                f"📚 {title}\n"
                f"📍 {location}\n\n"
            )

    if not found:
        result += "Пар нет 🎉"

    await message.answer(result)


@router.message(F.text == "свободное время")
async def free_time(message: Message):
    today = datetime.now().date()
    events = load_all_events()

    today_events = []

    for event in events:
        if event["start"].date() == today:
            today_events.append(event)

    if not today_events:
        await message.answer("Сегодня весь день свободен 🎉")
        return

    today_events.sort(key=lambda x: x["start"])

    result = "🕓 Свободное время:\n\n"
    found_free_time = False

    for i in range(len(today_events) - 1):
        current_end = today_events[i]["end"]
        next_start = today_events[i + 1]["start"]

        if current_end < next_start:
            found_free_time = True

            result += (
                f"Свободно с "
                f"{current_end.strftime('%H:%M')} "
                f"до "
                f"{next_start.strftime('%H:%M')}\n"
            )

    if not found_free_time:
        result += "Свободного времени между парами нет"

    await message.answer(result)
