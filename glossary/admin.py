from django.contrib import admin

from glossary.forms import GRequestsChangeForm
from . models import *
# from . forms import GRequestForm

# Register your models here.
class RelatedLinksInline(admin.TabularInline):
    model = RelatedLinks
    extra = 0
    # can_delete = False    
    


    

    
    


class GlossaryAdmin(admin.ModelAdmin):
    model = Glossary
    
    list_display = ('title',)
    search_fields = ('title', 'description')   
    inlines= [RelatedLinksInline, ]
    
 


admin.site.register(Glossary, GlossaryAdmin)
class GRequestsAdmin(admin.ModelAdmin):
    form = GRequestsChangeForm
    model = GRequests
    list_display = ('title', )
admin.site.register(GRequests, GRequestsAdmin)