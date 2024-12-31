"""
Django settings for sis_autochess project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jys=axcb&c_b8n6tb3x9c(ug-q=z7jxmp+e^@i-f@ubb)wki4!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ '192.168.48.173', '192.168.49.68', 'localhost' ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ejudge',
    'users',
    'battles',
    'tournament',
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

ROOT_URLCONF = 'sis_autochess.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
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

WSGI_APPLICATION = 'sis_autochess.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    'ejudge': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ejudge',
        'USER': 'w2021-olymp',
        'PASSWORD': 'w2021-olymp',
        # TODO: change host
        'HOST': '127.0.0.1',
        'PORT': '8001',
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/users/login'
LOGOUT_URL = '/users/logout'

EJUDGE_CONTEST_ID = 47999
EJUDGE_SERVE_CFG = BASE_DIR / '..' / 'serve.cfg'
EJUDGE_SERVE_CFG_ENCODING = 'utf-8'

REGISTRED_TEAMS = [
                    'winter-2024-01',
                    'winter-2024-02',
                    'winter-2024-03',
                    'winter-2024-04',
                    'winter-2024-05',
                    'winter-2024-06',
                    'winter-2024-07',
                    'winter-2024-08',
                    'winter-2024-09',
                    'winter-2024-10',
                    'winter-2024-11',
                    'winter-2024-12',
                    'winter-2024-13',
                    'winter-2024-14',
                    # 'winter-2024-15',
                    'winter-2024-16',
                    # 'winter-2024-17',
                    # 'winter-2024-18',
                    # 'winter-2024-19',
                    # 'winter-2024-20',
                  ]

import datetime

CONTEST_DURATION = datetime.timedelta(hours=4)

CONTEST_START_TIME = datetime.datetime(2024, 12, 31, 16, 45, 0)

ROUND_FREQ = datetime.timedelta(minutes=5)
# ROUND_FREQ = datetime.timedelta(seconds=15)

# Maximum units placed on the board by one player
FIGHTER_LIMIT = 16

TURNS_IN_ROUND_LIMIT = 1000
