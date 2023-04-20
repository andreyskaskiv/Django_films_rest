~~~shell
$ pip install -r requirements.txt
~~~
~~~shell
$ pip freeze > requirements.txt
~~~


<a name="top"></a>
### Tutorial

Create requirements.txt, .gitignore, Tutorial.md, .env

1. Create <a href="#project">project</a>
2. Create <a href="#databases">Databases</a>
3. Create <a href="#movie">movie</a>
4. <a href="#crud">CRUD</a>


### 1. Create project: <a name="project"></a>
   ```
   python manage.py startapp .....
   ```
---

### 2. Databases: <a name="databases"></a>

1.

* https://docs.djangoproject.com/en/4.1/ref/databases/
* https://docs.djangoproject.com/en/4.1/ref/databases/#postgresql-notes
* https://www.postgresql.org/download/
* https://postgresapp.com/

- CREATE DATABASE cinema_db;
- CREATE ROLE cinema_username with password 'cinema_password';
- ALTER ROLE "cinema_username" WITH LOGIN;
- GRANT ALL PRIVILEGES ON DATABASE "cinema_db" to cinema_username;
- ALTER USER cinema_username CREATEDB;

psycopg2.errors.InsufficientPrivilege:
- GRANT postgres TO cinema_username;

```shell
sudo su - postgres
psql

\list

\c book_store_db

\dt

```

2. settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}
```

3. migrate
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
   
4. Create createsuperuser
   ```
   python manage.py createsuperuser
   ```

---


### 3. app movie: <a name="movie"></a>

1. Create app movie
   ```
   python manage.py startapp movie
   ```

2. Registration app movie:
   ```
   films -> settings.py
   
   INSTALLED_APPS = [
      ....
    'movie',
      ....
   ]
   ```

3. Create models:
   ```
   movie -> models.py
   
   Movie
   ```
   ```
   python manage.py makemigrations
   python manage.py migrate
   ``` 

4. Registration in admin panel:
   ```
   movie -> admin.py
   
   MovieAdmin
   ```

5. Create serializers:
   ```
   movie -> serializers.py
   
   MoviesSerializer
   ```

6. Create Views:
   ```
   movie -> views.py 
   
   class MovieViewSet(ModelViewSet)
   ```

7. Add the URLs:
   ```
   films -> urls.py added urlpatterns
   

    from rest_framework.routers import SimpleRouter

    from movie.views import MovieViewSet
    
    router = SimpleRouter()
    
    router.register(r'movie', MovieViewSet)

    urlpatterns += router.urls
   ```

8. Test serializers

    * pip install django-extensions
       ```
          INSTALLED_APPS = (
              ...
              'django_extensions',
          )
        ```
       ```
       python manage.py shell_plus
       ```

   
   ```
   Movie.objects.create(title='Loki', tagline='Glorious Purpose, King', year=2021)
   Movie.objects.create(title='Hawkeye', tagline='Holiday season, the best gifts are decorated with a bow', year=2021)
   Movie.objects.create(title='Moon Knight', tagline='The Goldfish Problem', year=2022)
   Movie.objects.create(title='Marvel One-Shot: All Hail the King', tagline='All Hail the King', year=2014)

   ```
   [&#8658; test serializers ](http://127.0.0.1:8000/movie/?format=json)

9. Create TestCase

   ```
   movie/tests -> test_api.py
   
   MovieApiTestCase
   ```
   ```
   url = reverse('movie-list') - all
   
   url = reverse('movie-detail') + pk - single
   ```
   
   ```
   movie/tests -> test_serializers.py
   
   MovieSerializerTestCase
   ```

10. [Filtering in django-rest-framework](https://www.django-rest-framework.org/api-guide/filtering/)

* addition settings.py

    ```
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        ),
    }
    ```

* addition views.py 
    ```text
    If all you need is simple equality-based filtering, 
    you can set a filterset_fields attribute on the view, or viewset,
    listing the set of fields you wish to filter against.
    ```
    ```text
    The SearchFilter class will only be applied if the view has a search_fields 
    attribute set. The search_fields attribute should be a list of names of text type
    fields on the model, such as CharField or TextField.
    ```
    ```text
    The OrderingFilter class supports simple query parameter controlled ordering of results.
    ```

    ```
    movie -> views.py
    
    class MovieViewSet(ModelViewSet):
       ...
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_fields = ['title', ]
        search_fields = ['title', 'tagline', 'year']
        ordering_fields = ['year', ]
    ```

    
   #### test:

- [all](http://127.0.0.1:8000/movie/) :
    ```json
    [
    {
    "id": 4,
    "title": "Hawkeye",
    "tagline": "Holiday season, the best gifts are decorated with a bow",
    "description": null,
    "year": 2021
    },
    {
    "id": 5,
    "title": "Moon Knight",
    "tagline": "The Goldfish Problem",
    "description": null,
    "year": 2022
    },
    {
    "id": 6,
    "title": "Marvel One-Shot: All Hail the King",
    "tagline": "All Hail the King",
    "description": null,
    "year": 2014
    },
    {
    "id": 7,
    "title": "Loki",
    "tagline": "Glorious Purpose, King",
    "description": null,
    "year": 2021
    }
    ]
    ```
  
- [filterset_fields = ['year=2021']](http://127.0.0.1:8000/movie/?year=2021)
    ```json
    [
    {
    "id": 4,
    "title": "Hawkeye",
    "tagline": "Holiday season, the best gifts are decorated with a bow",
    "description": null,
    "year": 2021
    },
    {
    "id": 7,
    "title": "Loki",
    "tagline": "Glorious Purpose, King",
    "description": null,
    "year": 2021
    }
    ]
    ```

- [search_fields = ['search=King']](http://127.0.0.1:8000/movie/?search=King)
    ```json
    [
    {
    "id": 6,
    "title": "Marvel One-Shot: All Hail the King",
    "tagline": "All Hail the King",
    "description": null,
    "year": 2014
    },
    {
    "id": 7,
    "title": "Loki",
    "tagline": "Glorious Purpose, King",
    "description": null,
    "year": 2021
    }
    ]
    ```

- [ordering_fields = ['-ordering=-year']](http://127.0.0.1:8000/movie/?ordering=-year)
    ```json
    [
    {
    "id": 5,
    "title": "Moon Knight",
    "tagline": "The Goldfish Problem",
    "description": null,
    "year": 2022
    },
    {
    "id": 4,
    "title": "Hawkeye",
    "tagline": "Holiday season, the best gifts are decorated with a bow",
    "description": null,
    "year": 2021
    },
    {
    "id": 7,
    "title": "Loki",
    "tagline": "Glorious Purpose, King",
    "description": null,
    "year": 2021
    },
    {
    "id": 6,
    "title": "Marvel One-Shot: All Hail the King",
    "tagline": "All Hail the King",
    "description": null,
    "year": 2014
    }
    ]
    ```
  
11. Continued TestCase
    ```
    movie/tests -> test_api.py
    
    MovieApiTestCase
    ```
    ```
    movie/tests -> test_serializers.py
    
    MovieSerializerTestCase
    ```


```
python manage.py test
```

### 5. CRUD <a name="crud"></a>

1. Refactor Views:

    ```
   movie -> views.py
   
   class MovieViewSet(ModelViewSet):
      ...
      permission_classes = [IsAuthenticatedOrReadOnly]
      ...
   ```

2. Continued TestCase

* Checking Previous Tests
   ```pycon
    python manage.py test
   ```

  
* New test:

   ```
   movie/tests -> test_api.py
   
   def setUp(self):
       self.user = User.objects.create(username='test_username')
       ... 
   ```
   ```
   movie/tests-> test_api.py
   
   def test_05_POST_create(self):
       ...      

   def test_06_PUT_update(self):
       ... 
       
   def test_07_DELETE(self):
       ...          
          
   def test_08_get_id(self):
       ...    
   ```
  
'book-list' - no id  
'book-detail' - have id













<a href="#top">UP</a>