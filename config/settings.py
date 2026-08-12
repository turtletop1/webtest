
from pathlib import Path
from dotenv import load_dotenv # add
import os                       # add
from django.contrib.messages import constants as message  # add
load_dotenv()               # add


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')   # add this to .env

DEBUG = True

ALLOWED_HOSTS = []

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

LOCAL_APPS = [                      #add new page
    "pages.apps.PagesConfig",
    "accounts.apps.AccountsConfig",
    "posts.apps.PostsConfig",
    "stuffs.apps.StuffsConfig",
]

THIRD_PARTY_APPS = ["debug_toolbar", "widget_tweaks","taggit"]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],                  # add
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



DATABASES = {                                                                    # add this for database
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'webstestdb',
        "USER": 'postgres',
        "PASSWORD" : 'hkhkhk',
        "HOST" : 'localhost',
        "PORT" : '5432',
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = 'static/'                      
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'config/static')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')                 # 媒體文件保存在硬盤上的絕對路徑
MEDIA_URL = '/media/'   


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    message.ERROR : 'danger',
    message.SUCCESS : 'success',
}
