from django.contrib import admin
from . models import *


admin.site.register(GenarelGuide)



@admin.register(GuideType)
class GuideTypeAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'key': ('title',)}   
    # readonly_fields = ('key',)


@admin.register(GuideMenu)
class GuideMenuAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'slug': ('title',)}   
    
    