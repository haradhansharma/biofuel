# Import necessary modules and views.
from . import views
from django.urls import path

# Define the app name for URL namespace.
app_name = 'glossary'

# Define URL patterns for the 'glossary' app.
urlpatterns = [
    # Define a URL pattern for the glossary list view.
    path('', views.Glist.as_view(), name='g_list'),    
]

