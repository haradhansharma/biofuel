# Import the admin module from the Django framework.
from django.contrib import admin

# Import the GRequestsChangeForm and models from the glossary app.
from glossary.forms import GRequestsChangeForm
from .models import *

# Define an inline class for RelatedLinks to be used within the GlossaryAdmin.
class RelatedLinksInline(admin.TabularInline):
    # Specify the model that this inline class is related to.
    model = RelatedLinks
    # Set the initial number of extra forms to display.
    extra = 0

# Define the admin class for the Glossary model.
class GlossaryAdmin(admin.ModelAdmin):
    """
    Custom admin settings for the Glossary model.
    """
    # Specify the model this admin class is associated with.
    model = Glossary

    # Define the list of fields to be displayed in the admin list view.
    list_display = ('title',)

    # Define fields that can be searched in the admin list view.
    search_fields = ('title', 'description')

    # Include the RelatedLinksInline class as an inline form.
    inlines = [RelatedLinksInline,]

# Register the GlossaryAdmin class with the Django admin site for the Glossary model.
admin.site.register(Glossary, GlossaryAdmin)

# Define the admin class for the GRequests model.
class GRequestsAdmin(admin.ModelAdmin):
    """
    Custom admin settings for the GRequests model.
    """
    # Specify the form to be used for this admin class.
    form = GRequestsChangeForm

    # Specify the model this admin class is associated with.
    model = GRequests

    # Define the list of fields to be displayed in the admin list view.
    list_display = ('title',)

# Register the GRequestsAdmin class with the Django admin site for the GRequests model.
admin.site.register(GRequests, GRequestsAdmin)
