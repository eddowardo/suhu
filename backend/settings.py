from pathlib import Path
import os

# === BASE DIRECTORY ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === SECURITY ===
SECRET_KEY = 'django-insecure-ymb_(s0fh-n%f&!i*340w3$c7+**j@x5%c@%qi^opuht3ip4)l'  # Sebaiknya nanti pakai ENV variable
DEBUG = False  # ⚠️ Set ke False saat deploy
ALLOWED_HOSTS = ['103.151.63.83', 'localhost', '127.0.0.1']

# === APPLICATIONS ===
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',  # Untuk CORS

    # Aplikasi kamu
    'monitor_suhu',
    'users',
    'sensor',
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === ROOT CONFIGURATION ===
ROOT_URLCONF = 'backend.urls'

# === TEMPLATES ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'users' / 'templates',
        ],
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

# === WSGI CONFIGURATION ===
WSGI_APPLICATION = 'backend.wsgi.application'

# === DATABASE (PostgreSQL) ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'suhu_db',
        'USER': 'postgres',
        'PASSWORD': '12',        # Ganti jika password DB di server berbeda
        'HOST': 'localhost',     # Jika PostgreSQL di server yang sama
        'PORT': '5432',
    }
}

# === PASSWORD VALIDATION ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === INTERNATIONALIZATION ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# === STATIC & MEDIA FILES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Folder hasil collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# === LOGIN / LOGOUT Redirect ===
LOGIN_REDIRECT_URL = '/dashboard/'      # Setelah login
LOGOUT_REDIRECT_URL = '/users/login/'   # Setelah logout
LOGIN_URL = '/users/login/'             # Jika halaman butuh login

# === SESSION AND COOKIE SETTINGS ===
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True            # Aktifkan agar cookie aman (HTTPS)
CSRF_COOKIE_SECURE = True               # Aktifkan agar CSRF cookie aman

# === CORS SETTINGS ===
CORS_ALLOWED_ORIGINS = [
    "http://103.151.63.83",             # IP server kamu
    "http://localhost:8000",            # Untuk local testing
    "http://127.0.0.1:8000",
]

# Jika kamu ingin izinkan semua asal (tidak disarankan di production):
# CORS_ALLOW_ALL_ORIGINS = True

# === DEFAULT PRIMARY KEY ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
