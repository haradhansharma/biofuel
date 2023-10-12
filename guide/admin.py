from django.contrib import admin
from . models import * # Import all models from the current module
from django_summernote.admin import SummernoteModelAdmin

# Register the GenarelGuide model with the admin site
@admin.register(GenarelGuide)
class GenarelGuideAdmin(SummernoteModelAdmin):
    """
    Admin class for managing GenarelGuide model.

    This class extends SummernoteModelAdmin to provide a rich text editor for the 'content' field.
    """
    summernote_fields = ('content',) # Enable Summernote for the 'content' field     
    list_filter = ('menu', ) # Add a filter for the 'menu' field

# Register the GuideType model with the admin site
@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):    
    """
    Admin class for managing GuideType model.

    This class includes prepopulated_fields for the 'key' field based on the 'title' field.
    """
    prepopulated_fields = {'key': ('title',)}  # Auto-generate 'key' based on 'title'
    # readonly_fields = ('key',)  # Uncomment this line if 'key' should be read-only

# Register the GuideMenu model with the admin site
@admin.register(GuideMenu)
class GuideMenuAdmin(admin.ModelAdmin):    
    """
    Admin class for managing GuideMenu model.

    This class includes prepopulated_fields for the 'slug' field based on the 'title' field
    and a list filter for the 'guidetype' field.
    """
    prepopulated_fields = {'slug': ('title',)} # Auto-generate 'slug' based on 'title'   
    list_filter = ('guidetype', ) # Add a filter for the 'guidetype' field
    
    