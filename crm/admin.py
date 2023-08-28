from django.contrib import admin
from .models import *

# Register the Lead model with the admin site.
admin.site.register(Lead)

# Decorator-based registration of the MailQueue model with the admin site.
@admin.register(MailQueue)
class MailQueueAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the MailQueue model.
    """

    # Generate a list of field names to display in the admin list view.
    list_display = [f.name for f in MailQueue._meta.fields if not f.name == "id"] 

# Decorator-based registration of the BlogMailQueue model with the admin site.
@admin.register(BlogMailQueue)
class BlogMailQueueAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for the BlogMailQueue model.
    """

    # Generate a list of field names to display in the admin list view.
    list_display = [f.name for f in BlogMailQueue._meta.fields if not f.name == "id"] 
