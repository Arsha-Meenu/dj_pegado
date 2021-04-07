from .base import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        'ENGINE': 'django_tenants.postgresql_backend', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": 'uoktest1',  # Or path to database file if using sqlite3.
        "USER": 'admin' ,
        "PASSWORD":'admin',
        "HOST": 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": '5432',  # Set to empty string for default.
    }
}