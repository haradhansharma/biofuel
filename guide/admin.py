from django.contrib import admin
from . models import *



@admin.register(GenarelGuide)
class GenarelGuideAdmin(admin.ModelAdmin):
    list_filter = ('menu', )
    



@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'key': ('title',)}   
    # readonly_fields = ('key',)


@admin.register(GuideMenu)
class GuideMenuAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'slug': ('title',)}   
    
    