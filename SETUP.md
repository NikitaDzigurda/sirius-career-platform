# Инструкция по настройке проекта

## Быстрый старт

### 1. Установка зависимостей
```bash
poetry install
```

### 2. Настройка окружения
```bash
cp env.example .env
# Отредактируйте .env файл с вашими настройками
```

### 3. Запуск базы данных
```bash
docker-compose up -d mysql
```

### 4. Создание миграций (когда будут модели)
```bash
cd api
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

### 5. Запуск приложения
```bash
cd api
poetry run python main.py
```

## Структура проекта

```
api/
├── app/
│   ├── core/           # Базовые классы, exceptions, database
│   ├── db/             # SQLAlchemy модели
│   ├── routers/        # API endpoints
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   ├── utils/          # Утилиты
│   ├── middleware/     # Кастомные middleware
│   ├── config.py       # Настройки приложения
│   └── main.py         # Точка входа FastAPI
├── tests/              # Тесты
├── alembic/            # Миграции базы данных
└── main.py             # Запуск приложения
```

## Доступные эндпоинты

- `GET /` - Корневой эндпоинт
- `GET /health/` - Проверка здоровья приложения
- `GET /health/ready` - Проверка готовности
- `GET /health/live` - Проверка жизнеспособности
- `GET /docs` - Swagger UI документация (только в debug режиме)

## Настройка базы данных

### MySQL/MariaDB
Проект настроен для работы с MySQL/MariaDB. Для запуска используйте docker-compose:

```bash
docker-compose up -d mysql
```

### Переменные окружения
Основные переменные в `.env`:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/sirius_career
DEBUG=true
SECRET_KEY=your-secret-key-change-in-production
```

## Разработка

### Добавление новых эндпоинтов
1. Создайте роутер в `app/routers/`
2. Подключите роутер в `main.py`
3. Добавьте схемы в `app/schemas/`

### Добавление моделей БД
1. Создайте модель в `app/db/`
2. Импортируйте модель в `app/core/database.py`
3. Создайте миграцию: `poetry run alembic revision --autogenerate -m "Add model"`
4. Примените миграцию: `poetry run alembic upgrade head`

### Тестирование
```bash
cd api
poetry run pytest
```

## Следующие шаги для разработчика

1. **Создать модели пользователей** (User, Company, Admin)
2. **Реализовать аутентификацию** (JWT + OTP)
3. **Создать CRUD операции** для основных сущностей
4. **Добавить валидацию** через Pydantic схемы
5. **Написать тесты** для основных функций
6. **Настроить логирование** и мониторинг
