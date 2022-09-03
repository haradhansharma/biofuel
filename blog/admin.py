from django.contrib import admin

from blog.models import *
from django.utils import timezone





@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'updated', 'status',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    
    
    #this is for admin only, if you want to write same then modify in the views
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if obj.status == 'published':
            obj.publish = timezone.now()
        else:
            obj.publish = timezone.now()         
        
        super().save_model(request, obj, form, change)