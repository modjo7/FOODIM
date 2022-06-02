# FOODIM : Food ingredients management for people living alone

Run the following commands to set configuration:

Install django as follow if you don't use the existing virtual environment
```
pip install django-crispy-forms==1.8.1
pip install django-filter==2.4.0
pip install django-login-required-middleware==0.4
pip install django-widget-tweaks==1.4.5
pip install django==3.1.13
```

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


This project is closed after development:
```
Github token : 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
Archieve backup : https://drive.google.com/drive/folders/1oowvZU5oANydums6pr93IULgFFDMUH8f?usp=sharing
```