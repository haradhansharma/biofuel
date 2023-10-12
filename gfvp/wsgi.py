# Import necessary modules
import os
import sys

# Set the umask to 0o002, which controls default permissions when creating files and directories
os.umask(0o002)

# Check the operating system name
if os.name != 'nt':
    # On non-Windows systems, configure the Python path and Django settings
    sys.path.insert(0, '/home/gfvpcom/gfvpenv/lib/python3.9/site-packages')
    from django.core.wsgi import get_wsgi_application
    sys.path.insert(1, '/home/gfvpcom/public_html')
    os.environ["DJANGO_SETTINGS_MODULE"] = "gfvp.settings"
    application = get_wsgi_application()        
else:   
    # On Windows systems, configure Django settings 
    os.environ['DJANGO_SETTINGS_MODULE'] = 'gfvp.settings'
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

# Import the 'add_set' function from the 'gfvp.addset' module
from gfvp.addset import add_set

# Call the 'add_set' function to set some important special settings
add_set()
