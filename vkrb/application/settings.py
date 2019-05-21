import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2hyx7-$^8*0b%0i9hnjwsoqk#%8o^umr+!%w#j^(3e466j59$!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_celery_beat',
    'webpack_loader',
    'oauth2_provider',
    'corsheaders',
    'adminsortable2',
    'colorfield',
    'solo',
    'mptt',
    'smart_selects',

]

PROJECT_APPS = [
    'vkrb.core',
    'vkrb.oauth',
    'vkrb.auth',
    'vkrb.user',
    'vkrb.newsitem',
    'vkrb.attachment',
    'vkrb.recourse',
    'vkrb.expert',
    'vkrb.text',
    'vkrb.popular',
    'vkrb.event',
    'vkrb.calc',
    'vkrb.education',
    'vkrb.activity',
    'vkrb.digest',
    'vkrb.settings',
    'vkrb.matrix',
    'vkrb.favorites',
    'vkrb.search',
    'vkrb.feedback',
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'vkrb.application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'vkrb', 'templates')
        ],
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

WSGI_APPLICATION = 'vkrb.application.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

PLATFORM_CONFIG_NAME = 'vkrb.conf'
production_config = os.path.join('/etc', 'vkrb', PLATFORM_CONFIG_NAME)
development_config = os.path.join(BASE_DIR, 'conf', PLATFORM_CONFIG_NAME)
config_path = production_config if os.path.exists(production_config) else development_config
config = ConfigParser()

config.read(config_path)

SECRET_KEY = config.get('common', 'secret_key', fallback='my-secret-key')
DEBUG = config.getboolean('common', 'debug', fallback=True)
DOMAIN = config.get('common', 'domain', fallback='192.168.1.6:8000')#192.168.1.6:8000
SCHEMA = config.get('common', 'schema', fallback='http')

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


WSGI_APPLICATION = 'vkrb.application.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('database', 'name', fallback='vkrb'),
        'USER': config.get('database', 'user', fallback='vkrb_user'),
        'PASSWORD': config.get('database', 'password', fallback='vkrb_pass'),
        'HOST': config.get('database', 'host', fallback='127.0.0.1'),
        'PORT': config.get('database', 'port', fallback='5432'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
AUTHENTICATION_BACKENDS = [
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'core.User'

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': config.getint(
        'common', 'access_token_expire_seconds',
        fallback=60 * 60 * 24 * 365 * 100
    )
}
CORS_ORIGIN_ALLOW_ALL = True

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'

CELERY_TIMEZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

if not DEBUG:
    if config.get('logging', 'path', fallback=False):
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'verbose': {
                    'format': 'LEVEL:%(levelname)s '
                              'TIME:%(asctime)s MESSAGE:%(message)s'
                },
            },
            'handlers': {
                'file': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': config.get('logging', 'path'),
                    'formatter': 'verbose'
                }
            },
            'loggers': {
                'django': {
                    'handlers': ['file'],
                    'level': 'INFO',
                    'propagate': True,
                }
            },
        }

POPULAR_LIST_LIMIT = config.getint('common', 'popular_list_limit', fallback=7)
EVENT_NEAREST_LIMIT = config.getint('common', 'event_nearest_limit', fallback=5)
# CELERY SETTINGS
CELERY_BROKER_URL = config.get('celery', 'BROKER_URL', fallback='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

PROXY_BASE_URL = 'http://127.0.0.1:3000/assets/bundles'

VERIFICATION_CODE_TIMEOUT = config.getint('verification_code', 'timeout',
                                          fallback=60)
DRY_RUN_VERIFICATION = config.getboolean('verification_code', 'dry_run',
                                         fallback=False)
DEFAULT_VERIFICATION_CODE = 5555

SENDER_EMAIL = config.get('mailgun', 'sender_email', fallback='vkrb@mail.ru')
EMAIL_BACKEND = config.get('mailgun', 'email_backend', fallback='django_mailgun.MailgunBackend')
MAILGUN_ACCESS_KEY = config.get('mailgun', 'email_key', fallback='227817f576e184cc1b2ef6c20f226cdb-b3780ee5-171c064c')
MAILGUN_SERVER_NAME = config.get('mailgun', 'email_server_name', fallback='sandboxe477bb8577014827aa15169a5742e7fe.mailgun.org')
# MEDIA SETTINGS
MEDIA_URL = '/media/'
DEFAULT_MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = config.get('common', 'media', fallback=DEFAULT_MEDIA_ROOT)
CONTENT_TYPE_FILES = (
    'image/gif', 'image/jpeg', 'image/pjpeg', 'image/png', 'image/tiff',
    'image/bmp', 'image/x-icon', 'image/vnd.microsoft.icon', 'image/svg+xml',
    'application/pdf'
)
IMAGE_CONTENT_TYPES = {
    'image/jpeg',
    'image/png',
    'image/*'
}
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240000
# fcm
CLOUDMESSAGING_KEY = config.get('fcm', 'cloudmessaging_key', fallback='')

WKHTMLTOPDF_PATH = config.get('common', 'wkhtmltopdf_path', fallback='/usr/local/bin/wkhtmltopdf')
# chaining
USE_DJANGO_JQUERY = True

# JET CONFIG
JET_SIDE_MENU_COMPACT = True
JET_DEFAULT_THEME = 'green'
JET_CHANGE_FORM_SIBLING_LINKS = False
