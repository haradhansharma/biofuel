
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView 
from .forms import LoginForm


app_name = 'accounts'


urlpatterns = [
    path('signup/', views.signup, name='signup'),    
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',  authentication_form=LoginForm), name='login'),
      
]

urlpatterns += [
    path('my-profile/', views.userpage, name='user_link'),    
    
]

urlpatterns += [
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),    
]

urlpatterns += [
    path('check-username/', views.check_username, name='check_username'),  
    path('check-email/', views.check_email, name='check_email'),    
    path('<str:user_id>/<str:na_id>/commit-service/', views.commit_service, name='commit_service'),    
    path('<str:user_id>/<str:na_id>/delete-service/', views.delete_service, name='delete_service'),     
     
     
]




