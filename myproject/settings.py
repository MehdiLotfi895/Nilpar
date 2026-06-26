
from dotenv import load_dotenv
from pathlib import Path
import os

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# BASE DIR
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY
# =========================

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".ngrok-free.dev",
    "rumor-roving-goldfish.ngrok-free.dev",
    "*"
]

# =========================
# INSTALLED APPS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    # MY APPS
    'main',

    'cart',

    # THIRD PARTY
    'django.contrib.humanize',

    'django_jalali',

    'iranian_cities',
]

# فقط در debug
if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# فقط در debug
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

# =========================
# DEBUG TOOLBAR
# =========================

INTERNAL_IPS = [
    '127.0.0.1',
]

# =========================
# URLS
# =========================

ROOT_URLCONF = 'myproject.urls'

# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR.joinpath('templates')
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'cart.context_processors.cart',

                'main.context_processors.global_data',
            ],
        },
    },
]

# =========================
# WSGI
# =========================

WSGI_APPLICATION = 'myproject.wsgi.application'

# =========================
# DATABASE
# =========================

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': os.getenv('DB_NAME'),

        'USER': os.getenv('DB_USER'),

        'PASSWORD': os.getenv('DB_PASSWORD'),

        'HOST': os.getenv('DB_HOST'),

        'PORT': os.getenv('DB_PORT'),

        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# =========================
# PASSWORD VALIDATORS
# =========================

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

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

USE_L10N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('fa', 'فارسی'),

    ('en', 'English'),
]

# =========================
# STATIC FILES
# =========================

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# =========================
# MEDIA FILES
# =========================

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =========================
# AUTH
# =========================

AUTH_USER_MODEL = 'main.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = 'send_otp'

# =========================
# SESSION
# =========================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# =========================
# CSRF
# =========================

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = 'Lax'

# =========================
# SECURITY HEADERS
# =========================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SECURE_REFERRER_POLICY = 'same-origin'

# =========================
# CACHE
# =========================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# =========================
# CART
# =========================

CART_SESSION_ID = 'cart'

# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



ADMIN_PHONE = os.getenv('ADMIN_PHONE')

# زرین پال تست
ZARINPAL_MERCHANT_ID = os.getenv('ZARINPAL_MERCHANT_ID')

ZARINPAL_CALLBACK_URL = os.getenv('ZARINPAL_CALLBACK_URL')

ZARINPAL_REQUEST_URL = os.getenv('ZARINPAL_REQUEST_URL')

ZARINPAL_VERIFY_URL = os.getenv('ZARINPAL_VERIFY_URL')

ZARINPAL_STARTPAY_URL = os.getenv('ZARINPAL_STARTPAY_URL')




KAVENEGAR_API_KEY = os.getenv("KAVENEGAR_API_KEY")

KAVENEGAR_SENDER = os.getenv("KAVENEGAR_SENDER")



CSRF_TRUSTED_ORIGINS = [
    "https://rumor-roving-goldfish.ngrok-free.dev",
]

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'