# Диаграмма классов

```mermaid
classDiagram
    class User {
        int id
        int telegram_id
        str username
        datetime created_at
    }

    class ScheduleItem {
        int id
        int user_id
        str title
        str location
        str description
        datetime start_time
        datetime end_time
        str source_uid
    }

    class Task {
        int id
        int user_id
        str text
        str status
        datetime deadline
        datetime created_at
    }

    class FreeTimeSlot {
        datetime start_time
        datetime end_time
        int duration_minutes
    }

    class IcsParser {
        parse(file_path)
        extract_location(location, description)
        unfold_lines(lines)
    }

    class ScheduleService {
        get_today(user_id)
        get_week(user_id)
        get_free_time_today(user_id)
    }

    class TaskService {
        add_task(user_id, text)
        get_tasks(user_id)
        complete_task(user_id, task_id)
    }

    User "1" --> "many" ScheduleItem
    User "1" --> "many" Task
    ScheduleService --> ScheduleItem
    TaskService --> Task
    ScheduleService --> FreeTimeSlot
    IcsParser --> ScheduleItem
```

## Основные классы

### User

Пользователь Telegram-бота.

### ScheduleItem

Одна учебная пара. Обязательно содержит время, название и место.

### Task

Задача пользователя. В будущем может иметь статус и дедлайн.

### FreeTimeSlot

Свободный промежуток между парами.

### IcsParser

Отвечает только за парсинг `.ics`.

### ScheduleService

Отвечает за расписание: сегодня, неделя, свободное время.

### TaskService

Отвечает за добавление и просмотр задач.
