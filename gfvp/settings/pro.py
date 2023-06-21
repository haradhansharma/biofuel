
import os
from dotenv import load_dotenv
from . import BASE_DIR
load_dotenv(os.path.join(BASE_DIR, '.env'))
CNN = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
from .settings_email import *
from .settings_logs import *
from .settings_security import *
from .settings_summernote import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.getenv('CACHE_LOCATION'),
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
USER_AGENTS_CACHE = 'default'
CACHE_MIDDLEWARE_SECONDS = 3600


RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHA_PUBLIC_KEY"))
RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHA_PRIVATE_KEY"))
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']