from .views import submit_feedback
from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'feedback'

urlpatterns = [
    path('submit/', submit_feedback, name='submit_feedback'),
    
    
    
    
]

hx_urlpatterns = [
    
    
    
    
    
    
    
]

urlpatterns += hx_urlpatterns