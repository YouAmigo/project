# Конфигурация, хранение и ограничения

## `.env`

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=123456789
DATABASE_URL=sqlite:///app/data/app.db
TIMEZONE=Europe/Moscow
```

## Текущее хранение

| Данные | Путь |
|---|---|
| Расписание | `app/data/*.ics` |
| Задачи | `app/data/tasks.json` |

## Проблема MVP

Если ботом пользуются несколько человек, общий файл расписания и общий JSON задач будут смешивать данные.

## Быстрое улучшение без БД

Хранить файлы по Telegram ID:

```text
app/data/users/
├── 111111111/
│   ├── schedule.ics
│   └── tasks.json
└── 222222222/
    ├── schedule.ics
    └── tasks.json
```

## Рекомендуемое улучшение: SQLite

### users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    first_name TEXT,
    created_at TEXT NOT NULL
);
```

### schedule_items

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

### tasks

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

## Индексы

```sql
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_schedule_user_start ON schedule_items(user_id, start_time);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

## Ограничения `.ics`

Парсер должен учитывать:

- переносы строк;
- `\,`;
- `LOCATION`;
- аудиторию в `DESCRIPTION`;
- отсутствие кабинета;
- разные часовые пояса.
