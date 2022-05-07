# FOODIM : Food ingredients management for people living alone

Run the following commands to set database:

Create the database & Migrate model changes
```
python manage.py makemigrations homepage
python manage.py migrate homepage
python manage.py makemigrations inventory
python manage.py migrate inventory
python manage.py makemigrations community
python manage.py migrate community
python manage.py makemigrations
python manage.py migrate

```

Create a admin user

```
python manage.py createsuperuser

```

Run Server

```
python manage.py runserver
```


Run Server (externel)

```
python manage.py runserver 0.0.0.0:8000
```
