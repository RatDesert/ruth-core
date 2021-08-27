import os
from datetime import datetime, timedelta
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(env_variable)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_value('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = [
    'user',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'corsheaders',
    'jwt_auth',
    'celery_worker',
    'hub',
    'sensor',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_env_value('POSTGRES_HOST'),
        'NAME': get_env_value('POSTGRES_DATABASE'),
        'PORT': get_env_value('POSTGRES_PORT'),
        'USER': get_env_value('POSTGRES_USER'),
        'PASSWORD': get_env_value('POSTGRES_USER_PASSWORD')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning'
}

AUTH_USER_MODEL = 'user.User'

FRONTEND_DOMAIN_NAME = 'http://localhost:3000'

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_WHITELIST = [
#     FRONTEND_DOMAIN_NAME,
# ]

# Email conformation service settings
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_value('EMAIL_HOST')
EMAIL_HOST_USER = get_env_value('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_value('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_env_value('EMAIL_PORT')


CELERY_BROKER_URL = get_env_value('CELERY_BROKER')
CELERY_RESULT_BACKEND = get_env_value('CELERY_BROKER')

# Authorization
REFRESH_MAX_AGE = timezone.timedelta(
    seconds=int(get_env_value('REFRESH_MAX_AGE')))
ACCESS_MAX_AGE = timezone.timedelta(
    seconds=int(get_env_value('ACCESS_MAX_AGE')))

REFRESH_COOKIE_SALT = get_env_value('REFRESH_COOKIE_SALT')
REFRESH_COOKIE_SCOPE = get_env_value('REFRESH_COOKIE_SCOPE')
REFRESH_COOKIE_NAME = get_env_value('REFRESH_COOKIE_NAME')

ACCESS_JWT_SIGNING_KEY = get_env_value('ACCESS_JWT_SIGNING_KEY')
ACCESS_COOKIE_SCOPE = get_env_value('ACCESS_COOKIE_SCOPE')
ACCESS_COOKIE_NAME = get_env_value('ACCESS_COOKIE_NAME')

NOTIFICATIONS_SERVICE_URL = get_env_value('NOTIFICATIONS_SERVICE_URL')
NOTIFICATIONS_SERVICE_API_KEY = get_env_value('NOTIFICATIONS_SERVICE_API_KEY')
NOTIFICATIONS_SERVICE_API_KEY_HEADER = get_env_value(
    'NOTIFICATIONS_SERVICE_API_KEY_HEADER')
