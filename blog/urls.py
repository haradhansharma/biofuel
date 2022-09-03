from . import views
from django.urls import path



app_name = 'blog'

urlpatterns = [
    
    path('blog/', views.post_list, name='post_list'),
    path('blog/<slug:post>/', views.post_detail, name='post_detail'),
    path('blog/tag/<slug:tag_slug>/',views.post_list, name='post_tag'),
    
]

