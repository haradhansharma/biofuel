import os
from pathlib import Path

# django-mkdocs demo parameters!
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

DOCUMENTATION_ROOT = os.path.join(PROJECT_DIR, 'gfvp_docs')
DOCUMENTATION_HTML_ROOT = os.path.join(DOCUMENTATION_ROOT, 'site')
DOCUMENTATION_ACCESS_FUNCTION = lambda user: user.is_authenticated
DOCUMENTATION_XSENDFILE = False
# JQUERY_URL = False
USE_DJANGO_JQUERY = True