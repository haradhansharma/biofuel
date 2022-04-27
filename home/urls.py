from . import views

from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/', views.user_setting, name='user_settings'),
    path('dashboard/change_pass/', views.password_change, name='change_pass'),
    path('dashboard/questions/', views.questions, name='questions'),
    path('dashboard/questions/<str:slug>', views.questions_details, name='questions_details'), 
    path('dashboard/questions/add-quatation/<str:slug>', views.add_quatation, name='add_quatation'), 
    path('dashboard/allreports/', views.allreports, name='all_reports'),  
    path('dashboard/new_questions/', views.new_questions, name='new_question'),
    path('quotation/<str:question>/<int:quotation>', views.quotation_report, name='quotation_report'),
]

hx_urlpatterns = [
    
    path('check_type_to_get_expert/', views.check_type_to_get_expert, name='check_type_to_get_expert'),
    path('dashboard/add_extra/<str:pk>', views.add_extra, name='add_extra'),
    path('dashboard/sub_extra/<str:pk>', views.sub_extra, name='sub_extra'),
    
]

urlpatterns += hx_urlpatterns