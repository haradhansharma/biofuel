from . import views

from django.urls import path, include
from django.views.generic.base import TemplateView


app_name = 'guide'

urlpatterns = [
    path('guide', views.guide_home, name='guide_home'),
    path('guide/<str:key>', views.guide_type, name='guide_type'),
    path('guide/<str:gt>/<str:slug>', views.genarel_guide, name='genarel_guide'),
    
    
    
]

