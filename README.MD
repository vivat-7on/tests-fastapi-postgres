# Tests FastAPI + PostgreSQL

Учебный проект для практики тестирования FastAPI-приложений с базой данных PostgreSQL и Docker.

## Стек технологий
- Python 3.11
- FastAPI
- PostgreSQL
- Docker + docker-compose
- Pytest
- Httpx
- Asgi-lifespan
- pytest-asyncio

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/vivat-7on/tests-fastapi-postgres.git
cd tests-fastapi-postgres
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите PostgreSQL через Docker:

```bash
docker-compose up -d
```

5. Запустите приложение:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## Тестирование

Запуск всех тестов:

```bash
pytest
```

Запуск отдельно юнит-тестов:

```bash
pytest -m unit
```

Запуск отдельно интеграционных тестов:

```bash
pytest -m integration
```

## Структура проекта

```
app/
    main.py
    database.py
tests/
    unit/
        test_main.py
    integrations/
        test_user_api.py
.env
docker-compose.yml
pytest.ini
requirements.txt
```

---

# 📢 Примечания

- Используется PostgreSQL в Docker-контейнере
- Отдельные юнит-тесты (TestClient)
- Отдельные интеграционные асинхронные тесты (httpx.AsyncClient)
- Тестирование обрабатывает как позитивные, так и негативные сценарии

---

# 🚀 Цель проекта

Научиться правильно тестировать асинхронные FastAPI-приложения с реальной базой данных.

---

# 🚀 Автор

[vivat-7on](https://github.com/vivat-7on)

