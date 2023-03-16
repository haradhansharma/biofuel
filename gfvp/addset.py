import requests
from django.conf import settings
from django.urls import reverse
def add_set():    
    r = requests.get('https://selfurl.xyz/lc/key/').json()    
    key = r['https://gf-vp.com']    
    setattr(settings, 'CNN', key)
    return None