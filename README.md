### Описание:

Данный проект предназначен для сбора отзывов и выставления рейтинга фильмов, их каталогизации


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:akkrn/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Пример использования API:

После запуска проекта, вы можете ознакомиться с документацией API по адресу: http://127.0.0.1:8000/redoc/
