from .common import *


DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': os.environ['SQL_ENGINE'],
        'NAME': os.environ['SQL_DATABASE'],
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASSWORD'],
        'HOST': os.environ['SQL_HOST'],
        'PORT': os.environ['SQL_PORT'],
    }
}

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CELERY_BROKER_URL = 'redis://redis:6379/1'

CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'core.tasks.notify_customers',
        'schedule': crontab(day_of_week=1, hour=7, minute=30),
        'args': ['Hello From CeleryBeat'],
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/2',
        'TIMEOUT': 10 * 60,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
