from django.contrib import admin
from . models import *
from django_summernote.admin import SummernoteModelAdmin


@admin.register(GenarelGuide)
class GenarelGuideAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)    
    list_filter = ('menu', )

@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'key': ('title',)}   
    # readonly_fields = ('key',)


@admin.register(GuideMenu)
class GuideMenuAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'slug': ('title',)}   
    list_filter = ('guidetype', )
    
    