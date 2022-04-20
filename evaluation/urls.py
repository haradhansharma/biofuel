from django.urls import path
from . import views

app_name = 'evaluation'
urlpatterns = [   
    path('evaluation/thanks/', views.thanks, name='thanks'),      
    path('evaluation/report/<str:slug>', views.report, name='report'),    
]

urlpatterns += [
    path('evaluation2/', views.eva_index2, name='evaluation2'), 
    path('evaluation2/option_add/', views.option_add2, name='option_add2'),  
    path('evaluation2/<int:evaluator>/<str:slug>', views.eva_question, name='eva_question'),   
    
]
