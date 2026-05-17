# Python microservices app

Пример приложения на Python из **трех отдельных микросервисов**:
- `api` — REST API для создания и получения задач
- `frontend` — простой web-интерфейс
- `worker` — фоновый обработчик задач

Инфраструктура:
- `postgres` — база данных
- `nginx` — reverse proxy
- `docker compose` — оркестрация локального запуска

## Структура

```text
.
├── api/
├── frontend/
├── worker/
├── nginx/
├── postgres-init/
└── README.md
```

## Как это работает

1. Пользователь открывает приложение через `nginx`.
2. `frontend` отдает HTML-страницу.
3. Фронтенд вызывает `api` по пути `/api/tasks`.
4. `api` сохраняет задачу в `postgres` со статусом `new`.
5. `worker` периодически читает новые задачи и переводит их в статус `done`.

### Проверка здоровья

```bash
curl http://localhost/api/health
```

### Создать задачу

```bash
curl -X POST http://localhost/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"test task"}'
```

### Получить список задач

```bash
curl http://localhost/api/tasks
```

## Сервисы

### api
- Flask + Gunicorn
- Подключается к Postgres через `psycopg2`
- Отдает REST endpoints

### frontend
- Отдельный Python-сервис на Flask
- Отдает HTML/JS
- Работает только через API

### worker
- Отдельный Python-процесс
- Асинхронно обрабатывает записи в таблице `tasks`
- Использует `FOR UPDATE SKIP LOCKED`, чтобы избежать конфликтов при масштабировании

