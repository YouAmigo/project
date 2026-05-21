# Диаграмма компонентов

## MVP

```mermaid
flowchart TD
    User[Пользователь Telegram]
    Bot[Telegram Bot]
    Handlers[Handlers]
    Ics[ICS файл]
    Json[tasks.json]

    User --> Bot
    Bot --> Handlers
    Handlers --> Ics
    Handlers --> Json
```

## Улучшенная версия

```mermaid
flowchart TD
    User[Пользователь Telegram]
    Bot[Telegram Bot API]
    Handlers[Handlers]
    Services[Services]
    Parsers[Parsers]
    Repositories[Repositories]
    DB[(SQLite)]

    User --> Bot
    Bot --> Handlers
    Handlers --> Services
    Services --> Parsers
    Services --> Repositories
    Repositories --> DB
```

## Компоненты

| Компонент | Назначение |
|---|---|
| Telegram UI | кнопки и сообщения |
| Handlers | обработка действий пользователя |
| Services | бизнес-логика |
| IcsParser | чтение `.ics` |
| Repositories | доступ к данным |
| SQLite | хранение пользователей, задач и расписания |

## Главное улучшение

Сейчас данные могут быть общими. После улучшения должно быть так:

```text
User 1 → свои задачи → своё расписание
User 2 → свои задачи → своё расписание
```
