"""
WSGI config for gfvp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""


import os
import sys

if os.name == 'linux':
    path = '/home/gfvpcom/public_html'
    python_path = '/home/gfvpcom/gfvpenv/lib/python3.9/site-packages'
    sys.path.append(path)
    sys.path.append(python_path)

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gfvp.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gfvp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
setattr(settings, 'CNN', False)