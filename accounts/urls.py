
from .forms import LoginForm
from django.urls import path
from . import views

# Set the app_name to 'accounts' to avoid URL naming conflicts
app_name = 'accounts'

# Define the URL patterns for the 'accounts' app
urlpatterns = [
    # URL pattern for user signup
    path('signup/', views.signup, name='signup'),

    # URL pattern for user login with a custom login view
    path('login/', views.CustomLoginView.as_view(
        redirect_authenticated_user=True,
        template_name='registration/login.html',
        authentication_form=LoginForm
    ), name='login'),

    # URL pattern for user profile page
    path('my-profile/', views.userpage, name='user_link'),

    # URL pattern for user activation with token
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # URL patterns for checking username and email availability
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),

    # URL patterns for committing and deleting user services
    path('<str:user_id>/<str:na_id>/commit-service/', views.commit_service, name='commit_service'),
    path('<str:user_id>/<str:na_id>/delete-service/', views.delete_service, name='delete_service'),
]

