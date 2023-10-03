# admin.py - Django Admin Configuration for Feedback Model

from django.contrib import admin
from .models import Feedback


# Register the Feedback model with the Django admin site.
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the Feedback model.

    This class defines how the Feedback model should be displayed and
    filtered in the Django admin interface.

    Attributes:
        list_display (list of str): Fields to display in the list view.
        list_filter (tuple of str): Fields to use for filtering records.
        search_fields (tuple of str): Fields to use for searching records.
        ordering (tuple of str): Fields to determine the default ordering of records.
        readonly_fields (tuple of str): Fields that should be read-only in the admin interface.
    """

    # Display these fields in the list view of the admin interface.
    list_display = [f.name for f in Feedback._meta.fields if f.editable and not f.name == "id"] 
    
    # Allow filtering by the 'url' field in the right sidebar.
    list_filter = ('url', )
    
    # Enable searching by 'message', 'name', and 'email' fields.
    search_fields = ('message', 'name', 'email', )    
    
    # Order records by 'created_at' in descending order by default.
    ordering = ('-created_at',)
    
     # Make 'url', 'message', 'name', 'email', and 'phone' fields read-only.
    readonly_fields = ('url', 'message', 'name', 'email', 'phone',)
    
    

