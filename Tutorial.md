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
   Movie.objects.create(title='Loki', tagline='Glorious Purpose')
   Movie.objects.create(title='Hawkeye', tagline='Holiday season, the best gifts are decorated with a bow')

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













<a href="#top">UP</a>