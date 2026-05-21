# План улучшения проекта

## Цель

Сделать из MVP нормальное многопользовательское приложение.

## Текущее состояние

```text
Telegram → handlers → .ics / tasks.json
```

Проблемы:

- данные могут быть общими;
- нет нормального разделения пользователей;
- `.ics` парсится повторно;
- JSON неудобен для обновления;
- задачи сложно удалять и завершать.

## Целевая архитектура

```text
Telegram
  ↓
Handlers
  ↓
Services
  ↓
Repositories
  ↓
SQLite
```

## Этап 1. Вынести парсер `.ics`

Создать:

```text
app/parsers/ics_parser.py
```

Парсер должен читать:

- `DTSTART`;
- `DTEND`;
- `SUMMARY`;
- `LOCATION`;
- `DESCRIPTION`;
- `Аудитория:` внутри `DESCRIPTION`;
- `UID`.

## Этап 2. Добавить пользователей

Таблица:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    first_name TEXT,
    created_at TEXT NOT NULL
);
```

При каждом сообщении получать пользователя:

```text
get_or_create_user(message.from_user.id)
```

## Этап 3. Перенести расписание в БД

Таблица:

```sql
CREATE TABLE schedule_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    description TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    source_uid TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

При новой загрузке `.ics`:

1. удалить старое расписание пользователя;
2. распарсить новый файл;
3. сохранить события в БД.

## Этап 4. Перенести задачи в БД

Таблица:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    deadline TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Этап 5. Добавить действия с задачами

- выполнить задачу;
- удалить задачу;
- показать только активные;
- добавить дедлайн.

## Этап 6. Добавить настройки

```sql
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY,
    timezone TEXT DEFAULT 'Europe/Moscow',
    notifications_enabled INTEGER DEFAULT 1,
    reminder_minutes_before INTEGER DEFAULT 15,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Этап 7. Напоминания

Идея:

1. раз в минуту проверять ближайшие пары;
2. если пара скоро начинается — отправлять сообщение;
3. хранить отметку, что напоминание уже отправлено.

## Приоритеты

| Приоритет | Улучшение |
|---|---|
| 1 | Вынести `.ics` парсер |
| 2 | Добавить SQLite |
| 3 | Добавить пользователей |
| 4 | Перенести задачи в БД |
| 5 | Перенести расписание в БД |
| 6 | Добавить удаление задач |
| 7 | Добавить статусы задач |
| 8 | Добавить напоминания |
| 9 | Добавить тесты |

## Итог

Главная цель — чтобы каждый пользователь имел свои данные:

```text
Telegram ID → User → ScheduleItems + Tasks
```
