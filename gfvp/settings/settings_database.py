import os
import ast
from dotenv import load_dotenv
from . import BASE_DIR
load_dotenv(os.path.join(BASE_DIR, '.env'))
DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gfvp' if DEBUG else os.getenv('DB_NAME'),
        'USER': 'root' if DEBUG else os.getenv('DB_USER'),
        'PASSWORD': '' if DEBUG else os.getenv('DB_PASS'),
        'HOST':'localhost',
        'PORT': '3306',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
