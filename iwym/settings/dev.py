from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database dev
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iwym',
        'USER': 'iwym',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 'CHARSET': 'utf8',
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
