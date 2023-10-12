from . import views

from django.urls import path
from django.views.generic.base import TemplateView

# Define the app name for namespacing
app_name = 'home'

# Define URL patterns for the home app
urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Dashboard view
    path('dashboard/', views.dashboard, name='dashboard'),
    # User settings view
    path('dashboard/settings/', views.user_setting, name='user_settings'),
    # Change password view
    path('dashboard/change_pass/', views.password_change, name='change_pass'),
    # path('dashboard/questions/', views.questions, name='questions'),
    # Integrate questions view
    path('dashboard/questionsint/', views.questionsint, name='questionsint'), 
    # Quotations view  
    path('dashboard/quotations/', views.quotations, name='quotations'),
    # path('dashboard/my-services/', views.my_services, name='myservices'), 
    # Add new service view
    path('<str:user_id>/add-new-services/', views.add_new_service, name='add_new_service'),    
    # Quotations ATG view
    path('dashboard/quotationsatg/', views.quotationsatg, name='quotationsatg'),
    # Delete avatar view
    path('delete-avatar/', views.delete_avatar, name='delete_avatar'),   
    # Question details view
    path('dashboard/questions/<str:slug>', views.questions_details, name='questions_details'), 
    # Add quotation view
    path('dashboard/questions/add-quatation/<str:slug>', views.add_quatation, name='add_quatation'), 
    # All reports view
    path('dashboard/allreports/', views.allreports, name='all_reports'),  
    # New questions view
    path('dashboard/new_questions/', views.new_questions, name='new_question'),
    # Quotation report view
    path('quotation/<str:question>/<int:quotation>', views.quotation_report, name='quotation_report'),
    # Webmanifest view
    path('webmanifest/', views.webmanifest, name='webmanifest'),
]

# Define additional URLs for HX views
hx_urlpatterns = [
    # Check user type to get expert view
    path('check_type_to_get_expert/', views.check_type_to_get_expert, name='check_type_to_get_expert'),
    # Add extra view
    path('dashboard/add_extra/<str:pk>', views.add_extra, name='add_extra'),
    # Subtract extra view
    path('dashboard/sub_extra/<str:pk>', views.sub_extra, name='sub_extra'),
    # Child modal data view
    path('modal-data/<str:id>', views.child_modal_data, name='child_modal_data'),
    # Delete suggestion view
    path('sugestion-delete/<str:pk>', views.delete_sugestion, name='delete_sugestions'),
    # Add suggestion view   
    path('add-sugestion/<str:slug>/', views.AddSugestion.as_view(), name='add_sugestions'),
    # Edit suggestion view
    path('edit-sugestion/<str:slug>/<str:pk>/', views.get_edit_sugestion, name='edit_sugestions'),
    # Edit new suggestion view
    path('edit-new-sugestion/<str:pk>/', views.get_edit_new_sugestion, name='edit_new_sugestions'),
    # Get suggestion list view
    path('get-sugestion-list/<str:slug>/', views.get_sugestion_list, name='get_sugestions_list'),
    # Suggest new question option view
    path('new-ques-sugestion/', views.sugest_new_ques_option, name='sugest_new_ques_option'),
    # Get new suggestion list view
    path('new-sugestion-list/', views.get_new_sugestion_list, name='get_new_sugestion_list'),
    
]
# Add the HX URLs to the main urlpatterns
urlpatterns += hx_urlpatterns