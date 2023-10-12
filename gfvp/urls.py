# Import necessary modules
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from home.views import user_types
from django.views.generic.base import TemplateView
from accounts.views import partner_service, producer_fuels

# Configure the Django admin site. But it is not workable in Material Admin
# if you are looking for material admin then look into the gfvp/settings/settings_material_admin.py
admin.site.site_header = 'GF-VP admin'
admin.site.site_title = 'GF-VP admin'
admin.site.index_title = 'GF-VP administration'
admin.empty_value_display = '**Empty**'


# Define the URL patterns for the Django application
urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    
    # Debug Toolbar URL for debugging purposes
    path('__debug__/', include('debug_toolbar.urls')),
    
    # Smart selects URL for chaining select fields
    path('chaining/', include('smart_selects.urls')),
    
    
    # Include URLs for various app modules
    path('', include('evaluation.urls')),
    path('', include('home.urls')),
    path('', include('crm.urls')),
    path('', include('guide.urls')),
    path('', include('blog.urls')),
    path('g/', include('glossary.urls')),
    path('feedback/', include('feedback.urls')),   
    
    # URL for displaying user types 
    path('types/<str:slug>/', user_types, name='types'),
    
    # Include URLs for user accounts and authentication
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # URL for integrating the Summernote WYSIWYG editor
    path('summernote/', include('django_summernote.urls')),
    
    # URL for taggit autosuggest functionality
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),  
    
    # URL for displaying GDPR policy
    path("gdpr-policy/", TemplateView.as_view(template_name="includes/gdpr.html"), name='gdpr'),
    
    # URL for displaying terms and conditions
    path("terms/", TemplateView.as_view(template_name="includes/terms.html"), name='term'),
    
    # URL for integrating MkDocs documentation
    path('docs/', include('django_mkdocs.urls', namespace='mkdocs')), 
    
    # URL for displaying partner services    
    path('<int:pk>/services/', partner_service, name='partner_service'), 
    
    # URL for displaying producer fuels
    path('<int:pk>/producer-fuels/', producer_fuels, name='producer_fuels'),     
        
] 


# If the application is in DEBUG mode, include URLs for serving media and static files
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    


