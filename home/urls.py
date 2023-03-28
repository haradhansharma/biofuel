from . import views

from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/', views.user_setting, name='user_settings'),
    path('dashboard/change_pass/', views.password_change, name='change_pass'),
    # path('dashboard/questions/', views.questions, name='questions'),
    path('dashboard/questionsint/', views.questionsint, name='questionsint'),   
    path('dashboard/quotations/', views.quotations, name='quotations'),
    # path('dashboard/my-services/', views.my_services, name='myservices'),
    path('<str:user_id>/add-new-services/', views.add_new_service, name='add_new_service'),
    
    
    path('dashboard/quotationsatg/', views.quotationsatg, name='quotationsatg'),
    path('delete-avatar/', views.delete_avatar, name='delete_avatar'),   
    path('dashboard/questions/<str:slug>', views.questions_details, name='questions_details'), 
    path('dashboard/questions/add-quatation/<str:slug>', views.add_quatation, name='add_quatation'), 
    path('dashboard/allreports/', views.allreports, name='all_reports'),  
    path('dashboard/new_questions/', views.new_questions, name='new_question'),
    path('quotation/<str:question>/<int:quotation>', views.quotation_report, name='quotation_report'),
    path('seo/webmanifest/', views.webmanifest, name='webmanifest'),
    
    
    
    
]

hx_urlpatterns = [
    
    path('check_type_to_get_expert/', views.check_type_to_get_expert, name='check_type_to_get_expert'),
    path('dashboard/add_extra/<str:pk>', views.add_extra, name='add_extra'),
    path('dashboard/sub_extra/<str:pk>', views.sub_extra, name='sub_extra'),
    path('modal-data/<str:id>', views.child_modal_data, name='child_modal_data'),
    path('sugestion-delete/<str:pk>', views.delete_sugestion, name='delete_sugestions'),   
    path('add-sugestion/<str:slug>/', views.AddSugestion.as_view(), name='add_sugestions'),
    path('edit-sugestion/<str:slug>/<str:pk>/', views.get_edit_sugestion, name='edit_sugestions'),
    path('edit-new-sugestion/<str:pk>/', views.get_edit_new_sugestion, name='edit_new_sugestions'),
    
    path('get-sugestion-list/<str:slug>/', views.get_sugestion_list, name='get_sugestions_list'),
    path('new-ques-sugestion/', views.sugest_new_ques_option, name='sugest_new_ques_option'),
    path('new-sugestion-list/', views.get_new_sugestion_list, name='get_new_sugestion_list'),
    
    
    
    
    
]

urlpatterns += hx_urlpatterns