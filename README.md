#  Bewise test task 1

## Инструкция по сборке
1. Перейти в директорию с файлом `docker-compose.yml`
2. Собрать сервис `$ docker compose build`
3. Запустить сервис `$ docker compose up -d`

## Примеры
### Создание пользователя
```
url: http://127.0.0.1:8000/user
method: POST
body: {"name": "username"}
```
Ответ:
```json
{
    "uuid": "52a663e5-2638-43bc-acd0-619c0fe54a4f",
    "name": "username"
}
```
### Создание пользователя
```
url: http://127.0.0.1:8000/record
method: POST
body: wav file
```
Ответ:
```json
{
    "record": {
        "uuid": "d12cfed8-908f-47f9-b6ba-4261f71e2394",
        "user": {
            "uuid": "52a663e5-2638-43bc-acd0-619c0fe54a4f",
            "name": "username"
        },
        "url": "/record?uuid=d12cfed8-908f-47f9-b6ba-4261f71e2394"
    }
}
```
### Получение записи
```
url: http://127.0.0.1:8000/record?uuid=d12cfed8-908f-47f9-b6ba-4261f71e2394
method: GET
```
Ответ:
```
mp3 file
```

### Пример ошибки
```
url: http://127.0.0.1:8000/user
method: POST
body: {"name": ""}
```
Ответ 422
```json
{
    "error": "Name must be longer than 1 char",
    "type": "HTTP_422"
}
```