import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import ast
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No DJANGO_SECRET_KEY set for production!")

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = os.getenv(
        "CSRF_TRUSTED_ORIGINS", "https://127.0.0.1, https://127.0.0.1:8000 https://localhost"
    ).split(" ")
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "gf-vp.com www.gf-vp.com").split(" ")
    CSRF_TRUSTED_ORIGINS = os.getenv(
        "CSRF_TRUSTED_ORIGINS", "https://www.gf-vp.com"
    ).split(" ")    
    
SITE_ID=1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'django_summernote',    
    "debug_toolbar",
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'axes',
    'accounts',
    'home',
    'evaluation',    
    'crm',
    'doc',
    'captcha',
    'guide',
    'maintenance_mode',
    'blog',
    "taggit",
    'taggit_autosuggest',
    'import_export',
    "django_cron",
    'django_extensions',
    'django_mkdocs',
    'glossary',  
    'feedback',
    'navigation',    
]

if DEBUG:
    MIDDLEWARE = [
        'django.middleware.gzip.GZipMiddleware',         
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        'evaluation.middleware.EvaMiddleware',
        'django.contrib.sites.middleware.CurrentSiteMiddleware',
        #'django.middleware.cache.UpdateCacheMiddleware',  
        'django.middleware.common.CommonMiddleware',
        #'django.middleware.cache.FetchFromCacheMiddleware', 
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'accounts.middleware.ServiceMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'axes.middleware.AxesMiddleware',
        'maintenance_mode.middleware.MaintenanceModeMiddleware',
    ]

else:
    MIDDLEWARE = [
        'django.middleware.gzip.GZipMiddleware',         
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        'evaluation.middleware.EvaMiddleware',
        'django.contrib.sites.middleware.CurrentSiteMiddleware',
        #'django.middleware.cache.UpdateCacheMiddleware',  
        'django.middleware.common.CommonMiddleware',
        #'django.middleware.cache.FetchFromCacheMiddleware', 
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'accounts.middleware.ServiceMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'axes.middleware.AxesMiddleware',
        'maintenance_mode.middleware.MaintenanceModeMiddleware',
    ]

    
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

CRON_CLASSES = [
    "crm.lead_mail_jobs.SendQueueMail",
    "crm.lead_mail_jobs.DeleteIncompleteReports",
]

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'gfvp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'doc.doc_processor.comon_doc',
            ],
        },
    },
]

WSGI_APPLICATION = 'gfvp.wsgi.application'

from .settings_database import *
from .settings_local import *

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from .settings_debug_toolbar import *

LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'

from .settings_axes import *

YOUTUBE_DATA_API_KEY = str(os.getenv("YOUTUBE_DATA_API_KEY"))
IPINFO_TOKEN = str(os.getenv("IPINFO_TOKEN"))


from .settings_maintanance import *

TAGGIT_CASE_INSENSITIVE = True
TAGGIT_AUTOSUGGEST_CSS_FILENAME = 'autoSuggest-grappelli.css'
IMPORT_EXPORT_USE_TRANSACTIONS = True

from .settings_mkdocs import *

if DEBUG:
    from .dev import *   
else:
    from .pro import *