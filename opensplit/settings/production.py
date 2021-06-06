from .common import *


SECRET_KEY = "mei0Auzeuy9eiTh3iebu^ophu7baht3!Jei4ahth0vai$Z(uishohhohh?angi/j"
DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.mysql", "NAME": "", "USER": "", "PASSWORD": "", "HOST": "", "PORT": 3306}
}

BASE_URL = "https://opensplit.de"
