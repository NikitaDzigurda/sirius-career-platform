# Настройка CI в GitHub Actions

## Обзор Pipeline

CI pipeline состоит из следующих стадий:

### 1. **Lint** - Проверка стиля кода
- **Black** - форматирование кода
- **Ruff** - линтинг и исправление ошибок
- **MyPy** - проверка типов

### 2. **Security** - Проверка безопасности
- **Bandit** - поиск уязвимостей в коде
- **Safety** - проверка уязвимостей в зависимостях

### 3. **Test** - Запуск тестов
- **Pytest** - unit тесты
- **Coverage** - отчет о покрытии кода
- **MySQL** - тестовая база данных

### 4. **Build** - Сборка и публикация образа
- **Docker** - создание образа приложения
- **GHCR** - загрузка в GitHub Container Registry

### 5. **Deploy** - Развертывание (будущее)
- **Staging** - тестовое развертывание
- **Production** - продакшн развертывание

## Настройка в GitHub

### 1. Создание репозитория и пуш исходников
- Создайте репозиторий в GitHub (без автогенерации README)
- Подключите локальный проект:
```
git remote remove origin || true
git remote add origin https://github.com/<your-username>/sirius-career-platform.git
git branch -M main
git push -u origin main
```

### 2. Включение GitHub Actions
- Откройте вкладку Actions и подтвердите запуск workflow при первом пуше/PR

### 3. Настройка GHCR (Container Registry)
- Settings → Actions → General → Workflow permissions → Read and write
- Публикация образов выполняется автоматически через `GITHUB_TOKEN`
- Итоговые теги:
  - `ghcr.io/<owner>/<repo>:<sha>`
  - `ghcr.io/<owner>/<repo>:latest`

## Локальная настройка

### 1. Установка pre-commit hooks

```bash
# Установить зависимости
poetry install

# Установить pre-commit hooks
poetry run pre-commit install

# Запустить проверки вручную
poetry run pre-commit run --all-files
```

### 2. Локальный запуск проверок

```bash
# Форматирование кода
poetry run black api/

# Линтинг
poetry run ruff check api/

# Проверка типов
poetry run mypy api/

# Безопасность
poetry run bandit -r api/

# Тесты
poetry run pytest api/tests/
```

## Правила работы с Pipeline

### ✅ Что разрешено:
- **Merge Request** - автоматически запускает CI
- **Push в main** - запускает полный pipeline
- **Push в develop** - запускает полный pipeline

### ❌ Что блокирует merge:
- **Падающие тесты** - исправьте тесты
- **Ошибки линтеров** - исправьте стиль кода
- **Проблемы безопасности** - исправьте уязвимости
- **Ошибки сборки** - исправьте код

### 🔄 Автоматические действия:
- **Форматирование** - Black автоматически форматирует код
- **Исправления** - Ruff автоматически исправляет простые ошибки
- **Кэширование** - Poetry и pip кэшируются для ускорения

## Мониторинг Pipeline

### 1. Статус в GitHub Actions:
- **Зеленый** ✅ - все проверки прошли
- **Красный** ❌ - есть ошибки
- **Желтый** ⏳ - выполняется
- **Серый** ⏸️ - ожидает

### 2. Уведомления:
- **Email** - при падении pipeline
- **Slack** - интеграция с командой
- **GitHub Actions** - в интерфейсе репозитория

### 3. Артефакты:
- **Coverage report** - отчет о покрытии тестами
- **Security reports** - отчеты о безопасности
- **Docker images** - собранные образы

## Troubleshooting

### Частые проблемы:

#### 1. Pipeline не запускается
- Проверьте включение GitHub Actions в Settings → Actions
- Проверьте синтаксис `.github/workflows/ci.yml`

#### 2. Тесты падают
- Проверьте подключение к MySQL
- Проверьте переменные окружения
- Запустите тесты локально

#### 3. Docker build падает
- Проверьте Dockerfile
- Проверьте доступ к GHCR (Workflow permissions: write)
- Проверьте размер образа

#### 4. Линтеры падают
- Запустите `poetry run black api/`
- Запустите `poetry run ruff check --fix api/`
- Проверьте настройки в pyproject.toml

## Расширение Pipeline

### Добавление новых проверок:

1. **Новый линтер:**
```yaml
new-linter:
  stage: lint
  script:
    - poetry run new-linter api/
```

2. **Новые тесты:**
```yaml
integration-tests:
  stage: test
  script:
    - poetry run pytest tests/integration/
```

3. **Новая стадия:**
```yaml
stages:
  - lint
  - test
  - security
  - build
  - new-stage  # Добавить новую стадию
```

## Best Practices

### 1. Для разработчиков:
- **Маленькие MR** - легче ревьюить и тестировать
- **Понятные коммиты** - что и зачем изменено
- **Тесты** - покрывайте новый код тестами
- **Документация** - обновляйте при изменениях

### 2. Для Team Lead:
- **Мониторинг** - следите за статусом pipeline
- **Быстрые фиксы** - исправляйте падающие pipeline
- **Обучение** - объясняйте команде правила
- **Оптимизация** - улучшайте скорость pipeline

### 3. Для команды:
- **Коммуникация** - сообщайте о проблемах
- **Обучение** - изучайте инструменты качества
- **Стандарты** - следуйте принятым стандартам
- **Итерации** - улучшайте процесс разработки
