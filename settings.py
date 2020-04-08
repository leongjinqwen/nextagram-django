import dj_database_url
import os
from django.core.management.commands.makemigrations import Command
from django.core.management.commands.migrate import Command

DATABASES = { 
    'default': dj_database_url.config(default=os.environ['DATABASE_URL']) 
}

INSTALLED_APPS = ( 'dj', )

SECRET_KEY = 'REPLACE_ME'