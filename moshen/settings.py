"""
Django settings for moshen project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import sys
from re import split
from subprocess import check_output
import django_heroku
from pathlib import Path
from dotenv import load_dotenv


def configure():
    load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


IS_HEROKU = "DYNO" in os.environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
configure()
SECRET_KEY = os.getenv('SECRET_KEY')


# Generally avoid wildcards(*). However since Heroku router provides hostname validation it is ok
# if IS_HEROKU:
#     ALLOWED_HOSTS = ["*"]
# else:
#     ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['moshen.herokuapp.com']

# SECURITY WARNING: don't run with debug turned on in production!
# if not IS_HEROKU:
#     DEBUG = True

DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moshen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'moshen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


def configure_database():
    if 'DATABASE_URL' not in os.environ:
        database_url = check_output('heroku config:get DATABASE_URL -a moshen', shell=True).decode(sys.stdout.encoding).replace('\n', '')
    else:
        database_url = os.environ.get('DATABASE_URL')

    creds = split(':|//|@|/', database_url)

    databases = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': creds[-1],
            'HOST': creds[4],
            'USER': creds[2],
            'PORT': '5432',
            'PASSWORD': creds[3],
        }
    }

    return databases


DATABASES = configure_database()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "main/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
django_heroku.settings(locals())

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51Ljp7nKR9GOBW9TeMlxJlYhmXsm9Ooa1vt5y8QvhZNwTi5CA7kBmiUvbtvCJwEvmiSRCiRCBWyl3bIfoznC1UV5y00QapOQY6d'
if 'STRIPE_SECRET_KEY' in os.environ:
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
