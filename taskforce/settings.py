"""
Django settings for your_project_name project.

Generated by 'django-admin startproject' using Django x.x.x.
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@t3fm0tc3=4hwlzs%tyv+y0#w5y2_%(29-x$grlhb4h_++w7ow'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




MOLLIE_API_KEY = 'test_9cpV9y2UtfS2KR4SDeUVp4Vkp2tBWg'


# Application definition

INSTALLED_APPS = [
    'auth_app',
    'wdmmorpg',
    'task_manager',
    'music',
    'plan_selection',
    'HomeApp',
    'project_manager',
    'health_tracker',
        'corsheaders',
    'mind_wellness',
    'time_tracker',
    'seo_tools',
    'communication',
    'myblog',
    'data_analysis',
    'shop_manager',
    'payment_processor',
    'custom_software_dev',
    'lifestyle_consultancy',
    'user_groups_management',
    'project_export_import',
    'project_title_level_system',
    'priority_table_management',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',
]


# ALLOWED_HOSTS = ['','ff59-144-178-82-114.ngrok-free.app']

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# CSRF_TRUSTED_ORIGINS = ['https://*.ngrok.io','https://ff59-144-178-82-114.ngrok-free.app']

# CORS_ALLOWED_ORIGINS = [
#     "https://*.ngrok.io",  # Add your ngrok domain
# ]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ROOT_URLCONF = 'taskforce.urls'

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

WSGI_APPLICATION = 'taskforce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

AUTH_USER_MODEL = 'auth_apdebigp.CustomUser'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wdmdatabase',
        'USER': 'atlas',
        'PASSWORD': 'Lightvessel100!',  # Updated password
        'HOST': 'wdm-db.cihp8rwuaz6j.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/x.x/howto/static-files/
AWS_ACCESS_KEY_ID = 'AKIAZPFM3ISB4EG5U5JY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mediawdm'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_CUSTOM_DOMAIN = 'mediawdm.s3.amazonaws.com'
AWS_LOCATION = 'static'
STATIC_URL = 'https://mediawdm.s3.amazonaws.com//static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'https://mediawdm.s3.amazonaws.com/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/x.x/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'dashboard'