
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import user_types
from django.views.generic.base import TemplateView
# from django.views.static import serve
from accounts.views import partner_service





admin.site.site_header = 'GF-VP admin'
admin.site.site_title = 'GF-VP admin'
# admin.site.site_url = 'http://gf-vp.com/'
admin.site.index_title = 'GF-VP administration'
# admin.empty_value_display = '**Empty**'

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('chaining/', include('smart_selects.urls')),
    
    path('', include('evaluation.urls')),
    path('', include('home.urls')),
    path('', include('crm.urls')),
    path('', include('guide.urls')),
    path('', include('blog.urls')),
    path('g/', include('glossary.urls')),
    path('feedback/', include('feedback.urls')),
    
    path('types/<str:slug>/', user_types, name='types'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("gdpr-policy/", TemplateView.as_view(template_name="includes/gdpr.html"), name='gdpr'),
    path("terms/", TemplateView.as_view(template_name="includes/terms.html"), name='term'),
    path('docs/', include('django_mkdocs.urls', namespace='mkdocs')),    
    path('<int:pk>/services/', partner_service, name='partner_service'),    
    

    
] 

# if settings.DEBUG:
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    


