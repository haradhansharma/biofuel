from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Lead)

@admin.register(MailQueue)
class MailQueueAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MailQueue._meta.fields if not f.name == "id"] 
    
@admin.register(BlogMailQueue)
class BlogMailQueueAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BlogMailQueue._meta.fields if not f.name == "id"] 
    
