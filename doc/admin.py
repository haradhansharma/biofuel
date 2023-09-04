from django.contrib import admin
from .models import *

# Register the 'Acordion' model with the admin site
admin.site.register(Acordion)

# Create an inline admin class for 'ExSite' model
class ExtendSiteOfSite(admin.StackedInline):
    model = ExSite
    can_delete = False   

# Create an admin class for 'Site' model
class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name') # Define the fields to display in the list view
    search_fields = ('domain', 'name') # Define fields to enable search functionality
    inlines = [ExtendSiteOfSite] # Add the 'ExtendSiteOfSite' inline to the 'Site' admin view
    
# Unregister the default 'Site' admin to customize it    
admin.site.unregister(Site)

# Register the 'Site' model with the customized 'SiteAdmin' class
admin.site.register(Site, SiteAdmin)


