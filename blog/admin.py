from django.contrib import admin
from blog.models import *
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin

        
@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    # Enables the Summernote rich text editor for the 'body' field
    summernote_fields = ('body',)
    
    # Displayed columns in the change list view
    list_display = ('title', 'slug', 'author', 'publish', 'updated', 'status')
    
    # Filters for the change list view
    list_filter = ('status', 'created', 'publish', 'author')
    
    # Search fields for the search bar
    search_fields = ('title', 'body')
    
    # Adds a date-based navigation hierarchy
    date_hierarchy = 'publish'
    
    # Specifies the default ordering in the change list view
    ordering = ('status', 'publish')
    
    # This method is executed when a model is saved in the admin panel
    def save_model(self, request, obj, form, change):
        # Set the author of the blog post to the current logged-in user
        obj.author = request.user
        
        # If the status is 'published', set the publish date to the current time
        if obj.status == 'published':
            obj.publish = timezone.now()
        
        # Save the model with the modified data
        super().save_model(request, obj, form, change)