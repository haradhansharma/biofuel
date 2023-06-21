EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
from .settings_email import *
from .settings_logs import *
# from .settings_security import *
from .settings_summernote import *
X_FRAME_OPTIONS = 'SAMEORIGIN'
# SESSION_COOKIE_SAMESITE = 'Secure'
SESSION_COOKIE_SECURE = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'F:/django/gfvp/cache/',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
USER_AGENTS_CACHE = 'default'
CACHE_MIDDLEWARE_SECONDS = 3600

RECAPTCHA_PUBLIC_KEY = str('6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_PRIVATE_KEY = str('6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']







