### foodgram-project ###
Проект foodgram является web-приложением для любителей готовить различные блюда.
Пользователи могут ознакоимиться с рецептами других пользователей, зарегистировать
и выложить свой рецепт. Имеется возможность подписки на полюбившихся авторов рецептов,
добавление понравившихся рецептов в избранное. Есть возможность фильтрации рецптов, а также
поиска инргедиента по имени. Есть возможность добавить понравившееся рецепты в список покупок,
скачать список необходимых продуктов и ингредиентов в текстовом формате.


### Как запустить проект при помощи Docker на локальном ПК: ###
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Alexandrsgit/foodgram-project-react.git
```

В корне проекта создать файл .env и заполнить его:
```
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
SECRET_KEY=Your_secret_key
```

в папке infra выполнить команду:
```
docker compose up -d
```

Выполнить миграции и добавить данные в БД:
```
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic

```

Создайте суперпользователя для доступа в admin-зону и скопируйте статику:
```
docker exec -it backend  python manage.py createsuperuser
docker compose exec -it backend bash
cp -r /app/collected_static/. /foodgram_backend_static/static/
```


### Как запустить проект без помощи Docker: ###
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Alexandrsgit/foodgram-project-react.git
```

Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
cd backend/
pip install -r requirements.txt
```

Выполнить миграции и добавить данные в БД:
```
python manage.py makemigrations
python manage.py migrate
python manage.py import_data
```

Создайте суперпользователя для доступа в admin-зону и запустить проект:
```
python manage.py createsuperuser
python manage.py runserver
```



### URL-адреса для работы с проектом: ###
```
Главная страница проекта - http://127.0.0.1:80
Админ зона проеката - http://127.0.0.1:8000/admin/
Список API поинтов - http://127.0.0.1:8000/api/
Документация работы API поинтов - http://127.0.0.1:8000/api/docs/
```