from django.contrib import admin
from .models import Feedback



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Feedback._meta.fields if f.editable and not f.name == "id"] 
    list_filter = ('url', )
    search_fields = ('message', 'name', 'email', )    
    ordering = ('created_at',)
    readonly_fields = ('url', 'message', 'name', 'email', 'phone',)
    
    

