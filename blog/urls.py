from . import views
from django.urls import path

# Set the app name for URL reversing
app_name = 'blog'

urlpatterns = [
    # URL for the list of all blog posts
    path('blog/', views.post_list, name='post_list'),
    # e.g., 'blog/' will route to views.post_list() with the name 'post_list'
    
    # URL for viewing a specific blog post by its slug
    path('blog/<slug:post>/', views.post_detail, name='post_detail'),
    # e.g., 'blog/my-blog-post/' will route to views.post_detail(slug='my-blog-post') with the name 'post_detail'
    
    # URL for viewing blog posts filtered by a specific tag
    path('blog/tag/<slug:tag_slug>/',views.post_list, name='post_tag'),
    # e.g., 'blog/tag/my-tag/' will route to views.post_list(tag_slug='my-tag') with the name 'post_tag'
    
]

