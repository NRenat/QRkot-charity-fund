# Приложение QRKot

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

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