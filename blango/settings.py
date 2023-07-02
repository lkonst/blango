"""
Django settings for blango project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from configurations import Configuration
from configurations import values
import dj_database_url
from django.contrib.auth.hashers import Argon2PasswordHasher

class Dev(Configuration):

  EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  ACCOUNT_ACTIVATION_DAYS = 7
  # REGISTRATION_OPEN = False

  AUTH_USER_MODEL = 'blango_auth.User'
  #SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

  # Build paths inside the project like this: BASE_DIR / 'subdir'.
  BASE_DIR = Path(__file__).resolve().parent.parent

  #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


  # Quick-start development settings - unsuitable for production
  # See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = 'django-insecure-+sn%dpa!086+g+%44z9*^j^q-u4n!j(#wl)x9a%_1op@zz2+1-'

  # SECURITY WARNING: don't run with debug turned on in production!
  #DEBUG = True
  DEBUG = values.BooleanValue(True)

  #ALLOWED_HOSTS = []
  ALLOWED_HOSTS = ['*']
  X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io'
  CSRF_COOKIE_SAMESITE = None
  CSRF_TRUSTED_ORIGINS = [os.environ.get('CODIO_HOSTNAME') + '-8000.codio.io']
  CSRF_COOKIE_SECURE = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SAMESITE = 'None'
  SESSION_COOKIE_SAMESITE = 'None'

  # Application definition

  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'blango_auth',
      'blog',
      'crispy_forms',
      'crispy_bootstrap5',
      'debug_toolbar',
  ]

  MIDDLEWARE = [
          'debug_toolbar.middleware.DebugToolbarMiddleware',
          'django.middleware.security.SecurityMiddleware',
          'django.contrib.sessions.middleware.SessionMiddleware',
          'django.middleware.common.CommonMiddleware',
      #    'django.middleware.csrf.CsrfViewMiddleware',
          'django.contrib.auth.middleware.AuthenticationMiddleware',
          'django.contrib.messages.middleware.MessageMiddleware',
      #  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  ]

  ROOT_URLCONF = 'blango.urls'

  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [ BASE_DIR/'templates'],
          #'DIRS': [os.path.join(BASE_DIR, 'templates')],
          # 'DIRS': [os.path.join(BASE_DIR, 'templates'),
          #             os.path.join(BASE_DIR, 'blog', 'templates', 'blog')],
          #'DIRS': [ os.path.join(SETTINGS_PATH), 'templates'],
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

  WSGI_APPLICATION = 'blango.wsgi.application'


  # Database
  # https://docs.djangoproject.com/en/3.2/ref/settings/#databases

  #   DATABASES = {
  #       'default': {
  #           'ENGINE': 'django.db.backends.sqlite3',
  #           'NAME': BASE_DIR / 'db.sqlite3',
  #       }
  #   }

  DATABASES = {
      "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
      "alternative": dj_database_url.config(
          "ALTERNATIVE_DATABASE_URL",
          default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
          ),
      }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

  LANGUAGE_CODE = 'en-us'

  #TIME_ZONE = 'UTC'
  TIME_ZONE = values.Value("UTC")
  #TIME_ZONE = values.Value("UTC", environ_prefix="BLANGO")

  USE_I18N = True

  USE_L10N = True

  USE_TZ = True


  # Static files (CSS, JavaScript, Images)
  # https://docs.djangoproject.com/en/3.2/howto/static-files/

  STATIC_URL = '/static/'

  # Default primary key field type
  # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

  DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

  CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

  CRISPY_TEMPLATE_PACK = "bootstrap5"

  LOGGING = {
    "version":1,
    "disable_existing_loggers": False,
    "filters": {
      "require_debug_false": {
        "()": "django.utils.log.RequireDebugFalse",
      },
    },
    "formatters": {
      "verbose": {
        "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
        "style" : "{",
      },
    },

    "handlers": {
      "console": {                          #the handler will log to the console
        "class": "logging.StreamHandler", 
        "stream": "ext://sys.stdout",
        "formatter": "verbose",
      },
      "mail_admins":{
        "level": "ERROR",
        "class": "django.utils.log.AdminEmailHandler",
        "filters": ["require_debug_false"],
      },
    },
    "loggers":{
      "django.request": {
        "handlers": ["mail_admins"],
        "level": "ERROR",
        "propagate": True,
      },
    },
    # handlers": {
    #   "file": {"class": "logging.FileHandler", "filename": "/var/log/blango.log"},
    # }
    "root": {
      "handlers": ["console"],
      "level":"DEBUG",
    },
  }
  ADMINS = [("Ben Shaw", "ben@example.com"), ("Leo Lucio", "leo@example.com")]
  DJANGO_ADMINS="Ben Shaw,ben@example.com;Leo Lucio,leo@example.com"

  PASSWORD_HASHERS = [
  #'django.contrib.auth.hashers.Argon2PasswordHasher'
  'django.contrib.auth.hashers.PBKDF2PasswordHasher',
  'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
  #'django.contrib.auth.hashers.Argon2PasswordHasher',
  'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
  ]

  INTERNAL_IPS = ["192.168.11.179", '192.168.10.93']

class Prod(Dev):
  DEBUG = False
  SECRET_KEY = values.SecretValue()
  #SECRET_KEY = values.SecretValue("any-hard-coded-value")
  ALLOWED_HOSTS = values.ListValue(['localhost','0.0.0.0','.codio.io'])

  #BASE_DIR = Dev.BASE_DIR

  #DATABASES = values.DatabaseURLValue(f"sqlite:///{BASE_DIR}/db.sqlite3")
#   DATABASES = {
#     "default": dj_database_url.config(default=f"sqlite:///{BASE_DIR}/db.sqlite3"),
#     "alternative": dj_database_url.config(
#         "ALTERNATIVE_DATABASE_URL",
#         default=f"sqlite:///{BASE_DIR}/alternative_db.sqlite3",
#     ),
# }


