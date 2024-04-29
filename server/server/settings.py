from pathlib import Path
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_KEY') or 'django-insecure-$2itfu&rqrovvldye3m8uwh9!$ju+^_lle=-dsi_$3bc=+=tn#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') or True
ON_RENDER = os.environ.get('ON_RENDER') or False

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['*']

# CORS
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost',
        'http://127.0.0.1',
        'http://0.0.0.0'
    ]
else:
    CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # For allauth

    # Rest Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Social Auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # CORS
    'corsheaders',

    # Local
    'Users',
    'Docs',
    'Notis',
    'Bot',
    'Problems',
    'Tesis',
]

SITE_ID = 1 # For allauth

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise
    'corsheaders.middleware.CorsMiddleware', # CORS
    'allauth.account.middleware.AccountMiddleware', # ALL AUTH MIDDLEWARE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Auth Middleware
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# For Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if ON_RENDER:

    DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgres://avicyttest_user:jFHpRSKv7d7EwqpjzIrREkMR8ux12Aeq@dpg-conp1s4f7o1s73fopuig-a/avicyttest',
        conn_max_age=600
    )
    }
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.environ.get('AWS_ACCESS_KEY'),
                "secret_key": os.environ.get('AWS_SECRET_ACCESS_KEY'),
                "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": os.environ.get('AWS_ACCESS_KEY'),
                "secret_key": os.environ.get('AWS_SECRET_ACCESS_KEY'),
                "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
                "location": "static",
            },
        }
    }

else:

    DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgres://avicyttest_user:jFHpRSKv7d7EwqpjzIrREkMR8ux12Aeq@dpg-conp1s4f7o1s73fopuig-a.oregon-postgres.render.com/avicyttest',
        conn_max_age=600
    )
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


AUTHENTUCATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest_auth settings
REST_AUTH = {
    'LOGIN_SERIALIZER': 'Users.serializers.CustomLoginSerializer',
    'TOKEN_SERIALIZER': 'Users.serializers.CustomTokenSerializer',  #Esto es por si necesitamos más adelante
    'REGISTER_SERIALIZER': 'Users.serializers.CustomRegisterSerializer',
    'USER_DETAILS_SERIALIZER': 'Users.serializers.UserDetailsSerializer',

}

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Allauth account settings
AUTH_USER_MODEL = 'Users.Usuario'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_ADAPTER = 'Users.adapters.CustomAccountAdapter'

# Email Settings
# https://docs.djangoproject.com/en/5.0/topics/email/
#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # For development, Sends the email to the console
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"                                   # Your email host
EMAIL_USE_TLS = True                                            # True
EMAIL_PORT = 587                                                # 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')             # your email address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')     # your password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                            # email ending with @sendinblue.com

# <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL = \
    "https://banco-de-ideas-latest.onrender.com/verify_email_redirect/?key=" # Send the Key to the frontend to make the request on the backend

# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = \
    "<your frontend link>" # Send the UIDB64 and Token to the frontend to make the request on the backend

# Social Auth