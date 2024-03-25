import requests
from django.conf import settings
from django.urls import reverse

def add_set():  
    setattr(settings, 'CNN', False)
    return None