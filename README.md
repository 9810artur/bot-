# LocalAdsBot

Маркетплейс рекламы между бизнесом и блогерами на базе Telegram.

## Описание проекта

LocalAdsBot — это Telegram-бот, который объединяет бизнес и блогеров:

- **Бизнес** публикует рекламные кампании
- **Блогеры** получают уведомления и подают заявки
- **Бизнес** выбирает блогеров для сотрудничества

## Технологический стек

- **Python 3.12** — основной язык
- **Aiogram 3.x** — фреймворк для Telegram Bot API
- **PostgreSQL** — база данных
- **SQLAlchemy 2.x** — ORM
- **Alembic** — управление миграциями БД
- **Docker & Docker Compose** — контейнеризация
- **Python-dotenv** — управление переменными окружения

## Архитектура

```
src/
├── config/              # Конфигурация приложения
├── database/            # Работа с БД
│   ├── models/          # SQLAlchemy модели
│   └── migrations/       # Alembic миграции
├── handlers/            # Обработчики команд и сообщений
├── services/            # Бизнес-логика
├── repositories/        # Data Access Layer
├── middlewares/         # Middleware для обработки запросов
├── states/              # FSM состояния для форм
├── keyboards/           # Клавиатуры и кнопки
├── utils/               # Утилиты и вспомогательные функции
└── main.py              # Точка входа приложения
```

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.12+ (для локального разработки)
- PostgreSQL (используется в контейнере)

### 1. Клонирование репозитория

```bash
git clone https://github.com/9810artur/bot-.git
cd bot-
```

### 2. Создание файла .env

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте ваш `BOT_TOKEN` из BotFather.

### 3. Запуск с Docker Compose

```bash
docker-compose up -d
```

Приложение автоматически:
- Создаст БД
- Применит миграции
- Запустит бота

### 4. Локальная разработка

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск миграций
alembic upgrade head

# Запуск приложения
python -m src.main
```

## Структура проекта

### `src/config/`
Конфигурация приложения: переменные окружения, параметры бота, БД.

### `src/database/`
- `models/` — SQLAlchemy модели (User, Campaign, Application)
- Сессии и подключение к БД

### `src/handlers/`
Обработчики команд и сообщений от пользователей.

### `src/services/`
Бизнес-логика приложения.

### `src/repositories/`
Data Access Layer для работы с БД (Repository Pattern).

### `src/middlewares/`
Middleware для логирования, проверки прав доступа и т.д.

### `src/states/`
Определение состояний FSM для пошаговых форм.

### `src/keyboards/`
Инлайн и обычные клавиатуры для управления ботом.

### `src/utils/`
Утилиты: парсеры, валидаторы, помощники.

## Логирование

Логирование настроено в `src/config/logging_config.py`:
- Логи выводятся в консоль и файл
- Уровень логирования настраивается через переменную `LOG_LEVEL`

## База данных

### Миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат на предыдущую версию
alembic downgrade -1
```

### Подключение

BD подключается через `src/database/__init__.py` с использованием SQLAlchemy.

## Разработка

### Форматирование кода

```bash
black src/
flake8 src/
mypy src/
```

### Тестирование

```bash
pytest
```

## Лицензия

MIT

## Контакты

Автор: 9810artur
