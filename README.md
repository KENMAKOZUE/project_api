## Запуск проекта

1. Установи зависимости
```bash
pip install -r requirements.txt
```

2. Запусти приложение
```bash
python3 -m uvicorn main:app --reload
```

3. Открой Swagger UI для тестирования API
```text
http://127.0.0.1:8000/docs
```

4. Примеры доступных маршрутов:
- `POST /api/v1/users/register`
- `POST /api/v1/users/login`
- `POST /api/v1/users/refresh`
- `GET /api/v1/users/protected`

> Токен передаётся в заголовке `Authorization: Bearer <token>`.
# project_api
# project_api
