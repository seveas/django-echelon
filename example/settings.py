import os


_PATH = os.path.abspath(os.path.dirname(__file__))
_MODULE = os.path.basename(_PATH)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

DEBUG = True

SECRET_KEY = '$yir+-pws5+1qd5#ny9e$a=^tr$@z(7Tr!tY4j-ytj1**^e+##'

ROOT_URLCONF = '%s.urls' % _MODULE

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'echelon.middleware.EchelonMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'echelon',
)
