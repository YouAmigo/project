# Архитектура системы

## Текущий подход

Сейчас проект можно рассматривать как Telegram-бот с файловым хранением:

```text
Telegram → handlers → app/data
```

## Рекомендуемая архитектура

```text
Telegram UI
    ↓
Handlers
    ↓
Services
    ↓
Repositories
    ↓
Storage
```

## Слои

| Слой | Назначение |
|---|---|
| `handlers` | принимают сообщения Telegram |
| `services` | бизнес-логика |
| `parsers` | разбор `.ics` |
| `repositories` | работа с файлами или БД |
| `models` | модели данных |
| `keyboards` | кнопки |
| `data` | файлы и SQLite |

## Рекомендуемая структура

```text
app/
├── bot.py
├── config.py
├── handlers/
│   ├── start.py
│   ├── schedule.py
│   ├── upload.py
│   └── tasks.py
├── keyboards/
│   └── main_menu.py
├── services/
│   ├── schedule_service.py
│   ├── task_service.py
│   └── free_time_service.py
├── parsers/
│   └── ics_parser.py
├── repositories/
│   ├── user_repository.py
│   ├── schedule_repository.py
│   └── task_repository.py
├── models/
│   ├── user.py
│   ├── schedule_item.py
│   └── task.py
└── data/
```

## Правило зависимостей

Правильно:

```text
handler → service → repository → storage
```

Неправильно:

```text
repository → handler
service → Telegram Message
parser → keyboard
```

## Что улучшить

1. Вынести парсинг `.ics` из `handlers`.
2. Создать `IcsParser`.
3. Создать `TaskService` и `ScheduleService`.
4. Добавить `repositories`.
5. Перейти на SQLite.
6. Добавить `user_id` к расписанию и задачам.
