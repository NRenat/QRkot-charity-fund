# Приложение QRKot

Благотворительный фонд QRKot создан для поддержки и помощи котикам. Фонд предоставляет возможность создания проектов, каждый из которых имеет уникальное название, описание и целевую сумму для сбора. После достижения необходимой суммы проект считается завершенным и закрывается.

Google Sheets используются для формирования отчета по проектам.


Документация к API хранится в [openapi.json](openapi.json).

## Запуск

* Установить зависимости 
```bash
pip install -r requirements.txt
```

* Шаблон переменных окружения можно найти тут: [жмяк](.env.example)

* Инициализировать Alembic

```bash
alembic init --template async alembic
```

* Применение миграций

```bash
alembic upgrade head
```

* Запуск приложения 

```bash
uvicorn app.main:app
```

## Технологии
* Python 3.9
* FastAPI
* SQLAlchemy
* Pydantic
* Google Sheets API
* uvicorn
