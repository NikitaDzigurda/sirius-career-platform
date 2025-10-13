# Sirius Career Platform — Summary & Team Workflow

Этот документ фиксирует каркас проекта, как настроен репозиторий на GitHub (включая CI), правила коммитов и рабочий процесс команды из 4 разработчиков: backend, frontend, ML и тимлид (вы).

## 1. Структура репозитория (монорепо)

```
/project-root
├── api/                 # Backend (FastAPI, Poetry, Pytest)
│   ├── app/
│   │   ├── core/       # базовая инфраструктура, database, exceptions
│   │   ├── routers/    # API endpoints
│   │   ├── schemas/    # Pydantic-схемы
│   │   ├── services/   # бизнес-логика
│   │   ├── utils/      # утилиты
│   │   └── config.py   # настройки
│   ├── tests/          # unit-тесты backend
│   └── main.py         # точка входа FastAPI
├── web/                 # Frontend (placeholder, при появлении — отдельный CI)
├── ml/                  # ML-пакеты/скрипты (placeholder, отдельный CI)
├── .github/workflows/
│   └── ci.yml          # CI для backend (ruff + pytest)
├── Dockerfile           # backend образ (опционально)
├── docker-compose.yml   # локальная разработка (опционально)
├── pyproject.toml       # зависимости backend
├── poetry.lock
├── README.md
├── CI_SETUP.md          # руководство по CI (GitHub Actions)
└── PROJECT_SUMMARY.md   # этот файл
```

План расширения CI для монорепо:
- Добавить `ci-web.yml` (путь-триггеры: `web/**`) и `ci-ml.yml` (`ml/**`).
- Интеграционные проверки — отдельный workflow по метке/расписанию.

## 2. GitHub и защита веток

- Главная ветка: `main` (защищена).
- Ruleset (Settings → Rules):
  - Target: branch pattern `main`.
  - Require a pull request before merging.
  - Require status checks to pass (обязателен workflow “CI”).
  - Block force pushes, Restrict deletions.
  - Bypass: ваш аккаунт — при необходимости экстренных правок.
- Actions (Settings → Actions → General):
  - Allow all actions.
  - Workflow permissions: Read (для текущего CI). Для публикации в GHCR — Read and write.

## 3. CI/CD (минимальный сейчас)

- Workflow: `.github/workflows/ci.yml`.
- Шаги:
  - Poetry install, ruff check --fix + ruff format, pytest `api/tests/`.
- PYTHONPATH в тестах указывает на корень репозитория.
- Расширения по мере роста:
  - backend: mypy, coverage; web: eslint/jest/vitest/build; ml: unit-тесты без тяжёлых данных.

## 4. Правила ветвления и именования

- От `main` создаём короткоживущие ветки:
  - feature/xyz-short-title
  - fix/bug-123
  - chore/infra-thing
  - docs/readme-update
- Для задач в бэк/веб/ML полезно префиксовать областью:
  - feature/api-auth, fix/web-header, feature/ml-preprocess

## 5. Стиль коммитов (Conventional Commits)

Формат: `type(scope): short summary`

- type: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`, `build`, `ci`.
- scope: `api`, `web`, `ml`, `infra`, `deps` и т.д.
- примеры:
  - `feat(api): add health readiness endpoint`
  - `fix(web): prevent double submit on login`
  - `ci(api): enable ruff --fix in workflow`
  - `test(api): add unit tests for /health`

Правила:
- Один коммит — одна логическая единица.
- Сообщение в повелительном наклонении, до 72 символов в summary.
- В описании PR — ссылка на задачу/контекст, скриншоты/ответы API где уместно.

## 6. Процесс Pull Request и ревью (4 разработчика)

Роли:
- Тимлид (вы) — владелец правил, финальное approve, может bypass.
- Backend dev, Frontend dev, ML dev — исполнители своих областей.

Flow на каждый PR:
1) Автор: ветка → коммиты → `push` → PR в `main`.
2) Авто-CI запускается. Пока CI не зелёный — ревью опционально, merge невозможен.
3) Назначение ревьюеров:
   - По области: минимум 1 профильный ревьюер (api/web/ml).
   - Тимлид подключается к ключевым изменениям (архитектура, публичные API, безопасность).
4) Ревьюер смотрит:
   - дизайн/архитектура, читаемость, имена
   - тесты и их достаточность
   - обратная совместимость API/схем
   - секреты/хардкоды/безопасность
5) Статус: `Request changes` или `Approve`.
6) Автор вносит правки, CI зелёный, 1–2 approve → `Squash and merge`.
7) Опционально удаляем feature-ветку.

SLA по ревью:
- В рабочее время: первый фидбек ≤ 4 часа.
- Крупные PR (>400 строк) — разбивать на части.

## 7. Код-стайл и качество

- Python: ruff (исправление и формат), Pydantic v2, явные типы в публичных API.
- Избегать тяжёлых интеграций в unit-тестах; для интеграционных — отдельный workflow.
- Комментарии только там, где важна мотивация/инварианты.

## 8. Локальная разработка

```bash
poetry install
poetry run pre-commit install   # если используете pre-commit
poetry run ruff check api/
poetry run pytest -q api/tests/
```

ENV:
```bash
cp env.example .env
```

## 9. Релизы (базовый сценарий)

- Теги по семвер: `vMAJOR.MINOR.PATCH`.
- Ченджлог — из PR описаний и Conventional Commits.
- Автоматизацию (release notes, build/publish) добавим после стабилизации API.

## 10. Рост монорепозитория

- Добавляем `ci-web.yml`, `ci-ml.yml` с фильтрацией по путям (`paths: [web/**]`, `paths: [ml/**]`).
- В branch protection добавляем required checks: `CI-API`, `CI-WEB`, `CI-ML`.
- Для интеграций создаём `ci-integration.yml` (docker-compose) по кнопке/расписанию.

---
Если потребуется, подготовлю шаблоны для `ci-web.yml` и `ci-ml.yml`, а также `CODEOWNERS` для автоматического назначения ревьюеров по путям.
