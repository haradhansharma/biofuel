
import os
import sys

if os.name != 'nt':
    path = '/home/gfvpcom/public_html'
    python_path = '/home/gfvpcom/gfvpenv/lib/python3.9/site-packages'
    sys.path.append(path)
    sys.path.append(python_path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'gfvp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from gfvp.addset import add_set
add_set()