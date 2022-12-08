from . import views

from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'glossary'

urlpatterns = [
    path('', views.Glist.as_view(), name='g_list'),    
]

