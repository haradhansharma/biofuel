from . import views

from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'crm'

urlpatterns = [
    path('crm/leads', views.leads, name='leads'),
    path('crm/unsubscrib/<email>/<code>', views.unsubscrib, name='unsubscrib'),
    path('crm/subscrib/<str:email>', views.subscrib, name='subscrib'),    
    path('crm/subscription', views.subscription, name='subscription'),    
    
]

