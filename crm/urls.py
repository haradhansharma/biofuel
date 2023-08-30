from . import views
from django.urls import path


app_name = 'crm'

urlpatterns = [
    # URL pattern for the leads view
    path('crm/leads', views.leads, name='leads'),
    
    # URL pattern for unsubscribing from emails
    path('crm/unsubscrib/<email>/<code>', views.unsubscrib, name='unsubscrib'),
    
    # URL pattern for subscribing to emails
    path('crm/subscrib/<str:email>', views.subscrib, name='subscrib'),    
    
    # URL pattern for the subscription view
    path('crm/subscription', views.subscription, name='subscription'),    
    
]

