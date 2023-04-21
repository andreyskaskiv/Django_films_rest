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
5. Create <a href="#permissions">Permissions</a>
6. Create <a href="#like">Like, Bookmarks, Rating </a>
7. Create <a href="#annotation">Annotation and Aggregation </a>


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

\c cinema_db

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

### 4. CRUD <a name="crud"></a>

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
  
'movie-list' - no id  
'movie-detail' - have id


### 5. Create Permissions: <a name="permissions"></a>

Любой может открывать фильм,  
создавать и изменять может только stuff


1. Create permissions:
   ```
   movie -> permissions.py
   
   class IsStaffOrReadOnly(BasePermission):
   ```

2. Views refactoring:
   ```
   movie -> views.py 
   
   class MovieViewSet(ModelViewSet)
        ...
        permission_classes = [IsStaffOrReadOnly]
        ...

   ```

3. Continued TestCase
   ```pycon
    python manage.py test
   ```

* addition test:

    ```
    movie/tests -> test_api.py
    
    def setUp(self):
       ... 
       self.user = User.objects.create(username='test_username', is_staff=True)
       ... 
    
    ```

* New test:

    ```
    movie/tests -> test_api.py
    
    def test_09_PUT_update_not_staff(self):
       ...      
    
    def test_10_PUT_update_not_login(self):
       ...   

    def test_11_DELETE_not_staff(self):
       ...      
    
    def test_12_DELETE_not_login(self):
       ...  
     
    def test_13_POST_create_login_not_stuff(self):
       ...  
   
    ```
  

### 6. Like, Bookmarks, Rating: <a name="like"></a>

1. Create models:
   ```
   movie -> models.py
   
   UserMovieRelation
   ```

2. Models refactoring:
   ```
   movie -> models.py
   
    class Movie(models.Model):
        ...
        readers = models.ManyToManyField(User, through='UserMovieRelation',
                                     related_name='movie')
   ```

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. Registration in admin panel:
   ```
   movie -> admin.py
   
   UserMovieRelationAdmin
   ```
   
4. `python manage.py shell_plus`

    ```
    >>> user = User.objects.last()
   
    >>> user
    <User: Test_users>

    >>> user.movie.all()
    <QuerySet [<Movie: Id 4: Hawkeye>, <Movie: Id 6: Marvel One-Shot: All Hail the King>]>

    
    >>> user = User.objects.get(id=1)
   
    >>> user
    <User: andrey>
   
    >>> user.movie.all()
    <QuerySet [<Movie: Id 5: Moon Knight>]>

    ```
    movie = UserMovieRelation (like/in_bookmarks/rate)

5. Create serializers:  
    id мы берем из self.request.user, поэтому не передаем в сериализоторе
   ```
   movie -> serializers.py
   
   UserMovieRelationSerializer
   ```

6. Create Views:  
    `lookup_field = 'movie'` создаем  для удобства, для фронта подменяя id релейшена на id movie, и реализуем через def get_object
    ```
    movie -> views.py 
    
    class UserMoviesRelationView(UpdateModelMixin, GenericViewSet):
    ```

7. Add the URLs: 
   ```
   films -> urls.py 

   router.register(r'movie_relation', UserMoviesRelationView)

   ```

8. Create TestCase

   ```pycon
    python manage.py test
   ```

* addition test:

    ```
    movie/tests -> test_serializers.py
    
    class MovieSerializerTestCase(TestCase):
        def test_ok(self):
        ...
        'readers': [],
        ...
  
     ```   
  
* New test:

   ```
   movie/tests -> test_api.py
   
   MoviesRelationTestCase
   ```


### 7. Create Annotation and Aggregation: <a name="annotation"></a>

   
1. Annotation, View refactoring:
    Аннотируем каждый фильм, присваиваем вот этому полю annotated_likes количество (Count)
    в случае (Case), когда (When) usermovierelation__like=True. И оно его сериализует через IntegerField

    ```
    movie -> views.py 
    
    class MovieViewSet(ModelViewSet):
        queryset = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
               ...
    ```
2. Serializers refactoring:

    ```
    movie -> serializers.py
       
    class MoviesSerializer(ModelSerializer):
        annotated_likes = serializers.IntegerField(read_only=True)
        rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
        
        class Meta:
            model = Movie
            fields = ('id', 'title', 'tagline', 'description', 'year', 'readers',
                      'annotated_likes', 'rating')
    
    ```

3. addition test_serializers:

    ```
    movie/tests -> test_serializers.py
    
    class MovieSerializerTestCase(TestCase):
        def test_ok(self):
            user1 = User.objects.create(username='user1')
            user2 = User.objects.create(username='user2')
            user3 = User.objects.create(username='user3')
            
            ...
            UserMovieRelation = 
            ...
            
            ...
            queryset = Movie.objects.all().annotate(
                annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
                rating=Avg('usermovierelation__rate')
            ).order_by('id')
            ...
            
            ...
            'readers': [user1.id, user2.id, user3.id],
            'annotated_likes': 3,
            'rating': '4.67',
            ...
     ```  

4. addition test_api:

    ```
    movie/tests -> test_api.py
    
    def setUp(self):
       ... 
       UserMovieRelation.objects.create(user=self.user, movie=self.movie_1, like=True,
                                         rate=5)
       ... 
    
   
    def test_01_get(self):
       ... 
       queryset = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data
       ... 
   
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)
       ... 
   

   
    def test_02_get_filter(self):
       ... 
       queryset = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_2.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data
       ... 

   
   
    def test_03_get_search(self):
       ... 
        queryset = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_3.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data
       ... 

   
    def test_04_get_ordering(self):
       ... 
        queryset = Movie.objects.annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('-year')
        serializer_data = MoviesSerializer(queryset, many=True).data
       ... 
 
   
   
    def test_08_get_id(self):
       ... 
        queryset = Movie.objects.filter(id__in=[self.movie_1.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data
       ...      
   
       self.assertEqual(serializer_data[0], response.data)
   
   
    ```

   ```pycon
    python manage.py test
   ```











<a href="#top">UP</a>