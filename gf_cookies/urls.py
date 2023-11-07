from django.urls import path
from .views import cookie_consent

app_name = 'gf_cookies'
urlpatterns = [
    path('cookie-consent/', cookie_consent, name='cookie_consent'),
]