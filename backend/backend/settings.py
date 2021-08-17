from pathlib import Path
import os
import datetime
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')
ALLOWED_HOSTS = [] if not any(ALLOWED_HOSTS) else ALLOWED_HOSTS

AUTH_USER_MODEL = 'users.User'


# Application definition

INSTALLED_APPS = [
    # CAVEAT: we need to overwrite createsuperuser command.
    # That's the reason behind this module being the first one.
    # In fact, it need only to come before django.contrib.auth module
    'users',
    'posts',
    'config_ui',
    'events',
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'PORT': os.getenv('DB_PORT')
    }
}


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

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
THUMBNAIL_SIZE=(300,300)
PHOTO_SIZE=(1000,1000)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser'
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False
}

CORS_ORIGIN_ALLOW_ALL = True

# TEXT LOCAL
TEXTLOCAL_API_KEY = os.getenv('TEXTLOCAL_API_KEY')
TEXTLOCAL_USERNAME = os.getenv('TEXTLOCAL_USERNAME')
TEXTLOCAL_PASSWORD_HASH = os.getenv('TEXTLOCAL_PASSWORD_HASH')
SMS_SENDER = os.getenv('SMS_SENDER')
PASSWORD_TEMPLATE = os.getenv('PASSWORD_TEMPLATE')
SIGNUP_TEMPLATE = os.getenv('SIGNUP_TEMPLATE')
NUMBER_CHANGE_TEMPLATE = os.getenv('NUMBER_CHANGE_TEMPLATE')
TEXTLOCAL_SEND_URL = os.getenv('TEXTLOCAL_SEND_URL')
SOCIETY_NAME = os.getenv('SOCIETY_NAME')
OTP_VALIDATION_TIME = os.getenv('OTP_VALIDATION_TIME')
ACCOUNT_APPROVAL_TEMPLATE = os.getenv('ACCOUNT_APPROVAL_TEMPLATE')
