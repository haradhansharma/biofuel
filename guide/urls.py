from . import views

from django.urls import path, include
from django.views.generic.base import TemplateView


app_name = 'guide'

urlpatterns = [
    # URL pattern for the guide home page
    path('guide', views.guide_home, name='guide_home'),
    
    # URL pattern for a specific guide type
    path('guide/<str:key>', views.guide_type, name='guide_type'),
    
    # URL pattern for a general guide under a specific guide type
    path('guide/<str:gt>/<str:slug>', views.genarel_guide, name='genarel_guide'),
    
]


# In Django, urlpatterns is a list of URL patterns that map URLs to views or other URL patterns.
# Each path() function call represents a URL pattern.
# The first argument of path() is the URL path, and the second argument is the view function to be called.
# The 'name' parameter assigns a unique name to each URL pattern, which can be used in templates or reverse URL lookups.

# For example:
# - '/guide' maps to the 'guide_home' view.
# - '/guide/<str:key>' maps to the 'guide_type' view, where 'key' is a dynamic parameter extracted from the URL.
# - '/guide/<str:gt>/<str:slug>' maps to the 'genarel_guide' view, where 'gt' and 'slug' are dynamic parameters.

# The 'app_name' variable sets the namespace for these URL patterns, which can help avoid naming conflicts in larger Django projects.

