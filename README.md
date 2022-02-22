# CMCPER - Backend

## Installation 

The first thing to do is clone the repository:
```
$ git clone https://github.com/dsuarez2/cmcper_back.git

$ cd cmcper
```
You need to install python3 and pip.

Create a virtual environment to install dependencies and activate it:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Note that the `(venv)` indicates that the terminal session operates in a virtual environment created by `virtualenv`.

Installing the dependencies:
```
(env)$ pip install -r requirements.txt
```




## Configurations
Once `pip` has finished downloading the dependencies:
```
(env)$ cd cmcper
```

Now, we need to edit the `.env` file.
```
# True-> DB filesystem/Email de prueba  
# False-> DB cliente/Email envio  
DEBUG=True

DATABASE_ENGINE=django.db.backends.mysql
DATABASE_NAME=cmcper_local
DATABASE_USER=root
DATABASE_PASSWORD=Mindset2020
DATABASE_HOST=127.0.0.1
PORT=3306

STRIPE_API_KEY_TEST=sk_test_rr9VKE4Po9YQip41vMw9x18y000h9ssG70
STRIPE_API_KEY_PROD=sk_test_rr9VKE4Po9YQip41vMw9x18y000h9ssG70

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=sistema@cmcper.org.mx
EMAIL_HOST_PASSWORD=Consejo3654#
EMAIL_PORT=465

STATIC_ROOT=../static/
MEDIA_ROOT=./uploads/

```
Migration of models:
```
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
## Starting 

````
(env)$ python3 manage.py runserver
````

Navigate to `http://127.0.0.1:8000`.


## CMCPER API documentation

`http://127.0.0.1:8000/api/swagger/`