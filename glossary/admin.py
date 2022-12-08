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
    # list_display = [ 'id', 'user', 'service', 'service_option', 'order_amount', 'paid_amount', 'payment_method']
    # readonly_fields = [
    #     'user', 
    #     'service', 
    #     'service_option', 
    #     'order_amount', 
    #     'paid_amount', 
    #     'payment_method', 
    #     'tentative_delivery_date', 
    #     'full_payment_date', 
    #     'shipping_address', 
    #     'payment_address',
    #     'last_status',
    #     ]
    inlines= [RelatedLinksInline, ]
    
 


admin.site.register(Glossary, GlossaryAdmin)


class GRequestsAdmin(admin.ModelAdmin):
    form = GRequestsChangeForm
    model = GRequests
    list_display = ('title', )
admin.site.register(GRequests, GRequestsAdmin)