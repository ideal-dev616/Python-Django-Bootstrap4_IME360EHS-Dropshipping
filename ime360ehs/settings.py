"""
Django settings for ime360ehs project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&-zjyiy6lhs85jc5x=vbbxzgffzvqld+78d2!#a305g%+mc@ac'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'ime360ehs',
    'clear_cache',
    'sass_processor'
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

ROOT_URLCONF = 'ime360ehs.urls'

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

WSGI_APPLICATION = 'ime360ehs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '360ehs',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'ime360ehs.User'

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
    }
]


SOUTH_TESTS_MIGRATE = False

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

# DISCOVERY_DOCUMENT = 'https://developer.api.intuit.com/.well-known/openid_sandbox_configuration/'
# CLIENT_ID = 'ABOEhkbAiGKlHZhvJFhff3fSxq8HJxRRMPh3OTgqntSed1YfVc'
# CLIENT_SECRET = 'ctUtmxLwyw9CSZktXJMIa7iEDMFS5OHhAnyIziZQ'
# REDIRECT_URI = 'http://localhost:8000/callback'
# ACCOUNTING_SCOPE = 'com.intuit.quickbooks.accounting'
# OPENID_SCOPES = ['openid', 'profile', 'email', 'phone', 'address']
# GET_APP_SCOPES = ['com.intuit.quickbooks.accounting', 'openid', 'profile', 'email', 'phone', 'address']
# SANDBOX_QBO_BASEURL = 'https://sandbox-quickbooks.api.intuit.com'
# SANDBOX_PROFILE_URL = 'https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo'
# ID_TOKEN_ISSUER = 'https://oauth.platform.intuit.com/op/v1'
# ENVIRONMENT = 'sandbox'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'index'

# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# eMail Server Config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "lixiangde888@gmail.com"
EMAIL_HOST_PASSWORD = "limengxiang0616"