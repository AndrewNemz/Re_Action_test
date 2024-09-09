# Технологии

+ Python 3.12
+ Django 4.2
+ DRF
+ RESTApi
+ Djoser
+ PostgreSQL
+ DRF-Spectacular

# Описание проекта Re_Action

Тестовый проект Re_Action - личный блог, где пользователи могут публиковать посты.
Пользователи могут зарегестрироваться на платформе при помощи e-mail.

# Техническое описание проекта

### Пользовательские роли

+ Аноним — может просматривать посты, также может просмотреть определенный пост, указав его id.
+ Аутентифицированный пользователь (user) — помимо прав Анонимного пользователя, может публиковать посты, редактировать или удалять свои посты
+ Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые посты
+ Администратор (admin) — полные права на управление всем контентом проекта. Может создавать или удалять посты. Может назначать роли пользователям.
+ Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.
  
### Ресурсы Re_Action_test

+ Ресурс auth: аутентификация.
+ Ресурс users: пользователи.
+ Ресурс posts: Просмотр, добавления, удаление или редактирование постов

# Как запустить проект:
### Клонировать репозиторий и перейти в него в командной строке:

```
git git@github.com:AndrewNemz/Re_Action_test.git

cd Re_Action_test
```

### Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

### Для *nix-систем:

```
source venv/bin/activate
```

### Для windows-систем:

```
source venv/Scripts/activate
```

### Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Выполнить миграции:

```
cd personal_blog
python3 manage.py migrate
```

### Создать суперпользователя (для раздачи прав админам):

```
python manage.py createsuperuser
```

### Запустить проект:

```
python manage.py runserver
```

# Примеры запросов:

### Регистрация нового пользователя

#### url:
```
http://127.0.0.1:8000/api/users/
```
POST запрос
```json
 {
    "username": "test user",
    "first_name": "test_name",
    "last_name": "test last_name",
    "password": "test password",
    "email": "test@mail.ru"
}
```

ответ JSON:

```json
{
    "email": "test@mail.ru",
    "id": 4,
    "username": "test user",
    "first_name": "test_name",
    "last_name": "test last_name"
}
```

### Получение токена авторизации

#### url:
```
http://127.0.0.1:8000/api/auth/token/login/
```
POST запрос
```json
{
    "email": "test@mail.ru",
    "password": "test password"
}
```

ответ JSON:

```json
{
  "auth_token": "string"
}

```
### Публикация нового поста (для зарегестрированных пользователей)

#### url:
```
http://127.0.0.1:8000/api/posts/
```
POST запрос
```json
 {
    "post_name": "name test",
    "post_text": "text test "
}
```

ответ JSON:

```json
{
    "id": 1,
    "author": "test user",
    "post_name": "name test",
    "post_text": "text test",
    "created": "2024-09-09T18:38:44.564352Z",
    "post_status": "not_published"
}
```

### Редактирование поста (для зарегестрированных пользователей)

#### url:
```
http://127.0.0.1:8000/api/posts/1/
```
PATCH запрос
```json
 {
    "post_name": "name test patch",
    "post_text": "text test "
}
```

ответ JSON:

```json
{
    "id": 1,
    "author": "test user",
    "post_name": "name test patch",
    "post_text": "text test",
    "created": "2024-09-09T18:38:44.564352Z",
    "post_status": "not_published"
}
```

### Удаление поста (для зарегестрированных пользователей)

#### url:
```
http://127.0.0.1:8000/api/posts/1/
```
DELETE запрос
```json
 {
}
```

ответ JSON:

```json
 {
}
```

### Получение постов (для всех пользователей)
```
http://127.0.0.1:8000/api/posts/
```
GET запрос


ответ JSON:

```json
[
    {
        "id": 2,
        "author": "admin",
        "post_name": "test name",
        "post_text": "test_text dvfddaadv1",
        "created": "2024-09-07T12:25:13.641104Z",
        "post_status": "not_published"
    },
    {
        "id": 3,
        "author": "test user",
        "post_name": "test name",
        "post_text": "test_text",
        "created": "2024-09-07T13:08:36.375082Z",
        "post_status": "not_published"
    },
    {
        "id": 5,
        "author": "test user",
        "post_name": "test name",
        "post_text": "test_text dvfddaadv12",
        "created": "2024-09-07T14:06:14.587749Z",
        "post_status": "published"
    },
]
```

### Получение определенного поста (для всех пользователей)

#### url:
```
http://127.0.0.1:8000/api/posts/1/
```
GET запрос

ответ JSON:

```json
{
    "id": 1,
    "author": "test user",
    "post_name": "name test patch",
    "post_text": "text test",
    "created": "2024-09-09T18:38:44.564352Z",
    "post_status": "not_published"
}
```
