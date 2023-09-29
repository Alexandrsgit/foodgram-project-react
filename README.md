### foodgram-project ###
Проект foodgram является web-приложением для любителей готовить различные блюда.
Пользователи могут ознакоимиться с рецептами других пользователей, зарегистировать
и выложить свой рецепт. Имеется возможность подписки на полюбившихся авторов рецептов,
добавление понравившихся рецептов в избранное. Есть возможность фильтрации и поиска рецептов.
Есть возможность добавить понравившееся рецепты в список покупок,
скачать список необходимых продуктов и ингредиентов в удобном формате.


### Как запустить проект при помощи Docker ###:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Alexandrsgit/foodgram-project-react.git
```

в папке infra выполнить команду:
```
docker compose up
```


### Как запустить проект без помощи Docker ###:
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


### Доступ в админ-панель: ###
```
localhost:8000/admin/
```
