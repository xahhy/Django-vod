"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime

import os

from django.conf import settings


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from mysite.router import DatabaseAppsRouter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%ur^wgur*+1c$kxk_(bkqonaebu3&f#a7v+g7j)65k=6%z*itz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# import corsheaders.middleware

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False

# my settings
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
# filer cononical url set
# FILER_CANONICAL_URL = 'sharing/'

# Application definition

INSTALLED_APPS = [
    'easy_thumbnails',
    'filer',
    'mptt',
    # 'progressbarupload',
    'admin_resumable',

    "djangocms_admin_style",
    'django.contrib.admin',
    'django.contrib.auth',

    # 'django.contrib.sites',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # user apps
    'corsheaders',
    'vodmanagement.apps.VodConfig',
    'epg.apps.EpgConfig',
    'rest_framework',

    # Scheduler App
    'django_celery_beat',
    # 'rest_framework_docs',
    # 'drf_autodocs'
    # 'rest_framework_swagger',


    # The following apps are required:

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.weixin',

]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'mysite.urls'

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
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}
# AUTHENTICATION_BACKENDS = (
#
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',
#
#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',
#
# )
# SOCIALACCOUNT_PROVIDERS = {
#     'weixin': {
#         'AUTHORIZE_URL': 'https://open.weixin.qq.com/connect/oauth2/authorize',  # for media platform
#     }
# }

# SITE_ID = 1
WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASE_ROUTERS = ['mysite.router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
    'epg': 'tsrtmp'
}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'tsrtmp',
        'USER' : 'root',
        'PASSWORD': '123',
        'HOST': '',
        'PORT': '',#'3306',
    },
    'tsrtmp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'flask',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (200, 300), 'crop': True},
    },
}
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication'

    ),
    "DEFAULT_PERMISSION_CLASSES": (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'zh-Hans'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
RECORD_MEDIA_FOLDER = 'record'
RECORD_MEDIA_ROOT = os.path.join(MEDIA_ROOT, RECORD_MEDIA_FOLDER)
LOCAL_FOLDER_NAME = 'local_file'
LOCAL_MEDIA_URL = LOCAL_FOLDER_NAME + '/'
LOCAL_MEDIA_ROOT = os.path.join(MEDIA_ROOT, LOCAL_FOLDER_NAME)

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'filer.storage.PublicFileSystemStorage',
            'OPTIONS': {
                'location': MEDIA_ROOT,
                'base_url': '/media/filer/',
            },
            'UPLOAD_TO': 'filer.utils.generate_filename.by_date',
            # 'UPLOAD_TO': 'filer.utils.generate_filename.upload_video_location',
            # 'UPLOAD_TO' : 'vodmanagement.models.upload_video_location',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
    },
}
ADMIN_RESUMABLE_CHUNKSIZE = 1024 * 1024 * 10
ADMIN_RESUMABLE_STORAGE = 'vodmanagement.my_storage.VodStorage'

# Memory Cache
CACHES = {
    'default':{
        # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': '127.0.0.1:11211',
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Scheduler App
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# FILE_UPLOAD_HANDLERS = (
#     "progressbarupload.uploadhandler.ProgressBarUploadHandler",
#     "django.core.files.uploadhandler.MemoryFileUploadHandler",
#     "django.core.files.uploadhandler.TemporaryFileUploadHandler",
# )
# PROGRESSBARUPLOAD_INCLUDE_JQUERY = False
