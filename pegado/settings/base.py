"""
Django settings for pegado project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.normpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=0c#ev2tyjd67z7d-2doun7&nei^m8b8=o%cvz1)sozao8syav'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


SHARED_APPS  = [
    'django_tenants',  # mandatory
    'core',
    'util',
    'base_util',
    'river',
    'rest_framework.authtoken',
    'river_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
TENANT_APPS = (
    'django_tenants',  # mandatory
    'core',
    'util',
    'base_util',
    'river',
    'rest_framework.authtoken',
    'river_admin',
    
    'codemirror2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
)



INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
PUBLIC_SCHEMA_URLCONF = 'pegado.urls_public'
ROOT_URLCONF = 'pegado.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR, "../templates" ),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "loaders": [
                "django_tenants.template.loaders.filesystem.Loader",  # Must be first
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]

STATICFILES_FINDERS = [
    "django_tenants.staticfiles.finders.TenantFileSystemFinder",  # Must be first
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
   
]
STATICFILES_STORAGE = "django_tenants.staticfiles.storage.TenantStaticFilesStorage"

MULTITENANT_RELATIVE_STATIC_ROOT = "" 

DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"

MULTITENANT_RELATIVE_MEDIA_ROOT = "" 

TENANT_MODEL = "core.Client" 

TENANT_DOMAIN_MODEL = "core.Domain" 

WSGI_APPLICATION = 'pegado.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         'ENGINE': 'django_tenants.postgresql_backend', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         "NAME": 'kerala',  # Or path to database file if using sqlite3.
#         "USER":'admin',
#         "PASSWORD": 'admin',
#         "HOST": 'localhost' , # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         "PORT":  '5432',# Set to empty string for default.
#     }
# }
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


MULTITENANT_TEMPLATE_DIRS = [
     os.path.join( BASE_DIR, "../tenants/%s/templates" )
]
MULTITENANT_STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "../tenants/%s/static" ),
]


# STATIC_URL = '/static/'




#### river admin #####
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'EXCEPTION_HANDLER': 'river_admin.views.exception_handler'
}

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, './static'),
# )
STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')


#  logging section

    
LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/info.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            # 'propagate': True,
        },
    },
}