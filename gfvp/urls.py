
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import user_types




admin.site.site_header = 'GF-VP admin'
admin.site.site_title = 'GF-VP admin'
# admin.site.site_url = 'http://gf-vp.com/'
admin.site.index_title = 'GF-VP administration'
# admin.empty_value_display = '**Empty**'

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('evaluation.urls')),
    path('', include('home.urls')),
    path('', include('crm.urls')),
    path('<str:slug>/', user_types, name='types'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
