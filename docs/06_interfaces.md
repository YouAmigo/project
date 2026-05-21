# Интерфейсы и контракты

## IIcsParser

```python
class IIcsParser:
    def parse(self, file_path: str) -> list:
        pass

    def extract_location(self, location: str, description: str) -> str:
        pass
```

Парсер возвращает список событий:

```python
[
    {
        "title": "ИИТ / Лекция 15",
        "start": datetime,
        "end": datetime,
        "location": "Online"
    }
]
```

## IScheduleRepository

```python
class IScheduleRepository:
    async def save_many(self, user_id: int, items: list):
        pass

    async def get_today(self, user_id: int, date):
        pass

    async def get_between(self, user_id: int, start_date, end_date):
        pass

    async def delete_user_schedule(self, user_id: int):
        pass
```

## ITaskRepository

```python
class ITaskRepository:
    async def add(self, user_id: int, text: str):
        pass

    async def get_all(self, user_id: int):
        pass

    async def mark_done(self, user_id: int, task_id: int):
        pass

    async def delete(self, user_id: int, task_id: int):
        pass
```

## IUserRepository

```python
class IUserRepository:
    async def get_or_create(self, telegram_id: int, username: str | None):
        pass
```

## IScheduleService

```python
class IScheduleService:
    async def import_ics(self, user_id: int, file_path: str):
        pass

    async def get_today_text(self, user_id: int) -> str:
        pass

    async def get_week_text(self, user_id: int) -> str:
        pass

    async def get_free_time_text(self, user_id: int) -> str:
        pass
```

## Зачем это нужно

Интерфейсы позволят заменить JSON и `.ics` на SQLite без полного переписывания handlers.
