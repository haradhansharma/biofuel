from . import views

from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'guide'

urlpatterns = [
    path('guide', views.guide_home, name='guide_home'),
    path('guide/evaluation', views.guide_evaluation, name='evaluation'),
    
]

