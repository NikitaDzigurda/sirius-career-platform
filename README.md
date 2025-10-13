# Sirius Career Platform

Платформа для профориентации студентов Университета Сириус и поиска молодых сотрудников для компаний-партнеров.

## Структура проекта

```
/project-root
├── /api  # Backend
│   ├── /app  # Основной код
│   │   ├── /core  # Базовые классы, exceptions
│   │   ├── /db  # Models, sessions
│   │   ├── /routers  # API endpoints
│   │   ├── /schemas  # Pydantic models
│   │   ├── /services  # Бизнес-логика
│   │   ├── /utils  # Утилиты
│   │   ├── main.py  # FastAPI app
│   │   └── config.py  # Settings
│   ├── /tests  # Тесты
│   ├── /alembic  # Миграции
│   └── pyproject.toml  # Зависимости
├── /ml  # Placeholder для ML-моделей
├── /web  # Placeholder для frontend
├── docker-compose.yml  # Для app + db
├── Dockerfile  # Для backend
├── .env.example  # Env vars
└── .gitignore
```

## Установка и запуск

### Требования
- Python 3.12+
- Poetry
- MySQL/MariaDB

### Установка зависимостей
```bash
poetry install
```

### Настройка окружения
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

### Запуск приложения
```bash
poetry run python api/main.py
```

### Запуск с uvicorn
```bash
poetry run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## API документация

После запуска приложения документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Роли пользователей

1. **Студент** - прохождение тестов, получение рекомендаций
2. **Компания** - создание вакансий, поиск кандидатов
3. **Администратор** - управление тестами, аналитика
