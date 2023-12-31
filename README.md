## Запуск


0. Клонируем репозиторий

```
git clone https://github.com/moonburnt/thefactory_job_interview.git
```

1. Заходим в корневую директорию

```
cd thefactory_job_interview
```

2. Копируем/переименовываем .env.ref в .env

3. Открываем .env, меняем значение TG_TOKEN на токен бота. Например:

```
TG_TOKEN="0000000000:AAAAAAAAAAAAAAAA-AAAAAAAAAAAAAAAA1s"
BOT_HOST="bot"
BOT_PORT=8001
```

3. Запускаем все в докере

```
docker-compose up -d
```

Сервис будет запущен на 8000 порту.


## Тестирование

### Апи эндпоинты

- http://127.0.0.1:8000/ - корень апи
- http://127.0.0.1:8000/auth/register/ - регистрация пользователя в апи
- http://127.0.0.1:8000/auth/login/ - авторизация в веб интерфейсе апи
- http://127.0.0.1:8000/message/ - список сообщений пользователя и отправка новых
- http://127.0.0.1:8000/token/ - токен. Uuid4, генерируется при первом пост-запросе

### Процесс тестирования через интерфейс

- Заходим в /auth/register/, регистрируем пользователя POST-запросом.
- Авторизируемся POST-запросом в /auth/login/
- Переходим на /token/, POST-запросом генерируем токен
- Находим бота в телеграмме, открываем переписку с ним, нажимаем start
- Отправляем боту в телеграм сообщение с токеном (без кавычек)
- Бот отвечает "Successfully attached token '{токен}'"
- Отправляем POST-запросом в /message/ сообщение
- Бот дублирует сообщение из веб интерфейса в телеграмм в формате:
"{имя пользователя}, я получил от тебя сообщение: {сообщение}"
- GET-запросом в /message/ смотрим историю сообщений авторизированного пользователя

## Особенности реализации

- Django 4.2 (ради поддержки асинхронных запросов), drf 3.14
- БД - PostgreSQL (не принципиально, главное чтобы к одной БД был равный доступ
через ОРМ из разных сервисов).
- Микросервисная архитектура: апи для веб интерфейса и асинхронный бот, для
коммуникации используется общая БД через django ORM + запросы на внутренний
интерфейс бота (реализован на aiohttp).
- Бот и веб интерфейс обернуты в отдельные докер контейнеры, управление которыми
(вместе с БД) осуществляется через compose
