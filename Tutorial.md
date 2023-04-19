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

















<a href="#top">UP</a>