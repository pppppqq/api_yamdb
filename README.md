# api_yamdb

API Yamdb - это RESTful API небольшого приложения рейтингов произведений, разработанное на Django REST Framework.

## 📦 Возможности API

- Регистрация и аутентификация пользователей
- Управление произведениями (фильмы, книги и т.д.)
- Добавление отзывов и комментариев
- Система рейтингов
- Разграничение прав доступа (админ, модератор, пользователь)

## 🚀 Как развернуть проект

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/pppppqq/api_yamdb.git
cd .../api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Создать и применить миграции:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Загрузить данные из csv:
```
python manage.py import_data
```
Запустить проект:
```
python3 manage.py runserver
```

## 🔧 Документация к API

После запуска проекта документация станет доступна по ссылке: [ReDoc](http://127.0.0.1:8000/redoc/)
