from django.shortcuts import render
from .models import *


def guide_home(request):     
    guide_type = GuideType.objects.all().order_by('position')  
    context = {
        "guide_type": guide_type,          
    }
    return render(request, 'guide/bg_home.html', context = context)

def guide_type(request, key):    
    guide_general_menu = GuideMenu.objects.filter(type = GuideType.objects.get(key=key)).order_by('position')      
    type = GuideType.objects.filter(key=key).order_by('position')   
    
    context = {
        "type": type,
        'guide_general_menu' : guide_general_menu
    }
    return render(request, 'guide/bg_guide_type.html', context = context)


    
def genarel_guide(request, slug, type):
    guide_general_menu = GuideMenu.objects.filter(type =  GuideType.objects.get(key=type)).order_by('position')      
    guide = GenarelGuide.objects.filter(menu = guide_general_menu.get(slug=slug)).order_by('position')       
    
    context = {
        'guide_general_menu' : guide_general_menu ,
        'guide' : guide ,      
    }
    return render(request, 'guide/bg_genarel_guide.html', context = context)
        