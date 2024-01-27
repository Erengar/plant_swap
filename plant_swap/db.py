# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.
import os

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'plant_swap',
    'USER': os.environ.get('NEON_USER'),
    'PASSWORD': os.environ.get('NEON_PASS'),
    'HOST': 'ep-cold-glade-a27o191k.eu-central-1.aws.neon.tech',
    'PORT': '5432',
    'OPTIONS': {'sslmode': 'require'},
  }
}