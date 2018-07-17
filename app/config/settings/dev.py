from .base import *

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

DEBUG = True

# django storages settings
INSTALLED_APPS += [
    'storages',
    'django_extensions'
]

# Media
DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'

# AWS Settings
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']

# WSGI
WSGI_APPLICATION = 'config.wsgi.dev.application'

# DB
DATABASES = secrets['DATABASES']

