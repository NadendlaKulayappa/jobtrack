
"""
Django settings for config project.
"""

import os
from pathlib import Path
import dj_database_url

# Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Security settings
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "local-development-only-insecure-key"
    else:
        raise ValueError("DJANGO_SECRET_KEY must be set in production")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

# Installed applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "jobs",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# Database
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = "static/"


# Email configuration
# Use Django's MAILERS setting (Django 6.1)

# Email configuration for Django 6.1
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": "smtp.gmail.com",
            "port": 587,
            "use_tls": True,
            "username": os.environ.get("EMAIL_HOST_USER", ""),
            "password": os.environ.get("EMAIL_HOST_PASSWORD", ""),
        },
    },
}

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CSRF_TRUSTED_ORIGINS = [
    f"https://{render_host}"
    for render_host in [os.environ.get("RENDER_EXTERNAL_HOSTNAME")]
    if render_host
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")