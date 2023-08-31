
import os
import sys

os.umask(0o002)
if os.name != 'nt':
    # path = '/home/gfvpcom/public_html'
    # python_path = '/home/gfvpcom/gfvpenv/lib/python3.9/site-packages'
    # sys.path.append(path)
    # sys.path.append(python_path)    
    sys.path.insert(0, '/home/gfvpcom/gfvpenv/lib/python3.9/site-packages')
    from django.core.wsgi import get_wsgi_application
    sys.path.insert(1, '/home/gfvpcom/public_html')
    os.environ["DJANGO_SETTINGS_MODULE"] = "gfvp.settings"
    application = get_wsgi_application()    
    
else:    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'gfvp.settings'
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

from gfvp.addset import add_set
add_set()
