# e-shop
---
## __Swagger Doc__

[Collection](https://neo15shop.herokuapp.com/swagger/)
### __Deployed to Heroku__

[E-Shop REST API](https://neo15shop.herokuapp.com/api/)

### __Getting started__

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. 

---

#### __Prerequisites__

 This is a project written using Python, Django, and Django Rest Framework

#### __1. Clone the repository__
```
$ git clone https://github.com/Fattijenishbek/e-shop
```
#### __2. Generate a new secret key__
You can use [ Djecrety](https://djecrety.ir/) to quickly generate
 secure secret keys.   
#### __3. Create a new PostgreSQL database__

Assuming you already have pgAdmin and postgres installed.

In your terminal:
```
$ psql postgres
$ CREATE DATABASE databasename
$ \connect databasename
```
Go into pgAdmin, login, and check that the new database exists on the dbserver.
The database credentials to go in your project’s settings.py are the same credentials for pgAdmin.
##### *setting.py*
```
DATABASES = {
             ‘default’: {
                 ‘ENGINE’: ‘django.db.backends.postgresql_psycopg2’,
                 ‘NAME’: env(‘DATABASE_NAME’),
                 ‘USER’: env(‘DATABASE_USER’),
                 'HOST': env('DATABASE_HOST),
                 ‘PASSWORD’: env(‘DATABASE_PASS’),
                 'PORT': env('DATABASE_PORT')
       }
 }

```                                                                                       
                                                               
#### __4. Build the Docker Image__
In your terminal:

```
$ docker-compose build 
```
#### __5. Create a new superuser__
```
$ docker-compose run --rm app_name python manage.py createsuperuser
```
#### __6.Run the project__
Start the development server and ensure everything is running without errors.
```
$ docker-compose up
```



