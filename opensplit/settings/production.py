# flake8: F403
from .common import *
import os


SECRET_KEY = "mei0Auzeuy9eiTh3iebu^ophu7baht3!Jei4ahth0vai$Z(uishohhohh?angi/j"
DEBUG = False
ALLOWED_HOSTS = ["app"]

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": "django",
        "HOST": "db",
        "PORT": 3306,
    }
}

BASE_URL = "https://opensplit.de"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USER = "app@opensplit.de"
EMAIL_USER_PASSWORD = os.environ["EMAIL_PASS"]
EMAIL_HOST = "mail.felixbreidenstein.de"
EMAIL_USE_TLS = True
EMAIL_POST = 465
