# Domain-модели, DTO и маппинг

## Текущие структуры MVP

### Событие расписания

```python
event = {
    "start": datetime,
    "end": datetime,
    "title": str,
    "location": str
}
```

### Задача

```python
task = {
    "id": int,
    "text": str,
    "created_at": str
}
```

## Модели для улучшенной версии

### User

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | внутренний ID |
| `telegram_id` | int | Telegram ID |
| `username` | str | username |
| `created_at` | datetime | дата создания |

### ScheduleItem

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | ID пары |
| `user_id` | int | владелец |
| `title` | str | название |
| `location` | str | кабинет или Online |
| `description` | str | описание из `.ics` |
| `start_time` | datetime | начало |
| `end_time` | datetime | конец |
| `source_uid` | str | UID из `.ics` |

### Task

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | ID задачи |
| `user_id` | int | владелец |
| `text` | str | текст |
| `status` | str | `active` или `done` |
| `deadline` | datetime | дедлайн |
| `created_at` | datetime | дата создания |

## Маппинг `.ics` → ScheduleItem

| `.ics` | Domain |
|---|---|
| `SUMMARY` | `title` |
| `DTSTART` | `start_time` |
| `DTEND` | `end_time` |
| `LOCATION` | `location` |
| `DESCRIPTION` | `description` |
| `UID` | `source_uid` |

## Правило кабинета

```text
если есть LOCATION:
    location = LOCATION
иначе если DESCRIPTION содержит "Аудитория:":
    location = значение после "Аудитория:"
иначе:
    location = "Не указано"
```

## Инварианты

### ScheduleItem

- `start_time < end_time`;
- `title` не пустой;
- `location` может быть `Не указано`;
- после подключения БД нужен `user_id`.

### Task

- `text` не пустой;
- `status` только `active` или `done`;
- задача принадлежит пользователю.
