Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

## Запуск проекта:

```
python3 manage.py runserver
```

## Документация по API:
```

http://127.0.0.1:8000/redoc/
```

## Для работы с API необходима авторизация:

