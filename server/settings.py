"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_o246i)o*hmu($4y-eh(l!3p4b5bfm3$_z4!z5^n7_yzdb^62e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ['http://localhost:8000', 'http://345a5193bbe1.ngrok.io:80']
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://887721c653d1.ngrok.io',  # back
    'http://localhost:4200',
    # 'http://54625c39d9d4.ngrok.io',  # front
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters', # hay que instalarlo antes -> pip install django-filter
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    'api',
    'preregistro',
    'chat',
    'notificaciones',
    'convocatoria',
    'catalogos',
    'front',
    'recertificacion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    # --------- Por si se necesita autenticar
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'COERCE_DECIMAL_TO_STRING': False,  # quita que se los campos de tipo Decimal se regresen como string
}

# SWAGGER_SETTINGS = {
#     # 'SECURITY_DEFINITIONS': {
#     #     'api_key': {
#     #         'type': 'apiKey',
#     #         'in': 'header',
#     #         'name': 'Authorization'
#     #     }
#     # },
#     "is_authenticated": False,  # Set to True to enforce user authentication,
#     "is_superuser": False,  # Set to True to enforce admin only access
# }

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DATABASE_ENGINE'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST', default='localhost'),
            'PORT': config('PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = config('STATIC_ROOT')
# MEDIA_URL = '/uploads/'
# MEDIA_ROOT = config('MEDIA_ROOT')

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# STATIC_ROOT = config('STATIC_ROOT', default="./static/")
MEDIA_URL=config('MEDIA_URL', default="/uploads/")
MEDIA_ROOT=config('MEDIA_ROOT', default="./uploads/")


# Claves de STRIPE
if DEBUG:
    STRIPE_API_KEY = config('STRIPE_API_KEY_TEST', default='sk_test_rr9VKE4Po9YQip41vMw9x18y000h9ssG70')
else:
    STRIPE_API_KEY = config('STRIPE_API_KEY_PROD', default='sk_test_rr9VKE4Po9YQip41vMw9x18y000h9ssG70')

# Configuraciones de correo

if DEBUG:
    # EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

MAILER_EMAIL_BACKEND = EMAIL_BACKEND

EMAIL_HOST = config('EMAIL_HOST', default='mail.booster.com.mx')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='billy@booster.com.mx')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='billy123!')
EMAIL_PORT = config('EMAIL_PORT', default=465)
