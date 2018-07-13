from .base import *
# secrets = json.loads(open(os.path.join(SECRETS_DIR, 'dev.json')).read())
secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
]

# WSGI
WSGI_APPLICATION = 'config.wsgi.production.application'

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static
STATIC_URL = '/static/'
