from .views import submit_feedback
from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'feedback'  # Define the app namespace.

urlpatterns = [
    # Define a URL pattern for submitting feedback.
    path('submit/', submit_feedback, name='submit_feedback'),
]

hx_urlpatterns = [
    # You can add additional URL patterns for 'hx' (Hypertext) views here if needed.
    # These can be used for dynamic updates in web applications.
    
]

urlpatterns += hx_urlpatterns # Add 'hx' URL patterns to the main urlpatterns.