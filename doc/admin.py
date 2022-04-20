from django.contrib import admin
from .models import *

admin.site.register(Acordion)

class ExtendSiteOfSite(admin.StackedInline):
    model = ExSite
    can_delete = False   

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')
    inlines = [ExtendSiteOfSite]    
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)